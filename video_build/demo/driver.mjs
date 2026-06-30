import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';

const EXEC = '/nix/store/qa9cnw4v5xkxyip6mb9kxqfq1z4x2dx1-chromium-138.0.7204.100/bin/chromium';
const BASE = 'http://localhost:5000';
const VW = 1280, VH = 720;
const VIDS = path.resolve('video_build/demo/vids');
const SHOTS = path.resolve('video_build/demo/shots');
const DL = path.resolve('video_build/demo/downloads');
for (const d of [VIDS, SHOTS, DL]) fs.mkdirSync(d, { recursive: true });

const WANT = (process.env.SEGMENTS || 'all').split(',').map(s => s.trim()).filter(Boolean);
const want = (key) => WANT.includes('all') || WANT.includes(key);
const log = (...a) => console.log(`[${new Date().toISOString().slice(11, 19)}]`, ...a);
const pause = (p, ms) => p.waitForTimeout(ms);

let browser;
let T0 = 0;          // wall-clock at start of current recording (≈ video t=0)
let CUTS = [];       // [{a,b}] video-time ranges (seconds) to remove (dead latency)
const mark = () => (Date.now() - T0) / 1000;
function addCut(a, b, minGap = 1.5) {
  if (b - a > minGap) { CUTS.push({ a: +a.toFixed(2), b: +b.toFixed(2) }); log(`    cut dead time ${(b - a).toFixed(1)}s`); }
}

async function launch() {
  browser = await chromium.launch({
    executablePath: EXEC, headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--force-color-profile=srgb'],
  });
}

async function rec(name) {
  const dir = path.join(VIDS, name);
  fs.mkdirSync(dir, { recursive: true });
  const ctx = await browser.newContext({
    viewport: { width: VW, height: VH }, deviceScaleFactor: 2,
    recordVideo: { dir, size: { width: VW, height: VH } }, acceptDownloads: true,
  });
  const page = await ctx.newPage();
  page.on('dialog', async (d) => {
    const m = d.message().toLowerCase();
    const v = m.includes('project') ? 'Symptom Theory' : m.includes('rename') ? 'Symptom Theory' : 'Demo';
    try { await d.accept(v); } catch { }
  });
  page.on('download', async (d) => {
    try { await d.saveAs(path.join(DL, `${name}_${d.suggestedFilename()}`)); log('  download saved', d.suggestedFilename()); } catch { }
  });
  T0 = Date.now();
  CUTS = [];
  return { ctx, page };
}

async function finish(name, ctx, page) {
  const vid = page.video();
  await ctx.close();
  if (vid) {
    const src = await vid.path().catch(() => null);
    if (src && fs.existsSync(src)) {
      const dst = path.join(VIDS, `${name}.webm`);
      fs.renameSync(src, dst);
      fs.writeFileSync(path.join(VIDS, `${name}.cuts.json`), JSON.stringify(CUTS));
      log(`  ✓ video -> ${path.basename(dst)} (${(fs.statSync(dst).size / 1e6).toFixed(2)} MB)${CUTS.length ? `, ${CUTS.length} cut(s)` : ''}`);
    }
  }
  try { fs.rmSync(path.join(VIDS, name), { recursive: true, force: true }); } catch { }
}

async function gotoApp(page) {
  await page.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForSelector('#user-input', { timeout: 20000 });
  await pause(page, 1600);
}

async function shot(page, name) { await page.screenshot({ path: path.join(SHOTS, name + '.png') }).catch(() => { }); }

async function pickThinker(page, db) {
  const sel = `button.avatar-btn[data-db="${db}"], button.related-avatar[data-db="${db}"]`;
  await page.click(sel, { timeout: 8000 }).catch(async () => { await page.click(`[data-db="${db}"]`, { timeout: 8000 }).catch(() => { }); });
  await pause(page, 700);
}

async function typeQ(page, text, delay = 10) {
  await page.click('#user-input');
  await page.fill('#user-input', '');
  await page.type('#user-input', text, { delay });
  await pause(page, 500);
}

async function setSlider(page, id, val) {
  await page.locator('#' + id).fill(String(val)).catch(() => { });
  await pause(page, 500);
}

async function scrollToLatestQA(page) {
  await page.evaluate(() => {
    const c = document.getElementById('messages');
    const us = document.querySelectorAll('.message-user');
    const as = document.querySelectorAll('.message-assistant');
    const anchor = us[us.length - 1] || as[as.length - 1];
    if (c && anchor) c.scrollTo({ top: Math.max(0, anchor.offsetTop - 12), behavior: 'smooth' });
  }).catch(() => { });
}

