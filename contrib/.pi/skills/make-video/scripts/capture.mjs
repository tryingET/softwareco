// Capture an HTML page frame by frame in headless Chromium (CDP) and encode a silent H.264 video.
// No npm packages: Node 22+ (global WebSocket and fetch), Chromium, ffmpeg.
//
//   node capture.mjs PAGE.html --duration 20 [--fps 30] [--size 1920x1080] [--out out/video.mp4]
//                    [--workers 8] [--stills 1.5,10] [--chromium /usr/bin/chromium] [--force]
//
// Page contract: the page sets window.__ready = true when fonts and assets are loaded, and
// window.seek(seconds) draws exactly the frame for that time (it may return a promise). Every frame
// must be a pure function of time: no Date.now(), performance.now(), timers or requestAnimationFrame
// driving state while rendering. The page gets ?render=1 so it can hide preview controls.
// WebGL works through SwiftShader (CPU); create the context with preserveDrawingBuffer: true.
// Temporary browser profiles go to $TMPDIR, or beside --out when TMPDIR is unset or under /tmp.
// --stills writes PNGs beside --out (stills/) and renders no video.
import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const argv = process.argv.slice(2);
const opt = (name, dflt) => { const i = argv.indexOf(`--${name}`); return i >= 0 ? argv[i + 1] : dflt; };
const die = (msg, code = 2) => { console.error(`capture.mjs: ${msg}`); process.exit(code); };
const page = argv[0] && !argv[0].startsWith('--') ? resolve(argv[0]) : die('first argument must be the HTML page');
if (!existsSync(page)) die(`no such page: ${page}`);
const FPS = Number(opt('fps', 30));
const DUR = Number(opt('duration', NaN));
const [W, H] = opt('size', '1920x1080').split('x').map(Number);
const OUT = resolve(opt('out', 'out/video.mp4'));
const WORKERS = Math.max(1, Number(opt('workers', 8)));
const CHROMIUM = opt('chromium', process.env.CHROMIUM || '/usr/bin/chromium');
const STILLS = opt('stills', null);
if (!(FPS > 0) || !(W > 0) || !(H > 0) || W % 2 || H % 2) die('need --fps > 0 and an even --size WxH');
if (!STILLS && !(DUR > 0)) die('need --duration SECONDS');
if (!STILLS && existsSync(OUT) && !argv.includes('--force')) die(`${OUT} exists; pass --force to replace it`);
const TMP = process.env.TMPDIR && !process.env.TMPDIR.startsWith('/tmp') ? process.env.TMPDIR : join(dirname(OUT), '.capture-tmp');
const pause = ms => new Promise(r => setTimeout(r, ms));

class CDP {
  constructor(ws) {
    this.ws = ws; this.id = 0; this.pending = new Map();
    ws.addEventListener('message', ({ data }) => {
      const m = JSON.parse(data); const p = m.id && this.pending.get(m.id); if (!p) return;
      this.pending.delete(m.id); if (m.error) p.reject(new Error(JSON.stringify(m.error))); else p.resolve(m.result);
    });
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((res, rej) => { this.pending.set(id, { resolve: res, reject: rej }); this.ws.send(JSON.stringify({ id, method, params })); });
  }
  async evaluate(expression) {
    const r = await this.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    return r.result.value;
  }
}

