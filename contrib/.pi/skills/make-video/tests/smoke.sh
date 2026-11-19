#!/usr/bin/env bash
# Smoke test of the make-video helpers with fabricated content. Needs espeak-ng, ffmpeg, node 22+, chromium.
# Runs in a fresh folder under $TMPDIR (must not be /tmp) and deletes it afterwards unless KEEP=1.
set -euo pipefail
HERE=$(cd "$(dirname "$0")/../scripts" && pwd)
[[ -n "${TMPDIR:-}" && "$TMPDIR" != /tmp* ]] || { echo 'set TMPDIR to a folder on /data' >&2; exit 2; }
mkdir -p "$TMPDIR"; W=$(mktemp -d "$TMPDIR/make-video-smoke-XXXX")
[[ "${KEEP:-0}" == 1 ]] || trap 'rm -rf "$W"' EXIT
cd "$W"; fails=0
pass() { echo "PASS $1"; }; bad() { echo "FAIL $1"; fails=$((fails+1)); }

mkdir audio
espeak-ng -v en -w audio/a.wav 'Tally takes a job.'
espeak-ng -v en -w audio/b.wav 'Then it hands the job to a worker.'
cat > seg.json <<'EOF'
{"fps": 30, "segments": [{"id": "a", "wav": "audio/a.wav", "caption": "Tally takes a job."},
  {"id": "gap", "silence": 0.5},
  {"id": "b", "wav": "audio/b.wav", "caption": "Then it hands the job to a worker."}]}
EOF
python3 "$HERE/timeline.py" seg.json tl > tl.json
python3 - <<'EOF' && pass timeline-frames-align || bad timeline-frames-align
import json, wave
t = json.load(open('tl.json'))
w = wave.open('tl/voice.wav'); n, r = w.getnframes(), w.getframerate()
assert abs(n / r - t['total_frames'] / 30) < 1 / r, (n / r, t['total_frames'] / 30)
segs = t['segments']; assert all(a['end_frame'] == b['start_frame'] for a, b in zip(segs, segs[1:]))
assert segs[0]['speech_start_s'] == 0.25 and open('tl/captions.srt').read().count('-->') == 2
EOF
python3 "$HERE/timeline.py" seg.json tl >/dev/null 2>&1 && bad timeline-refuses-overwrite || pass timeline-refuses-overwrite
sox audio/a.wav -r 16000 audio/c.wav 2>/dev/null || ffmpeg -v error -i audio/a.wav -ar 16000 audio/c.wav
echo '{"segments":[{"id":"a","wav":"audio/a.wav"},{"id":"c","wav":"audio/c.wav"}]}' > mixed.json
set +e; python3 "$HERE/timeline.py" mixed.json tl2 >/dev/null 2>&1; rc=$?; set -e
[[ $rc == 2 ]] && pass timeline-rejects-mixed-formats || bad "timeline-rejects-mixed-formats rc=$rc"

DUR=$(python3 -c "import json;print(json.load(open('tl.json'))['duration_s'])")
cat > page.html <<'EOF'
<!doctype html><meta charset=utf-8><style>html,body{margin:0;background:#101820}canvas{display:block}
#t{position:absolute;left:12px;top:8px;color:#fff;font:20px sans-serif}</style>
<canvas id=c width=320 height=180></canvas><div id=t></div><script>
const gl = document.getElementById('c').getContext('webgl', {preserveDrawingBuffer: true});
window.seek = s => { const k = (s % 2) / 2; gl.clearColor(k, 0.3, 1 - k, 1); gl.clear(gl.COLOR_BUFFER_BIT);
  document.getElementById('t').textContent = 'Tally ' + s.toFixed(2); };
window.seek(0); window.__ready = !!gl;
</script>
EOF
node "$HERE/capture.mjs" page.html --duration "$DUR" --size 320x180 --workers 2 --out out/video.mp4 > cap.json
frames=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 out/video.mp4)
[[ "$frames" == $(python3 -c "import json;print(json.load(open('tl.json'))['total_frames'])") ]] && pass capture-frame-count || bad "capture-frame-count $frames"
node "$HERE/capture.mjs" page.html --stills 0.5,1.5 --size 320x180 --out out/video.mp4 >/dev/null
mean() { ffmpeg -v error -i "$1" -vf 'scale=1:1' -f rawvideo -pix_fmt rgb24 - | od -An -tu1 | tr -s ' ' | cut -d' ' -f2; }
r1=$(mean out/stills/t0_5.png); r2=$(mean out/stills/t1_5.png)
[[ "$r2" -gt "$r1" ]] && pass capture-webgl-draws-per-time || bad "capture-webgl-draws-per-time $r1 $r2"
mkdir tpl && cp "$HERE/../assets/page-template.html" tpl/page.html
node "$HERE/capture.mjs" tpl/page.html --stills 0,1 --out tpl/out/v.mp4 >/dev/null
mt0=$(mean tpl/out/stills/t0.png); mt1=$(mean tpl/out/stills/t1.png)
[[ "$mt1" -gt "$mt0" ]] && pass template-fades-in-title || bad "template-fades-in-title $mt0 $mt1"
printf '<!doctype html><script>window.__ready=true</script>' > noseek.html
set +e; node "$HERE/capture.mjs" noseek.html --duration 1 --size 320x180 --out out/x.mp4 >/dev/null 2>&1; rc=$?; set -e
[[ $rc == 1 ]] && pass capture-requires-seek || bad "capture-requires-seek rc=$rc"

ffmpeg -v error -f lavfi -i 'sine=frequency=220:duration=3' -ac 2 music.wav
set +e; python3 "$HERE/finish.py" --video out/video.mp4 --voice tl/voice.wav --music music.wav --subs tl/captions.srt \
  --subs-lang eng --stills 1 --sheet 8 --out final/tally.mp4 > fin.json; rc=$?; set -e
[[ $rc == 0 ]] && pass finish-ok || { bad "finish-ok rc=$rc"; cat fin.json; }
python3 - <<'EOF' && pass finish-report || bad finish-report
import json, os; r = json.load(open('fin.json'))
assert r['ok'] and r['checks']['tv_range'] and r['checks']['subtitle_track'] and os.path.isfile(r['sheet']), r
EOF
ffmpeg -v error -f lavfi -i 'color=c=black:s=320x180:d=1:r=30' -pix_fmt yuvj420p short.mp4
set +e; python3 "$HERE/finish.py" --video short.mp4 --voice tl/voice.wav --sheet 0 --out final/short.mp4 >/dev/null 2>&1; rc=$?; set -e
[[ $rc == 3 ]] && pass finish-refuses-long-voice || bad "finish-refuses-long-voice rc=$rc"
set +e; python3 "$HERE/finish.py" --video short.mp4 --sheet 0 --out final/full.mp4 > full.json; set -e
python3 -c "import json;r=json.load(open('full.json'));assert r['checks']['tv_range']" && pass finish-converts-full-range || bad finish-converts-full-range

echo "failures: $fails"; exit $fails