// After an answer finishes, make it VISIBLE on camera: show question + start of the
// answer (money shot), then slowly pan through the answer, then return to the top.
async function revealAnswer(page, { readMs = 9000, steps = 6 } = {}) {
  await scrollToLatestQA(page);
  await pause(page, 3600);
  for (let i = 0; i < steps; i++) {
    const more = await page.evaluate(() => {
      const c = document.getElementById('messages');
      if (!c) return false;
      if (c.scrollTop + c.clientHeight >= c.scrollHeight - 12) return false;
      c.scrollBy({ top: Math.floor(c.clientHeight * 0.7), behavior: 'smooth' });
      return true;
    }).catch(() => false);
    if (!more) break;
    await pause(page, Math.max(1400, Math.floor(readMs / steps)));
  }
  await pause(page, 1200);
  await scrollToLatestQA(page);
  await pause(page, 2200);
}

// Submit current input, wait for the streamed answer to complete, cut the dead
// latency, verify the answer is real, then reveal it on camera.
async function consult(page, { maxMs = 240000, reveal = true, tag = '' } = {}) {
  const beforeCount = await page.evaluate(() => document.querySelectorAll('.message-assistant .message-text').length).catch(() => 0);
  await page.click('#submit-btn');
  const tA = mark();
  await page.waitForFunction(() => {
    const b = document.querySelector('#submit-btn');
    return (b && b.disabled) || document.querySelector('.message-text.streaming') || document.querySelector('.message-assistant');
  }, { timeout: 20000 }).catch(() => { });
  await page.waitForFunction((bc) => {
    const b = document.querySelector('#submit-btn');
    const streaming = document.querySelector('.message-text.streaming');
    const n = document.querySelectorAll('.message-assistant .message-text').length;
    return b && !b.disabled && !streaming && n > bc;
  }, { timeout: maxMs }, beforeCount).catch(() => { });
  const tB = mark();
  addCut(tA + 0.4, tB - 0.3);
  await page.waitForFunction(() => {
    const s = document.querySelector('#sources-display');
    return s && s.children.length > 0;
  }, { timeout: 20000 }).catch(() => { });
  const info = await page.evaluate(() => {
    const t = document.querySelectorAll('.message-assistant .message-text');
    const last = t[t.length - 1];
    const txt = last ? last.textContent.trim() : '';
    return { words: txt ? txt.split(/\s+/).filter(Boolean).length : 0 };
  }).catch(() => ({ words: 0 }));
  log(`    ${tag} answer: ${info.words} words`);
  if (info.words < 5) log(`    !! WARNING: ${tag} answer appears empty`);
  if (reveal) await revealAnswer(page);
  else await pause(page, 2000);
}

async function closeModal(page, closeId) {
  await page.click('#' + closeId, { timeout: 4000 }).catch(async () => { await page.keyboard.press('Escape').catch(() => { }); });
  await pause(page, 700);
}

// One grounded Q/A turn: configure thinker + controls, type the prompt, consult, reveal.
async function turn(page, o) {
  await pickThinker(page, o.thinker);
  if (o.mode) await page.selectOption('#response-mode-select', o.mode).catch(() => { });
  if (o.data) await page.selectOption('#data-source-select', o.data).catch(() => { });
  if (o.len != null) await setSlider(page, 'answer-length', o.len);
  if (o.quotes != null) await setSlider(page, 'quote-count', o.quotes);
  if (o.creativity != null) await setSlider(page, 'creativity-level', o.creativity);
  await typeQ(page, o.q);
  await consult(page, { tag: o.tag || o.thinker, maxMs: o.maxMs || 240000 });
}

// ============================== SEGMENTS ==============================

// 01 — Orientation: the thinkers and how to ask (no LLM, fast)
async function intro() {
  log('01 intro / thinker selection');
  const { ctx, page } = await rec('01_intro');
  await gotoApp(page);
  for (const d of ['freud', 'kuczynski', 'jung', 'hume', 'nietzsche', 'bergler']) { await pickThinker(page, d); await pause(page, 650); }
  await pickThinker(page, 'kuczynski');
  await page.click('#what-to-ask-btn', { timeout: 5000 }).catch(async () => { await page.click('#what-to-ask-btn-header', { timeout: 5000 }).catch(() => { }); });
  await page.waitForSelector('#topics-modal', { state: 'visible', timeout: 6000 }).catch(() => { });
  await pause(page, 2400);
  await shot(page, '01_intro');
  await closeModal(page, 'close-topics-modal');
  await finish('01_intro', ctx, page);
}

