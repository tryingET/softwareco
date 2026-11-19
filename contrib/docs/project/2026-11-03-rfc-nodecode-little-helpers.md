---
summary: "RFC: the generic shell and engine hooks Nodecode needs so that a cell, nodecode-little-helpers, can provide /sidequest, /btw, stash and code-block copy."
status: proposed
read_when:
  - "Before building /sidequest, /btw, stash or code-block copy for Nodecode."
  - "Before proposing a new cell hook to upstream nodecode-ai/nodecode."
owner: softwareco/contrib (Nodecode)
ak_task: 8224
based_on: "nodecode-ai/nodecode main 153e5b7; pi-extensions packages/pi-little-helpers"
---

# RFC: Nodecode hooks for little-helpers

## 1. What the operator wants

One Nodecode cell, `nodecode-little-helpers`, does for Nodecode what
`pi-little-helpers` does for Pi. It starts with four helpers:

| Helper | What the person does | What happens |
|---|---|---|
| `/sidequest TEXT` | asks for a branch of this conversation | The session is forked at its head. The child has its own id and shows under its parent in the sessions tree. It opens in a new Ghostty tab with TEXT as its first prompt, and this shell stays where it is. |
| `/btw QUESTION` | asks a side question | The answer comes from a copy of the conversation. The side turn may read files but may not change anything. The running turn goes on, and nothing is added to the session. |
| stash (`/stash`, keys) | sets the draft aside and brings it back | Saves the input box text, clears the box, and restores the text later, in any session. |
| `/codeblocks` (key) | wants a code block from the answer | Picks a fenced block from the conversation and copies it to the clipboard. |

More helpers will follow, so the hooks must be general, not one per helper.

## 2. Where Nodecode stands (upstream main 153e5b7)

