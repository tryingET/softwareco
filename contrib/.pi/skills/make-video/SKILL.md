---
name: make-video
description: Chooses how to make a video on this workstation and carries it from script to a checked MP4. Covers explainers, announcements, product clips, animations, narrated or captioned films and music beds. It picks the renderer (FrankenManim, Manim CE, Pillow, HTML captured in Chromium, Director), times scenes from measured narration, mixes the audio once and checks the result. Use when someone asks to create, plan or produce a video, film, reel or Erklaerfilm, or asks which video tool to use. Do not use to trim, convert or join existing video files (use ffmpeg directly) or to make still images. Once a renderer is chosen, follow its own skill.
compatibility: Linux workstation with ffmpeg/ffprobe, Python 3.11+, Node 22+ and /usr/bin/chromium for the helpers; espeak-ng for the smoke test; a /data scratch volume.
metadata:
  owner: "softwareco/contrib lane root"
  version: "1.0.0"
  verified: "2026-11-04"
  analysis: "/data/ai-society-scratch/video-skill-handoff/analysis.md (AK 8322)"
---

# Make a video

## Outcome

An MP4 that plays on its target, made by a pipeline you can run again. Its timing follows the
measured narration. Its audio is encoded once. You looked at its frames and listened to it before
calling it done.

## Boundary and handoffs

This skill owns three things: choosing the path, the shared timing, audio and delivery contract,
and the HTML-in-Chromium path, which no other skill owns. Once you choose a path, its skill owns the
rendering. Read that skill next and follow its own AGENTS chain.

| The video is | Path | Hand off to |
|---|---|---|
| A German school maths Erklaerfilm (Klasse 1-10), portrait, narrated with the saved voice `steve23-de-v1`, exact maths, word captions | FrankenManim (pinned native build) | `~/ai-society/teachingco/.pi/skills/manim-video` (teachingco). Never Manim CE, never the clone's HEAD. Publication belongs to mathe-machraum. |
| A mathe-machraum place-value or cube lesson with exact counts and several subtitle languages | Pillow + ffmpeg | `~/ai-society/softwareco/owned/mathe-machraum/skills/skills/mathe-video-mehrsprachig`; voices via `mathe-piper-lokal` |
| Any other maths, algorithm or equation animation (not for a school series) | Manim Community v0.20.1 (`~/.local/bin/manim`) | `~/ai-society/softwareco/owned/workstation-capabilities/.pi/skills/manim-video` (Manim CE). Its voiceover plugin and ElevenLabs are not set up here, so use the narration contract below. |
| An announcement, product tour, social clip, title or typographic motion graphic made of layout, text, SVG and CSS/GSAP motion | Director (HTML/CSS to MP4 without a browser) | `~/ai-society/softwareco/contrib/.pi/skills/director-video` |
| Anything that needs a real browser: WebGL/three.js, canvas, iframes, page scripts, markup Director refuses, D3 or excalidraw-animate | HTML frames captured in headless Chromium | this skill: `scripts/capture.mjs` |
| Generated footage: realistic people, avatars, lip-sync, AI video, cloned voices, a terminal recording, a screen capture | none installed | Stop and ask the operator (see below) |

## Not installed: ask first

No path here generates footage, records a terminal or captures a screen. Do not install anything
for that on your own. Offer the operator a multiple choice, your recommendation first:

- Imagination Studio (`~/ai-society/softwareco/contrib/Imagination-Studio-by-keys-Wasserman`): AI
  shots, voices and music. Not installed. It needs about 125-400 GB on /data, its documented 64 GB
  RAM minimum is above this machine's 62 GiB, and its Finish renderer has a licence that limits
  commercial use.
- HyperFrames (heygen-com/hyperframes): a maintained HTML-to-video renderer in Chromium. Not installed.
- charmbracelet/vhs for terminal recordings. Not installed. A mock terminal laid out in Director
  needs nothing new.
- Remotion: its licence may need a company licence (not checked).

A realistic person or a voice that sounds like someone needs that person's consent. Label the video
as AI-generated. Use only fabricated or public content, never a capture of a real desktop or private
data.

## Workflow (every path)

1. **Script first.** Write on-screen text and spoken text per segment. Check facts and numbers
   before any audio exists.
2. **Narration.** Make one WAV per segment, using the voice route in
   [references/paths.md](references/paths.md#voices-and-captions). `espeak-ng` is for timing drafts only.
3. **Timing from measured audio.** Run [scripts/timeline.py](scripts/timeline.py) on a
   `segments.json` into a `build/` folder. It writes
   `voice.wav`, `timing.json` and `captions.srt`. Each segment lasts 0.25 s lead + measured WAV +
   0.65 s tail, rounded up to whole frames. Build each scene to the start and end frames in
   `timing.json`. Never type durations by hand in two places.
4. **Render silent video** on the chosen path, at the fps written in `timing.json`. Review the
   cheapest view first: contact sheet, then stills at the key moments, then a draft, then the master.
5. **Finish once.** Run `scripts/finish.py --video silent.mp4 --voice build/voice.wav [--music bed.wav]
   [--subs build/captions.srt --subs-lang deu] --stills <key seconds> --out final/name.mp4`. In one pass
   it ducks the music under the voice, normalises to -16 LUFS, encodes AAC once and fixes Director's
   full range to tv range. It also adds faststart and a soft subtitle track, then writes
   `review/sheet.png` and the stills. It refuses audio longer than the video (exit 3): lengthen the
   visuals, never cut the voice. Never use `-shortest` and never join per-scene AAC with `-c copy`.
6. **Verify.** Look at the sheet and every still you asked for. Listen at normal speed. Read the
   report's `checks`: every check must be true, or you report which one failed.

Keep the work folder, browser temp and caches on /data (`TMPDIR=/data/...`). Builds over a minute
or over a GB go through `AI_SOCIETY_SCRATCH_ROOT=/data/ai-society-scratch heavy-job run --label <l>
--task <AK id> -- ...`. Delete what you built when the video is done. Do not edit upstream clones in
contrib.

## Chromium path (owned here)

Start from [assets/page-template.html](assets/page-template.html). The page contract and the
commands are in the header of `scripts/capture.mjs`. Then finish and verify as in steps 5 and 6.

## Completion

Report the MP4 path, the `finish.py` report (size, duration, checks, LUFS), the frames you looked at,
what you listened to, the path you chose and why, and what you deleted. Uploading, posting or
publishing is the operator's decision, and so is installing a new tool.

## Helpers

[scripts/timeline.py](scripts/timeline.py), [scripts/finish.py](scripts/finish.py) and
[scripts/capture.mjs](scripts/capture.mjs) document their usage in their header. They refuse to
overwrite their output unless you pass `--force`. [tests/smoke.sh](tests/smoke.sh) runs all three
on fabricated content. Run it after changing a helper, with `TMPDIR` on /data.
