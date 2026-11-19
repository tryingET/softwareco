---
name: director-video
description: Make an animated video (release announcement, product tour, social clip for X, YouTube or LinkedIn, demo reel, motion graphic) on this workstation with Director, the HTML/CSS-to-MP4 renderer cloned at ~/ai-society/softwareco/contrib/director. Builds it, writes a composition, reviews it with check, sheet, still and draft renders, and exports an upload-ready MP4. Use when asked to create, render or iterate on a video, reel or announcement video made of layout, text and CSS motion. When the tool is not chosen yet, or the video needs WebGL, a browser, narration or captions, use make-video first. Do not use for trimming, converting or joining existing video files (use ffmpeg directly), for screen recordings, or for still images and charts.
compatibility: Linux workstation with cargo, clang, the FFmpeg development libraries, ffmpeg and ffprobe, and a /data scratch volume.
metadata:
  owner: "softwareco/contrib lane root"
  verified: "2026-11-04"
  worked-example: "~/ai-society/softwareco/owned/niri-desktop-continuity/docs/announce"
---

# Director video

## Outcome

An MP4 that plays on its target platform, rendered from an HTML/CSS composition that can be
rendered again, and reviewed frame by frame before the final render.

## Boundary

- Director is an upstream clone (stepupgaming/director) at `~/ai-society/softwareco/contrib/director`.
  Use it; do not edit it. A fix for Director goes upstream through `softwareco-contrib-upstream`.
- Director's own skills in `.agent/skills/` cover narrower jobs: `director-agent-loop` (the CLI
  review loop), `director-mcp` (the MCP server), `director-rhai` (Rhai scripts). This skill adds the
  workstation recipe and what real films taught.
- `make-video` (same folder) chooses between Director and the other video paths, and owns narration
  timing (`timeline.py`) and the audio and delivery pass (`finish.py`). Render the silent film here,
  then finish it there.
- Director's root AGENTS.md holds its upstream maintainer's Windows preferences (C: and F: paths,
  NVENC, Grok subagents). They do not apply on this workstation.

## Build

Build once per video through the heavy-job runner, with the target on /data:

```bash
cd ~/ai-society/softwareco/contrib/director
AI_SOCIETY_SCRATCH_ROOT=/data/ai-society-scratch heavy-job run --label director-build --task <AK id> -- \
  env CARGO_TARGET_DIR=/data/agnt/cache/cargo-target/director \
  cargo build --release -p director-cli --bin director-engine
E=/data/agnt/cache/cargo-target/director/release/director-engine
```

On 2026-11-04 this took 54 s and left a 2.5 GB target, with FFmpeg 9 and clang 23. Delete the
target when the video is done; rebuilding is cheap.

## Workflow

1. Work in a scratch folder on /data. Generate the HTML from a small script, so repeated markup
   stays consistent and the film can be rendered again. Use fabricated or public content only,
   never a capture of a real desktop or private data.
2. Copy the fonts you use beside the HTML and load them with `@font-face`. Bundled:
   `crates/director-core/assets/fonts/` (Inter, Roboto, Archivo, JetBrains Mono, Poppins) and
   `examples/assets/fonts/` (Instrument Serif, Archivo widths, JetBrains Mono).
3. Before writing markup, read [references/html-authoring.md](references/html-authoring.md): the
   markup Director refuses, how timing works, and what stays readable on a phone.
4. Review fastest first, and look at every image you make:
   `$E html check film.html` (compiles; names unsupported markup) →
   `$E check film.html --every 0.25 --safe-zone twitter` →
   `$E sheet film.html -n 16 -c 4 --cell-width 480 -o sheet.png` (under 1 s) →
   `$E still film.html -t <seconds> -o still.png` at the key moments →
   `$E render film.html --scale 0.5 --draft-encode -o draft.mp4` (about 10 s) →
   `$E render film.html -o master.mp4`.
5. Export for upload. Director writes full-range `yuvj420p`; convert it to standard range with
   fast start, then confirm codec, `pix_fmt=yuv420p`, `color_range=tv`, size and duration:

   ```bash
   ffmpeg -i master.mp4 -vf "scale=in_range=full:out_range=tv,format=yuv420p" \
     -c:v libx264 -profile:v high -preset slow -crf 16 -movflags +faststart -an out.mp4
   ffprobe -v error -show_entries stream=codec_name,pix_fmt,color_range,width,height \
     -show_entries format=duration,size -of compact out.mp4
   ```

   To commit the video to a repository that checks binaries, also drop its metadata:
   `ffmpeg -i out.mp4 -map 0:v -c copy -map_metadata -1 -fflags +bitexact -flags:v +bitexact -movflags +faststart final.mp4`.

## Known false alarm

`check` reports the digit strips of a `data-reel` counter as `off_canvas` errors and `clipped`
warnings, because it measures them without their scroll track. Check the counter with a still
after it lands instead.

## Completion

Report the MP4 path, its ffprobe line, the frames you looked at, and each finding you accepted
with its reason. Delete the Director target and scratch you made. Posting the video anywhere is the
user's decision.
