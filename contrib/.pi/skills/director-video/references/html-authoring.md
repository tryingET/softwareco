# Writing HTML that Director renders well

Read before writing or fixing a composition. Director's supported subset is in
`~/ai-society/softwareco/contrib/director/crates/director-html/README.md` ("Implemented subset" and
"Remaining incompatibilities"); this file adds what real films ran into.

## Contents

1. Markup Director refuses, and the fix
2. Timing
3. Counters and motion blur
4. Readability on a phone
5. Worked example

## 1. Markup Director refuses, and the fix

- `styled inline boxes require extraction`: an inline element with its own box, such as a `<b>`
  with a margin, padding or background. Make the parent `display:flex` and use block children.
- Bare text beside elements inside a flex container: wrap the text in its own element.
- A glyph missing from the loaded fonts (✳, emoji, rare symbols) falls back to a colour-emoji font
  and renders as a coloured box. Use only glyphs your loaded fonts have.
- No top-level `@media`, named grid areas or mixed inline and block formatting. Use absolute
  positioning, flexbox and plain grid tracks.

## 2. Timing

- The root element sets `data-width`, `data-height`, `data-fps` and `data-duration`; add
  `data-no-timeline` and give each scene `data-start` and `data-duration`.
- CSS animation delays count from the start of the whole composition, also inside a scene with
  `data-start`. Fade a scene in with an `animation-delay` equal to its `data-start`, as
  `examples/html/showreel.html` does.
- Several animations on one element are a comma-separated list, each with its own delay.

## 3. Counters and motion blur

- `data-reel` on a span that holds only text rolls its digits into place;
  `data-reel-start` counts from the scene's start. It works inside a larger line of text.
- `data-motion-blur="4"` on the root smooths motion. A 39-second 1080p film with it rendered in
  14 s on the CPU.

## 4. Readability on a phone

Feeds play video muted on a phone, where a 1080p frame shrinks about five times. Keep meaningful
text at 26 px or more and headlines around 90 px or more, show one idea per scene, and keep the
film around 30 to 45 seconds.

## 5. Worked example

`~/ai-society/softwareco/owned/niri-desktop-continuity/docs/announce/build.py` generates a
seven-scene release film: a desktop of window tiles that fall and fly back, agent cards, a result
page with a rolling counter, and an end card. Its README there is the full render recipe.
