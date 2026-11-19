---
name: x-thread
description: >-
  Plan and draft a post or thread for X (Twitter) for the operator: thread structure, opener,
  media specs, captions, mentions, link placement, timing and the first two hours, based on X's
  open-sourced ranking code. Use when asked to tweet, draft a thread, announce a project or video
  on X, or plan reach on X. Do not use to make the video itself (use make-video / director-video),
  for other networks, or to post: agents never post, like, follow or DM; the operator posts.
compatibility: "No X API here. Reading X (bookmarks, handles, posts) goes through the operator's Grok Bot app 'Jules' via a request file."
metadata:
  owner: "softwareco/contrib lane root"
  version: "0.1.1"
  verified: "2026-11-19 (research only; not yet measured on a posted thread)"
  worked-example: "~/ai-society/softwareco/owned/paradee-bend/docs/announce/x-clips (AK8840)"
---

# X thread

## Outcome
A ready-to-post draft: one file with every post's text (<= 280 characters each, counted),
its media file and .srt, alt text, mentions with their reason, the posting time and the plan
for the first two hours. Every fact in it has a source. The operator posts it himself.

## Boundary
- Agents only draft. Posting, liking, following, DMs and @grok questions are the operator's.
- Reading X: no API on this workstation. Write a request file (what to read/verify, where to
  write the answer, "read only") and give the operator one line to paste into the Grok Bot app
  (his bot is called Jules; it can read his bookmarks and run commands here). Never guess a handle:
  verified by Jules or marked "unverified" (2026-11: @loviscach, @hexgrad, @commonvoice were
  wrong or foreign accounts). Where no real account exists, link GitHub/Hugging Face instead.
- Real name + public servant (e.g. a teacher in Bavaria): private-capacity wording ("privat",
  "ich unterrichte" instead of an official title), no school, no town, no pupils, nothing from
  the job, moderate tone; bio: "Privater Account, Meinungen sind meine eigenen". Sources:
  km.bayern.de Soziale Medien; §§ 33, 37 BeamtStG; Art. 81/82 BayBG if it ever earns money.
- Video comes from make-video/director-video; never upload a capture of a private desktop.

## What the ranker rewards (xai-org/x-algorithm, weights as read 2026-11)
- Per-viewer predicted actions times weights: copy link 20, reply 5, quote 5, DM share 5,
  share 2.1, repost 1, like 0.708 (home-mixer/params/param.rs, commit b551517). A reply between
  mutual follows gets +15. Negative: block -31, not interested -53, mute -59, report -234.
  Live values may differ by feature switch. So: invite replies, never bait or annoy.
- Authors with <= 50k followers: an original post younger than 2 h that a viewer has seen
  < 200 times can be lifted into feed rank 15-16 (one per request, Thompson sampling;
  partly an experiment). A chance at a slot, not a blanket bonus. The operator stays online those 2 hours and
  answers every reply.
- Early follower response decides out-of-network reach. Near-identical posts are spread apart:
  one claim per post, as a thread, not five separate posts.
- No explicit link penalty found, but links lead away: put the link in the last post or the
  first reply, not the opener.

## Workflow
1. Facts first: list every claim with its source file or URL. Numbers only from receipts.
2. Opener: result first ("this is a voice that ...") with the clip attached, then the turn;
   a legal/private disclaimer goes in post 2 or the bio, not the first line. The most curious true claim + one media + an honest question that invites replies.
   No link, no mention, at most one emoji, no hashtag or one.
3. Posts 2..n: one claim, one clip each. Clip text and post text must agree.
4. Last post: method, repo link, credits (projects and people with verified handles), the one
   or two mentions the operator chose, each with a concrete reason.
5. Media: H.264 + AAC MP4, square or 16:9, <= 140 s without Premium, burned-in captions
   (feeds autoplay muted) plus the .srt uploaded in the browser (app cannot), alt text per image.
6. Timing: studies disagree; Tue-Thu morning is the common ground (X publishes nothing). Schedule in the browser
   composer or X Pro. Next day: quote the thread with the best reply.
7. Deliver: `x-thread.md` beside the media, each post with its character count, plus the
   operator's checklist (bio, pin the opener, upload .srt, stay 2 h, reply to all).

## Completion
Report the draft path, the sources table, which handles are verified and by whom, and what the
operator must do himself. Nothing posted.
