#!/usr/bin/env python3
"""Build a narration timeline from measured WAV files.

usage: timeline.py SEGMENTS.json OUT_DIR [--force]

SEGMENTS.json:
  {"fps": 30, "lead": 0.25, "tail": 0.65,
   "segments": [{"id": "intro", "wav": "audio/intro.wav", "caption": "Text as spoken."},
                {"id": "pause", "silence": 1.5}]}
Paths are relative to SEGMENTS.json. All WAVs must share sample rate, channels and sample width.

Writes OUT_DIR/voice.wav (PCM, never re-encoded), OUT_DIR/timing.json (every segment's start/end in
seconds and frames, for the visuals to follow) and OUT_DIR/captions.srt (one cue per spoken segment,
from its measured speech start to end). Prints timing.json. Exit 2 on bad input.
Segment length = lead + measured audio + tail, rounded UP to whole frames with integer arithmetic;
boundaries are placed on cumulative frames, so audio and frames never drift apart.
"""
import json, os, sys, wave
from fractions import Fraction
from math import ceil

def fail(msg):
    print(f'timeline.py: {msg}', file=sys.stderr)
    sys.exit(2)

def srt_time(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600_000); m, ms = divmod(ms, 60_000); s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def main(argv):
    args = [a for a in argv if a != '--force']
    force = '--force' in argv
    if len(args) != 2:
        fail(__doc__.strip().splitlines()[2])
    spec_path, out = args
    try:
        with open(spec_path) as spec_file:
            spec = json.load(spec_file)
    except (OSError, ValueError) as e:
        fail(f'cannot read {spec_path}: {e}')
    base = os.path.dirname(os.path.abspath(spec_path))
    fps = Fraction(str(spec.get('fps', 30)))
    lead, tail = Fraction(str(spec.get('lead', 0.25))), Fraction(str(spec.get('tail', 0.65)))
    segs = spec.get('segments') or fail('no segments')
    targets = [os.path.join(out, n) for n in ('voice.wav', 'timing.json', 'captions.srt')]
    if not force and any(os.path.exists(t) for t in targets):
        fail(f'{out} already holds timeline output; pass --force to replace it')
    fmt, clips = None, []
    for s in segs:
        if 'id' not in s:
            fail(f'segment without id: {s}')
        if 'wav' in s:
            p = os.path.join(base, s['wav'])
            try:
                with wave.open(p, 'rb') as w:
                    f = (w.getframerate(), w.getnchannels(), w.getsampwidth())
                    data = w.readframes(w.getnframes())
            except (OSError, wave.Error, EOFError) as e:
                fail(f'{s["id"]}: cannot read PCM WAV {p}: {e}')
            if fmt and f != fmt:
                fail(f'{s["id"]}: format {f} differs from {fmt}; resample all WAVs to one format first')
            fmt = f
            clips.append((s, data))
        elif 'silence' in s:
            clips.append((s, None))
        else:
            fail(f'{s["id"]}: needs "wav" or "silence"')
    if fmt is None:
        fail('at least one segment needs a wav')
    rate, ch, width = fmt
    bpf = ch * width  # bytes per sample frame
    os.makedirs(out, exist_ok=True)
    frame_pos, sample_pos, rows, cues, pcm = 0, 0, [], [], bytearray()
    for s, data in clips:
        if data is None:
            dur = Fraction(str(s['silence'])); speech = None
            body = Fraction(0)
        else:
            n = len(data) // bpf
            speech = Fraction(n, rate)
            dur = lead + speech + tail
        frames = ceil(dur * fps)
        end_frame = frame_pos + frames
        end_sample = round(Fraction(end_frame) * rate / fps)
        seg_samples = end_sample - sample_pos
        if data is None:
            pcm += bytes(seg_samples * bpf)
        else:
            lead_samples = round(lead * rate)
            pad = seg_samples - lead_samples - len(data) // bpf
            pcm += bytes(lead_samples * bpf) + data + bytes(pad * bpf)
        start_s = float(Fraction(frame_pos) / fps)
        row = {'id': s['id'], 'start_frame': frame_pos, 'end_frame': end_frame, 'frames': frames,
               'start_s': round(start_s, 6), 'end_s': round(float(Fraction(end_frame) / fps), 6)}
        if speech is not None:
            sp0 = Fraction(sample_pos, 1) / rate + lead
            row['speech_start_s'] = round(float(sp0), 6)
            row['speech_end_s'] = round(float(sp0 + speech), 6)
            if s.get('caption'):
                cues.append((row['speech_start_s'], row['speech_end_s'], s['caption']))
        rows.append(row)
        frame_pos, sample_pos = end_frame, end_sample
    with wave.open(targets[0], 'wb') as w:
        w.setnchannels(ch); w.setsampwidth(width); w.setframerate(rate); w.writeframes(bytes(pcm))
    timing = {'fps': float(fps), 'total_frames': frame_pos, 'duration_s': round(float(Fraction(frame_pos) / fps), 6),
              'sample_rate': rate, 'segments': rows}
    with open(targets[1], 'w') as f:
        json.dump(timing, f, indent=1)
    with open(targets[2], 'w') as f:
        for i, (a, b, text) in enumerate(cues, 1):
            f.write(f'{i}\n{srt_time(a)} --> {srt_time(b)}\n{text}\n\n')
    print(json.dumps(timing, indent=1))

if __name__ == '__main__':
    main(sys.argv[1:])
