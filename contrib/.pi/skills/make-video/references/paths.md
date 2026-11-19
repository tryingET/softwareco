# Video paths on this workstation: facts for routing

Verified 2026-11-04 (AK 8322). Read this when you choose between two paths, plan narration or
captions, or estimate cost. Full analysis: `/data/ai-society-scratch/video-skill-handoff/analysis.md`.

## Contents

1. Path facts
2. Voices and captions
3. Music
4. Delivery pitfalls

## 1. Path facts

| Path | Best at | Real limits | Cost to set up / iterate | Evidence |
|---|---|---|---|---|
| FrankenManim (`contrib/franken_manim`, Rust rewrite of 3b1b manimlib, pre-1.0) | exact school maths in portrait, narration synced to the sample, word captions | only the pinned 2D CPU route with Rust scene programs works; `fmn` is not installed; 3D, TeX fractions and the Python portal are unproven; teachingco's `setup.sh` reports `blocked` although the pinned binary works | high: about 8.7 GiB cache, pinned nightly Rust, multi-GB TTS and Whisper models. A render takes 14-18 s, but a full revision round takes about an hour | 12 published films (1080x1920, 24 fps, 72-145 s) in `~/ai-society/teachingco/media/videos/` |
| Manim CE v0.20.1 (`~/.local/bin/manim`) | quick generic maths and algorithm animations, LaTeX | not allowed for the teachingco school series; the imported skill describes ElevenLabs and manim-voiceover, which are not set up here | low: already installed | no production here; the skill dates from a 2026-08 spike |
| Pillow + ffmpeg (mathe-machraum) | diagrams whose counts must be exact (`geometry-lock.json`), up to two subtitle languages side by side | flat 2D drawing; each topic needs new drawing code; no right-to-left text shaping, so no Arabic; scene-level subtitles; the skill's `tools/render_lesson.py` path is wrong (the script is in `scripts/`) and the inputs it expects are missing from `apps/player/src` | low setup; medium per topic | six player clips (960x540, 12 fps) in `apps/player/media/` |
| HTML captured in Chromium (`scripts/capture.mjs`, from lehrplan-viz Zahlen-Spirale) | anything a browser renders: real fonts, SVG, canvas, WebGL, D3; exact stills for review; a live preview | about 1x real time at 1080p with 8 workers; the original film had no voice and no captions; its source sits in an ignored folder (`lehrplan-viz/.gitignore` ignores `output/`) | low: Node 22, chromium and ffmpeg are installed | `Zahlen-Spirale_Erklaervideo.mp4`, 1920x1080, 30 fps, 180 s |
| Director (`contrib/director`, pre-1.0) | typographic motion, product tours, mock windows; fastest review loop (sheet under 1 s, draft in about 10 s, 39 s master in 14 s) | refuses top-level `@media`, named grid areas, mixed inline/block text, iframes, WebGL, scripts with timers or fetch, unmuted video; missing glyphs render as boxes; silent output | build about 54 s, 2.5 GB target, deleted after each video | `niri-desktop-continuity/docs/announce/niri-desktop-continuity-0.3.1.mp4`, 1920x1080, 39 s |

## 2. Voices and captions

- German school series: the teachingco pipeline with the frozen voice card `steve23-de-v1`
  (Qwen3-TTS through `german-tts-voice-lab`, run through heavy-job).
- Other German or English narration: `~/ai-society/softwareco/owned/german-tts-voice-lab`, one WAV per
  segment, for example `uv run --extra runtime german-tts-voice-lab render --profile
  steve23-purposeful-peaceful-en --language English --text "..." --out audio/s1.wav --json`. The
  profiles are synthetic voices, not real people. Run `doctor` first. The model is several GB: run
  it through heavy-job.
- Piper voices, where they exist, are owned by `mathe-piper-lokal` (mathe-machraum). The piper
  binary is not installed on PATH.
- `espeak-ng` (`/usr/bin/speak` links to it) is for timing drafts only, never for delivery.
- Captions: `timeline.py` makes one cue per segment from the script text and the measured speech
  span, so captions never invent words. Word-level captions need a Whisper alignment. That alignment
  exists only inside teachingco task folders (faster-whisper large-v3-turbo, CPU); there is no
  Whisper CLI on PATH. Ask before setting one up.
- Before delivery, listen to every take at normal speed, or have a person do it. Remake takes that
  drop or garble words.

## 3. Music

Use only music you made or may use: a bed synthesised in code, like lehrplan-viz `music.mjs`, or
a public-domain or licensed track whose licence you record. `finish.py --music-db` sets the bed
level: -18 dB under narration, about -10 dB for a music-led clip. It loops the bed and ducks it
under the voice. For cuts on the beat, place the scene boundaries on beat frames in `timing.json`
before rendering.

## 4. Delivery pitfalls

- Serve MP4s for review with a server that supports byte ranges. `python -m http.server` does not,
  and seeking breaks after about 50 s.
- Director writes full-range `yuvj420p`; `finish.py` converts it. For any other path, finish anyway,
  so every file has the same tags.
- Portrait for phones: 1080x1920. Keep text inside the middle 80 %. Check a still scaled down to
  360 px wide, as a phone shows it.
- To commit a binary to a repository, strip its metadata: `ffmpeg -i in.mp4 -map 0 -c copy
  -map_metadata -1 -fflags +bitexact -movflags +faststart out.mp4`.