// 02 — Each thinker turns a STATEMENT (from the uploaded texts) into an ESSAY
async function essays() {
  log('02 statement -> essay (each thinker)');
  const { ctx, page } = await rec('02_essays');
  await gotoApp(page);
  const E = 'Turn the following statement into a short, rigorous essay defending it: ';
  const items = [
    { thinker: 'freud', q: E + '“It is aggression, not sexuality, that is the primary object of repression.”' },
    { thinker: 'kuczynski', q: E + '“Beauty is categorically identical with content-bioavailability.”' },
    { thinker: 'jung', q: E + '“The shadow is not merely what is repressed; it is the unlived life the conscious personality refuses to own.”' },
    { thinker: 'hume', q: E + '“All knowledge of matters of fact rests on cause and effect, which is learned only from experience and never from reason.”' },
    { thinker: 'nietzsche', q: E + '“Morality is the herd-instinct in the individual.”' },
    { thinker: 'bergler', q: E + '“Every neurotic is fundamentally a psychic masochist pursuing pleasure in displeasure.”' },
  ];
  for (const it of items) await turn(page, { ...it, mode: 'standard', data: 'classic', len: 350, quotes: 4, creativity: 8, tag: 'essay/' + it.thinker });
  await shot(page, '02_essays');
  await finish('02_essays', ctx, page);
}

// 03 — Each thinker EVALUATES a statement (true? false? with reasons)
async function evaluate() {
  log('03 evaluate a statement (each thinker)');
  const { ctx, page } = await rec('03_evaluate');
  await gotoApp(page);
  const V = 'Evaluate the following claim. Is it true? Give your verdict and your reasons: ';
  const items = [
    { thinker: 'freud', q: V + '“Group psychology is more basic than individual psychology.”' },
    { thinker: 'kuczynski', q: V + '“A priori knowledge is not knowledge your mind has, but knowledge that IS your mind.”' },
    { thinker: 'jung', q: V + '“Religious symbols are nothing but projections of the collective unconscious.”' },
    { thinker: 'hume', q: V + '“That the future will resemble the past can be proved by reason.”' },
    { thinker: 'nietzsche', q: V + '“Pity is a virtue that strengthens both the one who gives it and the one who receives it.”' },
    { thinker: 'bergler', q: V + '“Aggression, not masochism, is the true bedrock of neurosis.”' },
  ];
  for (const it of items) await turn(page, { ...it, mode: 'standard', data: 'classic', len: 350, quotes: 3, creativity: 8, tag: 'eval/' + it.thinker });
  await shot(page, '03_evaluate');
  await finish('03_evaluate', ctx, page);
}

// 04 — INTERVIEW the thinker, starting from an excerpt of the uploaded text
async function interview() {
  log('04 interview from an excerpt');
  const { ctx, page } = await rec('04_interview');
  await gotoApp(page);
  await turn(page, {
    thinker: 'kuczynski', mode: 'dialogue', data: 'classic', len: 300, quotes: 2, creativity: 9, tag: 'interview/kuczynski',
    q: 'I want to interview you about a passage of yours. You wrote: “An ego-syntonic illness is an inability to think rationally, and an ego-dystonic illness is an inability to act rationally.” My question: on this account, what exactly separates the obsessive-compulsive from the schizophrenic?',
  });
  await turn(page, {
    thinker: 'kuczynski', mode: 'dialogue', data: 'classic', len: 300, quotes: 2, creativity: 9, tag: 'interview/followup',
    q: 'Follow-up: you distinguish functional from structural delusiveness. Is OCD then a neurosis or a psychosis, and why does the obsessive-compulsive “hiss and seethe” when his situation is described to him?',
  });
  await turn(page, {
    thinker: 'freud', mode: 'dialogue', data: 'classic', len: 300, quotes: 2, creativity: 9, tag: 'interview/freud',
    q: 'Interview question from your text: you claim we repress sexuality only insofar as it is infused with aggression, and that masochism is sadism turned against the self. Walk me through why masochism is itself a form of repression.',
  });
  await shot(page, '04_interview');
  await finish('04_interview', ctx, page);
}