async function launch() {
  await mkdir(TMP, { recursive: true });
  const profile = await mkdtemp(join(TMP, 'capture-'));
  const proc = spawn(CHROMIUM, ['--headless=new', `--user-data-dir=${profile}`, '--remote-debugging-port=0',
    '--no-first-run', '--no-default-browser-check', '--disable-background-networking', '--disable-component-update',
    '--hide-scrollbars', '--force-color-profile=srgb', '--force-device-scale-factor=1', `--window-size=${W},${H}`,
    '--disable-dev-shm-usage', '--allow-file-access-from-files', '--enable-unsafe-swiftshader', '--use-angle=swiftshader',
    '--mute-audio', 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
  let stderr = ''; proc.stderr.on('data', d => { stderr += d; });
  let port;
  for (let i = 0; i < 300 && !port; i++) {
    if (proc.exitCode != null) throw new Error(`chromium exited: ${stderr.slice(-2000)}`);
    try { port = Number((await readFile(join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]); } catch { await pause(50); }
  }
  if (!port) throw new Error('chromium did not open a debugging port');
  const close = async () => {
    if (proc.exitCode === null) { proc.kill('SIGTERM'); await new Promise(r => proc.once('exit', r)); }
    await rm(profile, { recursive: true, force: true, maxRetries: 10, retryDelay: 100 });
  };
  try {
    const targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
    const ws = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl);
    await new Promise((r, j) => { ws.addEventListener('open', r, { once: true }); ws.addEventListener('error', j, { once: true }); });
    const cdp = new CDP(ws);
    await cdp.send('Page.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });
    await cdp.send('Page.navigate', { url: pathToFileURL(page).href + '?render=1' });
    let ready = false;
    for (let i = 0; i < 400 && !ready; i++) { ready = await cdp.evaluate('window.__ready === true').catch(() => false); if (!ready) await pause(50); }
    if (!ready) throw new Error('page never set window.__ready = true');
    if (!(await cdp.evaluate('typeof window.seek === "function"'))) throw new Error('page defines no window.seek(seconds)');
    return { cdp, close: async () => { try { ws.close(); } catch { /* gone */ } await close(); } };
  } catch (e) { await close(); throw e; }
}

async function shot(cdp, f) {
  await cdp.evaluate(`Promise.resolve(window.seek(${f / FPS})).then(() => new Promise(r => requestAnimationFrame(() => r(document.body.offsetHeight))))`);
  const { data } = await cdp.send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: W, height: H, scale: 1 } });
  return Buffer.from(data, 'base64');
}

function run(cmd, args) {
  const p = spawn(cmd, args, { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => { p.once('error', rej); p.once('exit', c => (c === 0 ? res() : rej(new Error(`${cmd} exited ${c}`)))); });
  return { p, done };
}

async function segment(id, from, to, dir, tick) {
  const { cdp, close } = await launch();
  const out = join(dir, `seg${String(id).padStart(3, '0')}.mp4`);
  const ff = run('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-tune', 'animation', '-pix_fmt', 'yuv420p', '-color_range', 'tv',
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-g', String(FPS * 2), '-r', String(FPS), out]);
  try {
    for (let f = from; f < to; f++) {
      const png = await shot(cdp, f);
      if (!ff.p.stdin.write(png)) await new Promise(r => ff.p.stdin.once('drain', r));
      tick();
    }
  } finally { ff.p.stdin.end(); await close(); }
  await ff.done;
  return out;
}

async function stills(list) {
  const dir = join(dirname(OUT), 'stills'); await mkdir(dir, { recursive: true });
  const { cdp, close } = await launch();
  try {
    for (const s of list) {
      const p = join(dir, `t${String(s).replace('.', '_')}.png`);
      await writeFile(p, await shot(cdp, Math.round(Number(s) * FPS))); console.log(p);
    }
  } finally { await close(); }
}

async function full() {
  const total = Math.round(FPS * DUR), workers = Math.min(WORKERS, total);
  await mkdir(dirname(OUT), { recursive: true }); await mkdir(TMP, { recursive: true });
  const segDir = await mkdtemp(join(TMP, 'segments-'));
  const per = Math.ceil(total / workers); let done = 0; const t0 = Date.now();
  const tick = () => { if (++done % 300 === 0) console.error(`${done}/${total} frames, ${((Date.now() - t0) / 1000).toFixed(0)} s`); };
  try {
    const segs = await Promise.all(Array.from({ length: workers }, (_, i) => [i * per, Math.min(total, (i + 1) * per)])
      .filter(([a, b]) => a < b).map(([a, b], i) => segment(i, a, b, segDir, tick)));
    const list = join(segDir, 'list.txt');
    await writeFile(list, segs.map(s => `file '${s}'`).join('\n'));
    await run('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', '-an', '-movflags', '+faststart', OUT]).done;
    console.log(JSON.stringify({ out: OUT, frames: total, fps: FPS, width: W, height: H, seconds: (Date.now() - t0) / 1000 }));
  } finally { await rm(segDir, { recursive: true, force: true }); }
}

try { if (STILLS) await stills(STILLS.split(',')); else await full(); }
catch (e) { die(e.message, 1); }