Nodecode runs as two processes. The **gateway**, a systemd service on this
machine, holds the organism: sessions, turns, cells. The **shell**, the TUI
in a terminal, holds the screen, the keys, the input box and the clipboard. A
cell's slash command runs in the gateway. The shell sends `POST
/api/gateway/slash {line, session_id}` and shows what comes back
(`src/tui/commands/cell-control.lisp:25-30`, `src/gateway/gateway.lisp:2861`).

What a cell can already do:

- **A slash command.** `(:command NAME RUN)` runs `(RUN args session-id)` and
  answers `(values TEXT DIALOG)` (`gateway.lisp:3276-3316`).
- **A picker.** DIALOG is a `list-dialog` with rows, search and tabs
  (`gateway.lisp:3167-3192`). A row's `:run (:enter LINE)` sends LINE back as
  a slash command. A row's `:value` is inserted into the input box at the
  cursor (`cell-control.lisp:113-152`).
- **Tools, hooks, routes, help** (`src/organism/cell-dsl.lisp:128-224`,
  `docs/cell-api.mdx:154-161`).
- **Fork without switching**, through HTTP only. `POST /api/gateway/sessions
  {session_id, parent}` creates a fork at the parent's head
  (`gateway.lisp:3543`). `/fork` adds the switch on the client side
  (`src/client/client-session.lisp:1554-1580`). The agent's `(fork ...)` does
  the same in Lisp with `create-session :parent :anchor-turn-id` and
  `nle:submit` (`src/organism/fork.lisp:238-262`). Parents are stored in
  `session_directory.parent`, and the sessions picker draws them as a tree
  (`gateway.lisp:3410-3422`).
- **Steer and stop a fork** from the parent's shell (#194), and ask the
  person a question and wait for the answer (#185, `src/gateway/questions.lisp:89`).
- **Resume with a prompt.** `nodecode resume SESSION-ID -- PROMPT` resumes a
  session and sends PROMPT in it (`src/cli/entry.lisp:401`).

What a cell cannot do:

| Gap | Why |
|---|---|
| Own a key | Keys come from the fixed `*keybind-actions*` (`src/tui/keys.lisp:199-252`). `keybinds.json` can only move those actions to other keys. Each action has its own hard-coded branch in `src/tui/frame.lisp:120-175`. |
| Read or replace the input box | The draft lives only in the shell (`chat-model-editor`, `src/tui/composer.lisp:81`). No frame or route carries it to the gateway. A picked row can only insert at the cursor. |
| Copy to the clipboard | Copying happens in the shell (`nlt:write-clipboard`: wl-copy, xclip or xsel, else OSC 52, `src/term/terminal.lisp:588-644`). A cell runs in the gateway, which has no terminal. |
| Open a terminal tab | The gateway is a service with no Ghostty surface. Only the shell knows its terminal (`TERM_PROGRAM`, `GHOSTTY_SURFACE_ID`). |
| Run a side turn that may only read | There is one global tool table (`*tools*`, `src/engine/turn.lisp:483`). It offers `eval`, which can do anything (`src/engine/exec.lisp:2616`). There is no read-only tool, and every turn is stored. `complete` has no tools by contract (`src/engine/provider.lisp:3187`). |
| Read a session's messages | There is no documented reader for cells. Code fences are recognised only while drawing (`src/tui/transcript/markdown.lisp:18-32`). |
| Show a result later, outside the model's context | A cell's notices are also shown to the model. Nothing shows text to the person alone after the command has returned. |

## 3. Design principle

The shell gains a small set of **effects** that a gateway answer may ask for.
The engine gains a few **verbs** for cells. Each is generic, has no Ghostty
or helper names in it, and is ignored by a shell that does not know it. Every
helper is then a cell made of ordinary slash commands. A key is only a
shortcut for a slash line. Effects that only the shell process can carry out
(keys, the draft, the clipboard, terminals) happen in the shell. Policy stays
in the cell.

## 4. Proposed changes to Nodecode

Each item below is one upstream PR with its own tests and docs.

### H1. Effects in the slash answer, run by the shell

The slash answer (and a picker row) may carry an `effects` list. The shell
runs it in order:

| Effect | Shell action | Used by |
|---|---|---|
| `{"draft": {"set": TEXT}}` / `{"insert": TEXT}` / `{"append": TEXT}` | replace, insert at the cursor, or append to the input box (next to `editor-insert`, `cell-control.lisp:119`) | stash restore |
| `{"clipboard": TEXT}` | `nlt:write-clipboard` (as `src/tui/mouse.lisp:886` does), with a notice that names the route taken | codeblocks |
| `{"open_session": {"session_id": ID, "prompt": TEXT}}` | open ID in a new terminal through the H4 setting | sidequest |

In Lisp, RUN may answer a third value, `(values TEXT DIALOG EFFECTS)`, and a
`list-dialog` row may take `:effects`. Existing commands are unchanged.

### H2. A command may receive the draft

`(:command NAME RUN :draft t)`. For such a command the shell adds `draft:
TEXT` to `POST /api/gateway/slash`, and RUN receives `(args session-id
&key draft)`. Only commands that ask for the draft get it, so a draft is not
sent anywhere it is not needed. Stash uses it to save the draft, then sends
`{"draft": {"set": ""}}` to clear the box.

### H3. Cell key bindings

A new clause, `(:key ACTION LABEL DEFAULT-KEYS LINE)`, adds a row to the
shell's key action list. An action with no built-in branch runs its slash
LINE through the H2 path, as if the person had typed it. `keybinds.json`
moves or turns off such a key like any other, and `/help` lists it. The key
goes away when the cell stops. A key that collides with a built-in one loses
to it, and `/cells` reports the collision. The shell learns these keys from
the slash catalog it already fetches (`GET /api/gateway/slash`,
`cell-control.lisp:14-23`) and refreshes its keymap
(`refresh-model-keymap`, `composer.lisp:71-80`).

### H4. Open a session in a new terminal

A new shell setting, `shell.open_session_command`, is an argv template such
as `["ghostty", "+new-tab", "-e", "{nodecode}", "resume", "{session_id}",
"--", "{prompt}"]`, filled in without a shell, so that no quoting is needed.
The default is unset. The effect then says that no terminal command is
configured, and it names the line to run by hand (`nodecode resume ID --
PROMPT`). The shell starts the command detached, in its own working folder,
with its own environment. That environment carries no `NODECODE_SESSION_ID`,
which only tool children get (AK8201). Upstream stays free of Ghostty. Our
cell supplies the Ghostty template, with a new window as fallback, following
the contract of `pi-little-helpers` `sidequestGhostty*.ts`.

### H5. Engine verbs for cells

- `nle:fork-session SESSION &key prompt title kind → CHILD-ID` wraps
  `create-session :parent :anchor-turn-id` and `nle:submit`, as
  `fork-start` does (`fork.lisp:244-258`). Without a prompt the child stays a
  standby id, so a sidequest always passes TEXT. `kind` is recorded on the
  child (`:sidequest`, `:side`) so that the tree can mark it and gc can find
  it.
- `nle:session-messages SESSION &key since → list` is a documented, read-only
  view of the role and text of each block. The fence reader moves from
  `src/tui/transcript/markdown.lisp` to a shared library file, so that the
  gateway can list code blocks too.
- `nle:tell-shell SESSION TEXT &key title` pushes a dismissible panel to the
  shells that follow SESSION. It is a new projection event kind, the frames
  the gateway already streams to shells (`encode-projection-event`,
  `src/gateway/protocol.lisp:526-535`, kinds admitted by `projection-kind`,
  `:352`). `client_command` frames run the other way, from shell to gateway. The text never enters the
  model's context. /btw answers through it.

### H6. Side turns with a restricted tool set

- `nle:submit` gains `:tools LIST`. The turn offers only those tools. The
  per-turn snapshot already takes a list (`snapshot-context-request
  :tool-bindings`, `turn.lisp:3984-4014`), so this only passes it through.
- `register-tool` gains `:offered nil`: a tool is registered but offered only
  to a turn that names it. The core ships three read-only tools this way:
  `read_file`, `list_dir` and `grep`. They are bounded in size, never write,
  and have no `eval`.
- A side turn is a fork of kind `:side`, submitted with those tools. When it
  answers, the cell shows the answer through `tell-shell` and deletes the
  child with the existing `delete-gateway-sessions` path
  (`gateway.lisp:3462`). Running as a fork reuses everything forks already
  have: concurrency with the main turn, steer, stop and progress rows. We
  chose "delete after" over a new "record nothing" mode because it adds no
  second turn loop. The cost is that the side answer is stored for its
  lifetime, which is a matter of seconds.

## 5. The cell `nodecode-little-helpers`

| Helper | Built from |
|---|---|
| `/sidequest TEXT` | `fork-session` (kind `:sidequest`, prompt TEXT), then the `open_session` effect. The child shows in the sessions tree under its parent, and its tools see its own `NODECODE_SESSION_ID`. |
| `/btw QUESTION` | `fork-session` (kind `:side`, `:tools` read-only), then `tell-shell` with the answer, then delete. It answers "started" at once, and the panel follows. Esc in the panel stops it (#194). |
| `/stash` (key Ctrl+X), `/stash pop` (Alt+X), `/stash list` (Ctrl+Shift+X) | H2 draft in, an H1 `draft` effect out, a `list-dialog` of saved drafts. Storage is `$NODECODE_HOME/little-helpers/stash.sexp` (read with `*read-eval*` off), shared across sessions, as Pi's is. |
| `/codeblocks` (key Ctrl+Shift+Y) | `session-messages` and the shared fence reader, a `list-dialog` with one row per block, Enter running the H1 `clipboard` effect. |

The cell lives in `softwareco/owned/nodecode-cells`, at
`cells/nodecode-little-helpers/` (operator decision, 2026-11-03; it follows
the doorbell cell's layout: a host-free `core`, a `native` host adapter, and
tests wired into the repo's `just check` and `just test`). It is built and
tested in an isolated home (`--ephemeral` or `--store` under
`/data/agnt/tmp`) before the operator installs it.

**What it does before any hook lands** (installed Nodecode, no new hook):

- `/sidequest TEXT` makes the fork the way the agent's own `fork` does
  (`nlk:create-session` at the parent's head, then `nle:submit` with TEXT,
  source `sidequest`). It then opens a new Ghostty **tab** beside the attached
  shell, as Pi does: the shell's `GHOSTTY_SURFACE_ID` and its Ghostty process's
  bus name take Ghostty's `new-tab` D-Bus action, running `nodecode resume
  FORK-ID` through Pi's `/bin/sh -lc` scaffold. With no attached Ghostty shell
  it spawns a window through niri. Only a shell on another machine needs H1
  `open_session`.
- `/codeblocks` lists the fenced blocks of the newest answer. Enter inserts
  the block into the input box through the row's `value`, and Space runs
  `/codeblocks copy N`. That copy is made in the gateway with `wl-copy`, so
  it works only where the gateway shares the person's desktop. A remote shell
  waits for H1 `clipboard`.
- `/btw` waits for P4 (turn tool limits). The stash keys wait for P2 and P3.
  The stash store (a JSON file under the home) is built and tested now.

## 6. Sequence and channel

1. **Upstream issue first.** Upstream merged #95 but closed #4, #5, #7, #9
   and #11 without merging them. So we file one issue with section 4 as a
   proposal and ask which hooks the maintainer wants, and in what shape,
   before writing the PRs. The upstream note says a feature request without a
   patch is filed as an issue.
2. **PRs in order of value per line:** H1+H2 (stash, codeblocks), then H5
   (`fork-session`, `session-messages`, `tell-shell`), then H4, H3 and H6.
   Each comes with tests that fail first, `just test` against a baseline,
   `just docs-check`, and a live proof on an isolated instance.
3. **The cell** is built against a local build carrying the PR branches, and
   tested in an isolated home.
4. **Interim:** until upstream merges, the hooks can run only from a local
   build (the `local` branch of the branch model). The installed Nodecode is
   upstream's release and is not changed by this work.

## 7. Alternatives considered

- **Advise TUI functions from a cell** (`nle:hook` around
  `frame.lisp`/`editor-*`). Rejected. A cell's command runs in the gateway
  (`gateway.lisp:3304-3311`). The shell's launch path also boots the cell
  folder (`src/cli/entry.lisp:921`), but nothing documented promises a
  cell's code runs in the shell process. Advice on internal TUI functions
  would also break with each upstream refactor.
- **Let the gateway open the terminal.** Rejected: a systemd service has no
  Ghostty surface or desktop session to aim at, and the tab must open beside
  the person's own shell.
- **/btw through `complete`.** Rejected: it has no tools by contract, and the
  operator wants /btw to read files.
- **A "record nothing" turn mode.** Deferred: it would need a second turn
  path. A deleted side fork gives the same result with existing code.
- **Helpers in Nodecode core.** Rejected: they are our policy (Ghostty,
  stash keys). Upstream gets only the generic hooks.

## 8. Risks

- **Upstream may decline or reshape the hooks.** The issue in step 1 asks
  first, and each hook is small enough to rework.
- **The draft leaves the shell only when asked.** H2 sends it only to
  commands that declare `:draft t`, and only to this machine's gateway, over
  the token-guarded route.
- **`open_session` starts a process from an answer.** It runs only the
  person's own configured template, filled with an id and a prompt, never an
  argv sent by the gateway.
- **Key collisions.** A built-in key always wins over a cell key, and the
  collision is reported.
- **Side forks left behind** if the gateway dies mid-answer. They are kind
  `:side`, and gc removes them.

## 9. Open questions for the operator

1. ~~Which repo holds the cell?~~ Decided 2026-11-03 by the operator:
   `softwareco/owned/nodecode-cells/cells/nodecode-little-helpers` (see
   section 5).
2. Should the upstream issue in step 6.1 be filed before any code (recommended),
   or should a local build be prototyped first?

## 10. Adjudication (many-of-the-greats, 2026-11-03)

Section 4 lists six hooks shaped by four helpers. Judged against the long
term, it is close but not optimal. It has too many surfaces, it is tied to one
front end, and one primitive is under-named.

**Facts that decide it:**

- **Nodecode has four front ends, not one:** the TUI shell, the web page the
  gateway serves (`docs/gateway.mdx:80`), channels on Discord, Telegram and
  Slack (`docs/channels.mdx`), and `nodecode rpc` (`docs/rpc.mdx`). Anything
  defined as "the shell does X" leaves three of them out.
- **The real catalogue is pi-little-helpers' 15 helpers,** not four. Among
  them: html-output-browser, fresh-handoff, scoutpeer, parallelquest,
  visible-loop and session-closeout.
- **Upstream takes outside PRs, issue first** (operator, from the maintainer,
  2026-11-03). Every surface we add is still one the maintainer must want to keep,
  so each PR stays small and links the issue.

**Schools weighed:**

- **Emacs malleability:** one hook, shell-side Lisp, everything reachable.
- **Elm and effects as data:** commands answer data, and each front end
  interprets it.
- **Object capabilities (Miller):** authority is granted explicitly and
  narrowly.
- **Mechanism, not policy (Unix, Lampson):** few orthogonal primitives.
- **Accretion (Hickey):** add, never change; open maps; ignore unknown keys.
- **Maintainer economics (Gabriel, Hyrum's law):** every surface becomes a
  contract.

**Decision: contextual dominance.**

- **The front-end boundary:** effects as data dominates Emacs malleability,
  because only data crosses four front ends, a process boundary and an
  upstream review.
- **Authority:** object capabilities dominate. A command declares what it
  reads, a turn is given the tools it may use, and the operator owns every
  process launch.
- **The count:** mechanism-not-policy cuts six hooks to four primitives and
  some documentation.

Emacs keeps one true point: the person's own shell may later run
operator-trusted Lisp. That belongs to a local build, not to the upstream
contract.

**Revised primitive set (replaces H1 to H6):**

| | Primitive | Absorbs | Degrades to |
|---|---|---|---|
| P1 | **Front-end effects.** An open set of data that a command answer or a picker row may carry: `draft {set,insert,append}`, `clipboard TEXT`, `open {session [prompt] \| url \| file}`, `show {title text}` (seen by the person only, and also pushable later as a projection event). | H1, H4 (the TUI implements `open session` through the operator's terminal template), H5 `tell-shell` | Text: a front end that lacks an effect shows the text fallback the effect carries ("run: nodecode resume ID -- PROMPT", "copy: ..."). |
| P2 | **Declared reads.** `(:command ... :reads (:draft :selection))`. The front end sends only what the command declared. | H2 | The front end has no draft, so the command gets none. |
| P3 | **Bindings.** An input gesture runs a slash line. A cell proposes defaults, and the person's binding file wins. | H3 | The slash command typed by hand. |
| P4 | **Turn capability.** `nle:submit :tools`, a registered but unoffered read-only set (`read_file`, `list_dir`, `grep`), and a session `kind`. | H6 | None needed: this is engine-side. |
| — | **Documented verbs over existing machinery:** `fork-session` / `new-session` (`:cwd`, `:kind`, `:prompt`), `session-messages`, `await-session`. | H5 | No new mechanism, only an exported contract. |

**Coverage check against the Pi catalogue:**

| Helper | Built from |
|---|---|
| stash | P1 draft, P2, P3 |
| codeblocks | P1 clipboard, session-messages, P3 |
| sidequest | fork-session, P1 open session |
| /btw | fork-session, P4 read-only, P1 show |
| fresh-handoff | new-session with a generated prompt, P1 open |
| scoutpeer | new-session, P4 read-only, P1 open |
| parallelquest | new-session `:cwd` worktree, P1 open |
| visible-loop, nexus-loop | new-session, await-session, P1 open |
| html-output-browser | the existing `:hook :tool`, P1 open url/file |
| session-closeout, limits, resets, update-notify | existing commands, dialogs, ask-operator, notices |

No helper needs a fifth primitive. P4 earns the most: it also makes
scoutpeer's "read-only" a real limit rather than a prompt contract.

**Process consequence:** the upstream issue states the needs and this
coverage table. It proposes P1 to P4 as one candidate shape, not as finished
hooks, and asks the maintainer to choose. The first PR is P1, with `draft`
and `clipboard` only.