// 05 — DIALOGUE between multiple thinkers about the uploaded material (longform)
async function dialogue() {
  log('05 multi-thinker dialogue (longform)');
  const { ctx, page } = await rec('05_dialogue');
  await gotoApp(page);
  await page.click('#longform-btn');
  await page.waitForSelector('#longform-modal', { state: 'visible', timeout: 8000 });
  await pause(page, 700);
  await page.selectOption('#lf-thinker', 'kuczynski').catch(() => { });
  await page.selectOption('#lf-mode', 'dialogue').catch(() => { });
  await page.fill('#lf-target-words', '1400').catch(() => { });
  await page.fill('#lf-prompt', 'A dialogue between Freud and Bergler on what is most fundamentally repressed. Freud presses the thesis that aggression — not sexuality — is the primary object of repression, and that masochism is inverted aggression. Bergler replies that psychic masochism, the pursuit of pleasure in displeasure, is the basic neurosis underlying even aggression. Let them genuinely disagree.');
  await pause(page, 700);
  const tA = mark();
  await page.click('#lf-start-btn');
  // wait for the skeleton to render
  await page.waitForFunction(() => { const s = document.querySelector('#lf-sections'); return s && s.children.length >= 1; }, { timeout: 150000 }).catch(() => { });
  const tB = mark();
  addCut(tA + 0.4, tB - 0.3); // cut the wait for the skeleton
  await pause(page, 3000); // show the skeleton on camera
  await shot(page, '05_dialogue_a');
  // wait for at least 2 COMPLETED section cards (real dialogue prose, not the placeholder)
  const tC = mark();
  await page.waitForFunction(
    () => document.querySelectorAll('#lf-sections .lf-section-card:not(.lf-section-pending)').length >= 2,
    undefined,
    { timeout: 260000, polling: 2000 }
  ).catch(() => { });
  const tD = mark();
  addCut(tC + 0.4, tD - 0.3); // cut the section-generation wait
  const info = await page.evaluate(() => {
    const done = document.querySelectorAll('#lf-sections .lf-section-card:not(.lf-section-pending)');
    const ps = document.querySelectorAll('#lf-sections .lf-section-card:not(.lf-section-pending) .lf-section-card-body p');
    const chars = Array.from(ps).map(p => p.textContent || '').join(' ').replace(/\s+/g, ' ').trim().length;
    return { sections: done.length, chars };
  }).catch(() => ({ sections: 0, chars: 0 }));
  log(`    dialogue generated: ${info.sections} sections, ${info.chars} chars`);
  if (info.chars < 200) log('    !! WARNING: dialogue prose appears empty');
  // pan through each completed section's prose so it is readable on camera
  const cardIds = await page.evaluate(() =>
    Array.from(document.querySelectorAll('#lf-sections .lf-section-card:not(.lf-section-pending)')).map(c => c.id)
  ).catch(() => []);
  for (const id of cardIds) {
    await page.evaluate((cid) => { const c = document.getElementById(cid); if (c) c.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, id).catch(() => { });
    await pause(page, 5000);
  }
  await pause(page, 2500);
  await shot(page, '05_dialogue_b');
  await finish('05_dialogue', ctx, page);
}

// 06 — Ask for the QUOTES / arguments / positions on a specific upload issue (RAG)
async function quotes() {
  log('06 quotes / positions on a specific issue');
  const { ctx, page } = await rec('06_quotes');
  await gotoApp(page);
  await turn(page, {
    thinker: 'kuczynski', mode: 'standard', data: 'newdb', len: 350, quotes: 12, creativity: 4, tag: 'quotes/delusiveness',
    q: 'Give me the exact positions and closely-quoted arguments from your work distinguishing functional (neurotic) delusiveness from structural (psychotic) delusiveness.',
  });
  await turn(page, {
    thinker: 'freud', mode: 'standard', data: 'newdb', len: 350, quotes: 12, creativity: 4, tag: 'quotes/repression',
    q: 'Quote the specific arguments and positions for the claim that we repress sexuality only to the extent that it is infused with aggression.',
  });
  await shot(page, '06_quotes');
  await finish('06_quotes', ctx, page);
}

// 07 — SAME thinker, SAME question, DIFFERENT creativity/intensity setting
async function intensity() {
  log('07 same question, different intensity meter');
  const { ctx, page } = await rec('07_intensity');
  await gotoApp(page);
  const Q = 'Can beauty really be reduced to content-bioavailability, or is something left out?';
  await turn(page, { thinker: 'kuczynski', mode: 'standard', data: 'classic', len: 350, quotes: 6, creativity: 1, q: Q, tag: 'intensity/low(1)' });
  await turn(page, { thinker: 'kuczynski', mode: 'standard', data: 'classic', len: 350, quotes: 6, creativity: 20, q: Q, tag: 'intensity/high(20)' });
  await shot(page, '07_intensity');
  await finish('07_intensity', ctx, page);
}

const ALL = [
  ['01_intro', intro],
  ['02_essays', essays],
  ['03_evaluate', evaluate],
  ['04_interview', interview],
  ['05_dialogue', dialogue],
  ['06_quotes', quotes],
  ['07_intensity', intensity],
];

(async () => {
  await launch();
  for (const [key, fn] of ALL) {
    if (!want(key)) continue;
    try { await fn(); }
    catch (e) { log(`  !! ${key} error:`, e.message); }
  }
  await browser.close();
  log('DONE');
})();
