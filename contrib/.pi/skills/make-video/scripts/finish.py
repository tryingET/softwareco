#!/usr/bin/env python3
"""Finish a rendered video for delivery: add audio once, fix colour range, verify, make review images.

usage: finish.py --video IN.mp4 --out OUT.mp4 [--voice voice.wav] [--music bed.wav] [--music-db -18]
                 [--subs captions.srt --subs-lang deu] [--stills 1.5,12,30] [--sheet 16] [--crf 18] [--force]

- Video: re-encoded once to H.264 high, yuv420p, tv range, BT.709 tags, +faststart. Full-range
  input (Director's yuvj420p) is converted with scale=in_range=full:out_range=tv.
- Audio: voice and music are mixed in one pass, music ducked under the voice, loudness-normalised
  to -16 LUFS (true peak -1.5 dB), padded to the video length and encoded to AAC exactly once.
  Audio longer than the video is an error (exit 3): lengthen the visuals, never cut the voice.
- Subtitles: soft mov_text track (players can switch it off).
- Review: OUT_DIR/review/still-<t>.png at each --stills time and sheet.png (a tiled contact sheet).
Prints a JSON report; exit 0 only when every check passed (exit 1 = a check failed, 2 = bad input).
"""
import argparse, json, os, re, subprocess, sys

def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'finish.py: cannot probe {path}: {r.stderr.strip()}')
    return json.loads(r.stdout)

def duration(info):
    return float(info['format']['duration'])

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'finish.py: command failed ({r.returncode}): {" ".join(cmd)}\n{r.stderr[-3000:]}')
    return r

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--video', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--voice'); ap.add_argument('--music'); ap.add_argument('--music-db', type=float, default=-18)
    ap.add_argument('--subs'); ap.add_argument('--subs-lang', default='und')
    ap.add_argument('--stills', default=''); ap.add_argument('--sheet', type=int, default=16)
    ap.add_argument('--crf', type=int, default=18); ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    for p in (a.video, a.voice, a.music, a.subs):
        if p and not os.path.isfile(p):
            print(f'finish.py: missing input {p}', file=sys.stderr); sys.exit(2)
    if os.path.exists(a.out) and not a.force:
        print(f'finish.py: {a.out} exists; pass --force to replace it', file=sys.stderr); sys.exit(2)
    vin = probe(a.video)
    vs = next((s for s in vin['streams'] if s['codec_type'] == 'video'), None)
    if not vs:
        print('finish.py: no video stream', file=sys.stderr); sys.exit(2)
    vdur = duration(vin)
    num, den = map(int, vs.get('avg_frame_rate', '30/1').split('/'))
    frame = den / num if num else 1 / 30
    for p in (a.voice, a.music):
        if p and a.voice == p and duration(probe(p)) > vdur + frame:
            print(json.dumps({'ok': False, 'error': 'voice longer than video', 'voice_s': duration(probe(p)),
                              'video_s': vdur}), flush=True)
            sys.exit(3)
    full = vs.get('pix_fmt', '').startswith('yuvj') or vs.get('color_range') == 'pc'
    vf = ('scale=in_range=full:out_range=tv,' if full else '') + 'format=yuv420p'
    cmd = ['ffmpeg', '-y', '-v', 'error', '-i', a.video]
    inputs = 1; amap = None; filt = [f'[0:v]{vf}[v]']
    norm = 'loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000'
    if a.voice:
        cmd += ['-i', a.voice]; vi = inputs; inputs += 1
    if a.music:
        cmd += ['-stream_loop', '-1', '-i', a.music]; mi = inputs; inputs += 1
    if a.voice and a.music:
        filt += [f'[{vi}:a]aresample=48000,asplit=2[vo][key]',
                 f'[{mi}:a]aresample=48000,volume={a.music_db}dB[mu]',
                 '[mu][key]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[duck]',
                 f'[vo][duck]amix=inputs=2:duration=first:normalize=0,apad,atrim=0:{vdur:.6f},{norm}[a]']
        amap = '[a]'
    elif a.voice or a.music:
        i = vi if a.voice else mi
        filt.append(f'[{i}:a]aresample=48000,apad,atrim=0:{vdur:.6f},{norm}[a]'); amap = '[a]'
    if a.subs:
        cmd += ['-i', a.subs]; si = inputs; inputs += 1
    cmd += ['-filter_complex', ';'.join(filt), '-map', '[v]']
    if amap:
        cmd += ['-map', amap, '-c:a', 'aac', '-b:a', '192k']
    if a.subs:
        cmd += ['-map', f'{si}:s', '-c:s', 'mov_text', f'-metadata:s:s:0', f'language={a.subs_lang}']
    cmd += ['-c:v', 'libx264', '-profile:v', 'high', '-preset', 'slow', '-crf', str(a.crf),
            '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
            '-t', f'{vdur:.6f}', '-movflags', '+faststart', a.out]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    run(cmd)
    out = probe(a.out)
    ov = next(s for s in out['streams'] if s['codec_type'] == 'video')
    oa = next((s for s in out['streams'] if s['codec_type'] == 'audio'), None)
    checks = {'h264': ov['codec_name'] == 'h264', 'yuv420p': ov.get('pix_fmt') == 'yuv420p',
              'tv_range': ov.get('color_range') == 'tv',
              'duration_matches': abs(duration(out) - vdur) <= 2 * frame}
    report = {'out': os.path.abspath(a.out), 'width': ov['width'], 'height': ov['height'],
              'fps': ov.get('avg_frame_rate'), 'duration_s': round(duration(out), 3), 'size_bytes': int(out['format']['size'])}
    if amap:
        checks['audio_aac'] = bool(oa) and oa['codec_name'] == 'aac'
        r = subprocess.run(['ffmpeg', '-nostats', '-i', a.out, '-map', '0:a', '-af', 'ebur128', '-f', 'null', '-'],
                           capture_output=True, text=True)
        m = re.findall(r'I:\s+(-?[\d.]+) LUFS', r.stderr)
        report['integrated_lufs'] = float(m[-1]) if m else None
        checks['loudness_near_-16'] = report['integrated_lufs'] is not None and abs(report['integrated_lufs'] + 16) <= 2
    if a.subs:
        checks['subtitle_track'] = any(s['codec_type'] == 'subtitle' for s in out['streams'])
    rev = os.path.join(os.path.dirname(os.path.abspath(a.out)), 'review'); os.makedirs(rev, exist_ok=True)
    stills = []
    for t in [x for x in a.stills.split(',') if x.strip()]:
        p = os.path.join(rev, f'still-{t.strip()}.png')
        run(['ffmpeg', '-y', '-v', 'error', '-ss', t.strip(), '-i', a.out, '-frames:v', '1', p]); stills.append(p)
    if a.sheet > 0:
        n = a.sheet; cols = 4; rows = -(-n // cols)
        step = max(duration(out) / n, frame)
        p = os.path.join(rev, 'sheet.png')
        run(['ffmpeg', '-y', '-v', 'error', '-i', a.out, '-vf',
             f'fps=1/{step:.6f},scale=480:-2,tile={cols}x{rows}', '-frames:v', '1', p]); report['sheet'] = p
    report['stills'] = stills
    report['checks'] = checks
    report['ok'] = all(checks.values())
    print(json.dumps(report, indent=1))
    sys.exit(0 if report['ok'] else 1)

if __name__ == '__main__':
    main()
