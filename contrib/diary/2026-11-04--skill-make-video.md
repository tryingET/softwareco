# 2026-11-04: make-video skill (AK 8322)

nodecode session s-1LW2Z74E, handed over from the niri-desktop-continuity Claude Code session.

- Built `.pi/skills/make-video`. It routes video work to five paths: FrankenManim through
  teachingco `manim-video`, Manim CE through workstation-capabilities `manim-video`, Pillow through
  mathe-machraum, Director through `director-video`, and Chromium capture, which this skill owns.
  Generated footage, terminal recordings and screen captures have no installed tool, so they go to
  the operator as a question.
- The helpers cover what every path lacked:
  - `timeline.py`: scene timing from the measured narration WAVs.
  - `finish.py`: one audio pass with ducking, -16 LUFS, a single AAC encode, tv range, soft
    subtitles, then review stills and a contact sheet.
  - `capture.mjs`: generalises the lehrplan-viz Zahlen-Spirale `render.mjs`; WebGL runs through
    SwiftShader.
- Learned:
  - Two different skills are named `manim-video`: teachingco's FrankenManim skill and
    workstation-capabilities' Manim CE skill. Renaming one is that owner's choice.
  - `director-video`'s handoff bullet was the measurable part: without it, a session that loads
    only Director finished the music by hand.
  - Regexes written in advance under-match correct answers given in other words ("Kein Manim CE").
    When a check is broadened, apply it to both arms and record why.
- Evidence: `/data/ai-society-scratch/video-skill-handoff/` (analysis.md, evals/).
