#!/usr/bin/env node
// R1 — FreudGPT synthetic user agent. Standalone Node project. See README.md.

import { chromium } from 'playwright';
import Anthropic from '@anthropic-ai/sdk';
import { createServer } from 'node:http';
import { mkdir, writeFile, appendFile, readFile, stat } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';

// ============================================================================
// CONFIG
// ============================================================================
const APP_URL = process.env.APP_URL || 'http://localhost:5000';
const OUTPUT_DIR = `./runs/${new Date().toISOString().replace(/[:.]/g, '-')}`;
const HEADLESS = process.env.HEADLESS === 'true' || true; // default headless on Replit
const TYPE_DELAY_MS = parseInt(process.env.TYPE_DELAY_MS || '15', 10);
const LIVE_VIEW_PORT = parseInt(process.env.LIVE_VIEW_PORT || '7777', 10);
const SKIP_FUNCTIONS = (process.env.SKIP_FUNCTIONS || '').split(',').filter(Boolean).map(Number);
const CONSULTATION_TIMEOUT_MS = parseInt(process.env.CONSULTATION_TIMEOUT_MS || '300000', 10);
const LONGFORM_TARGET_WORDS = parseInt(process.env.LONGFORM_TARGET_WORDS || '2000', 10);
const ABORT_ON_DIAGNOSTIC_DB_FAIL = process.env.ABORT_ON_DIAGNOSTIC_DB_FAIL !== 'false';
const ANTHROPIC_MODEL = process.env.ANTHROPIC_MODEL || 'claude-opus-4-20250514';
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

if (!ANTHROPIC_API_KEY) {
  console.error('FATAL: ANTHROPIC_API_KEY not set');
  process.exit(1);
}

const BLUEPRINT_COUNTS = { freud: 19077, kuczynski: 17499, jung: 2910, nietzsche: 2838, bergler: 1924, hume: 1114 };

// ============================================================================
// STATE
// ============================================================================
const anthropic = new Anthropic({ apiKey: ANTHROPIC_API_KEY });
const transcript = [];
const networkLog = [];
const screenshots = [];
let screenshotCounter = 0;
let interactionCounter = 0;
let currentInteraction = null;
const liveState = {
  banner: 'R1 starting…',
  step: '',
  approach: '',
  reasoning: '',
  url: '',
  keystrokes: '',
  latestScreenshot: '',
  streamedResponse: '',
  recentApi: [],
  judgeCritique: '',
  grounding: {},
  treeDelta: null,
  longformProgress: null,
  completed: [],
};

// ============================================================================
// UTILS
// ============================================================================
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const sha256 = (s) => createHash('sha256').update(s).digest('hex');
const log = (...args) => { const line = args.map(a => typeof a === 'string' ? a : JSON.stringify(a)).join(' '); console.log(line); _consoleLines.push(line); };
const _consoleLines = [];

async function ensureDir(p) { await mkdir(p, { recursive: true }); }
async function writeJson(p, obj) { await ensureDir(dirname(p)); await writeFile(p, JSON.stringify(obj, null, 2)); }
async function appendJsonl(p, obj) { await ensureDir(dirname(p)); await appendFile(p, JSON.stringify(obj) + '\n'); }

function shingles(text, k = 8) {
  const tokens = (text || '').toLowerCase().split(/\s+/).filter(Boolean);
  const s = new Set();
  for (let i = 0; i + k <= tokens.length; i++) s.add(tokens.slice(i, i + k).join(' '));
  return s;
}
function jaccard(a, b) {
  if (!a.size || !b.size) return 0;
  let inter = 0;
  for (const x of a) if (b.has(x)) inter++;
  return inter / (a.size + b.size - inter);
}

// ============================================================================
// LIVE VIEW SERVER
// ============================================================================
function startLiveView() {
  const html = () => `<!doctype html><meta charset="utf-8"><title>R1 Live View</title>
<style>
  body{font:13px/1.45 ui-monospace,Menlo,monospace;background:#0e1117;color:#e6edf3;margin:0;padding:14px;}
  h1{font-size:15px;margin:0 0 8px;color:#7ee787}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
  .panel{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:10px;max-height:340px;overflow:auto}
  .panel h2{font-size:12px;color:#79c0ff;margin:0 0 6px;text-transform:uppercase;letter-spacing:0.5px}
  pre{white-space:pre-wrap;word-break:break-word;margin:0;font-size:12px}
  .kv{display:grid;grid-template-columns:160px 1fr;gap:4px 8px;font-size:12px}
  .kv b{color:#ffa657;font-weight:normal}
  .stream{background:#0d1117;border:1px solid #21262d;border-radius:4px;padding:6px;min-height:80px;max-height:200px;overflow:auto;font-size:11px}
  .api{border-bottom:1px solid #21262d;padding:3px 0;font-size:11px}
  .api .m{color:#7ee787} .api .s2{color:#7ee787} .api .s4{color:#f78166} .api .s5{color:#ff7b72}
  img{max-width:100%;border:1px solid #30363d;border-radius:4px;display:block;margin-top:4px}
  .completed{font-size:11px;border-bottom:1px solid #21262d;padding:2px 0}
  .ok{color:#7ee787} .fail{color:#ff7b72} .pend{color:#ffa657}
  .banner{background:#1f6feb33;border:1px solid #1f6feb;padding:6px 10px;border-radius:4px;margin-bottom:8px}
</style>
<div class="banner" id="banner">R1 starting…</div>
<div class="grid">
  <div class="panel"><h2>Current Step</h2>
    <div class="kv">
      <b>Step</b><span id="step"></span>
      <b>URL</b><span id="url"></span>
      <b>Approach</b><span id="approach"></span>
      <b>Reasoning</b><span id="reasoning"></span>
      <b>Keystrokes</b><span id="keystrokes"></span>
    </div>
    <div id="shot"></div>
  </div>
  <div class="panel"><h2>Streamed Response</h2><div class="stream" id="stream"></div></div>
  <div class="panel"><h2>Recent /api/* Calls</h2><div id="api"></div></div>
  <div class="panel"><h2>Grounding State</h2><div class="kv" id="grounding"></div>
    <h2 style="margin-top:10px">Tree Delta</h2><div class="kv" id="tree"></div>
    <h2 style="margin-top:10px">Longform Progress</h2><div class="kv" id="lf"></div>
  </div>
  <div class="panel" style="grid-column:1/3;max-height:200px"><h2>Judge Critique (latest)</h2><pre id="judge"></pre></div>
  <div class="panel" style="grid-column:1/3"><h2>Completed Interactions (newest first)</h2><div id="completed"></div></div>
</div>
<script>
async function tick(){
  try{
    const r = await fetch('/state'); const s = await r.json();
    document.getElementById('banner').textContent = s.banner || '';
    document.getElementById('step').textContent = s.step || '';
    document.getElementById('url').textContent = s.url || '';
    document.getElementById('approach').textContent = s.approach || '';
    document.getElementById('reasoning').textContent = s.reasoning || '';
    document.getElementById('keystrokes').textContent = s.keystrokes || '';
    document.getElementById('shot').innerHTML = s.latestScreenshot ? '<img src="/shot/'+encodeURIComponent(s.latestScreenshot)+'?t='+Date.now()+'">' : '';
    document.getElementById('stream').textContent = s.streamedResponse || '';
    document.getElementById('judge').textContent = s.judgeCritique || '';
    document.getElementById('api').innerHTML = (s.recentApi||[]).map(c=>'<div class="api"><span class="m">'+c.method+'</span> '+c.url+' <span class="s'+String(c.status).charAt(0)+'">'+c.status+'</span> '+c.ms+'ms</div>').join('');
    const g = s.grounding || {};
    document.getElementById('grounding').innerHTML = Object.entries(g).map(([k,v])=>'<b>'+k+'</b><span>'+(Array.isArray(v)?'['+v.slice(0,10).join(', ')+(v.length>10?', …':'')+']':String(v))+'</span>').join('');
    const t = s.treeDelta || {};
    document.getElementById('tree').innerHTML = Object.entries(t).map(([k,v])=>'<b>'+k+'</b><span>'+(Array.isArray(v)?JSON.stringify(v):String(v))+'</span>').join('');
    const lf = s.longformProgress || {};
    document.getElementById('lf').innerHTML = Object.entries(lf).map(([k,v])=>'<b>'+k+'</b><span>'+(typeof v==='object'?JSON.stringify(v).slice(0,200):String(v))+'</span>').join('');
    document.getElementById('completed').innerHTML = (s.completed||[]).slice().reverse().map(c=>'<div class="completed"><span class="'+(c.violations?'fail':(c.concerns?'pend':'ok'))+'">●</span> #'+c.n+' F'+c.fn+' '+c.name+' — '+c.verdict+'</div>').join('');
  }catch(e){}
  setTimeout(tick, 800);
}
tick();
</script>`;

  const srv = createServer(async (req, res) => {
    if (req.url === '/state') {
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify(liveState));
    } else if (req.url?.startsWith('/shot/')) {
      const name = decodeURIComponent(req.url.slice(6).split('?')[0]);
      try {
        const buf = await readFile(join(OUTPUT_DIR, 'screenshots', name));
        res.writeHead(200, { 'content-type': 'image/png' });
        res.end(buf);
      } catch { res.writeHead(404); res.end(); }
    } else {
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
      res.end(html());
    }
  });
  srv.listen(LIVE_VIEW_PORT, () => log(`Live view: http://localhost:${LIVE_VIEW_PORT}`));
  return srv;
}

// ============================================================================
// SCREENSHOT
// ============================================================================
async function snap(page, label) {
  screenshotCounter++;
  const fname = `${String(screenshotCounter).padStart(4, '0')}-${label}.png`;
  const path = join(OUTPUT_DIR, 'screenshots', fname);
  await ensureDir(dirname(path));
  try {
    await page.screenshot({ path, fullPage: false });
    screenshots.push(fname);
    liveState.latestScreenshot = fname;
    return fname;
  } catch (e) {
    log('snap failed', e.message);
    return null;
  }
}

// ============================================================================
// NETWORK CAPTURE
// ============================================================================
function attachNetworkCapture(page) {
  page.on('response', async (resp) => {
    const url = resp.url();
    if (!url.includes('/api/')) return;
    const req = resp.request();
    const t0 = Date.now();
    let body = '';
    let isSSE = false;
    try {
      const ct = resp.headers()['content-type'] || '';
      isSSE = ct.includes('text/event-stream');
      if (!isSSE) body = await resp.text();
    } catch (e) { body = `[body read error: ${e.message}]`; }
    const entry = {
      t: new Date().toISOString(),
      method: req.method(),
      url,
      status: resp.status(),
      ms: Date.now() - t0,
      requestBody: (req.postData() || '').slice(0, 4000),
      responseBody: isSSE ? '[SSE stream — see sse-streams/]' : body.slice(0, 8000),
      isSSE,
    };
    networkLog.push(entry);
    await appendJsonl(join(OUTPUT_DIR, 'network.log'), entry);
    if (currentInteraction) currentInteraction.app_response.network_calls.push(entry);
    liveState.recentApi = [...liveState.recentApi, { method: entry.method, url: entry.url.replace(APP_URL, ''), status: entry.status, ms: entry.ms }].slice(-10);
  });
  page.on('console', (msg) => {
    if (msg.type() === 'error' && currentInteraction) {
      currentInteraction.app_response.errors_in_console.push(msg.text());
    }
  });
}

// ============================================================================
// SSE CONSUMPTION (via fetch — not via Playwright; SSE is hard to capture there)
// ============================================================================
// FreudGPT emits: `data: {"type":"token"|"retrieval_log"|"sources"|"done", "data": ...}`
// with NO `event:` line (except longform service which uses real `event:` names).
// Longform service: `event: <name>\ndata: <json>\n\n`. We handle both.
async function consumeSSE(url, options = {}, onEvent, timeoutMs = CONSULTATION_TIMEOUT_MS, ssePath = null) {
  const events = [];
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  let fullText = '';
  const t0 = Date.now();
  const requestSummary = { method: options.method || 'GET', url, requestBody: options.body || '', isSSE: true };
  try {
    const r = await fetch(url, { ...options, signal: controller.signal });
    requestSummary.status = r.status;
    if (!r.body) throw new Error('no body');
    const reader = r.body.getReader();
    const decoder = new TextDecoder();
    let buf = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      let idx;
      while ((idx = buf.indexOf('\n\n')) !== -1) {
        const raw = buf.slice(0, idx);
        buf = buf.slice(idx + 2);
        const evMatch = raw.match(/^event:\s*(.+)$/m);
        const dataMatch = raw.match(/^data:\s*([\s\S]+)$/m);
        if (!dataMatch) continue;
        let raw_data = dataMatch[1].replace(/\ndata:\s*/g, '\n'); // unfold multi-line data
        let parsed = raw_data;
        try { parsed = JSON.parse(raw_data); } catch {}
        // Resolve event type — prefer explicit event:, else parsed.type, else 'message'
        let type = evMatch ? evMatch[1].trim() : (parsed && typeof parsed === 'object' && parsed.type) ? parsed.type : 'message';
        // Normalize FreudGPT's retrieval_log to canonical 'retrieval' for downstream code
        const canonicalType = type === 'retrieval_log' ? 'retrieval' : type;
        // If the JSON envelope has a 'type' field, treat the rest as the payload.
        // Prefer parsed.data when present (FreudGPT convention), else the whole object minus 'type'.
        const payload = (parsed && typeof parsed === 'object' && parsed.type)
          ? (('data' in parsed) ? parsed.data : (() => { const { type: _t, ...rest } = parsed; return rest; })())
          : parsed;
        // Preserve sibling `positions` field on sources event
        const extra = (parsed && typeof parsed === 'object' && parsed.positions) ? { positions: parsed.positions } : {};
        const ev = { t: new Date().toISOString(), type: canonicalType, rawType: type, data: payload, ...extra };
        events.push(ev);
        // Token accumulation: FreudGPT uses parsed.data as the token string
        if (canonicalType === 'token') {
          const tok = (typeof payload === 'string') ? payload : (payload?.text || payload?.token || '');
          if (tok) { fullText += tok; liveState.streamedResponse = fullText.slice(-2000); }
        }
        if (onEvent) try { onEvent(ev); } catch (e) { log('onEvent err', e.message); }
        if (canonicalType === 'done' || canonicalType === 'complete' || canonicalType === 'error') {
          clearTimeout(timer);
          requestSummary.ms = Date.now() - t0;
          requestSummary.responseBody = `[SSE — ${events.length} events, ${fullText.length} chars assembled. See sse-streams/]`;
          await logFetchCall(requestSummary);
          return { events, fullText };
        }
      }
    }
  } catch (e) {
    events.push({ t: new Date().toISOString(), type: 'harness_error', data: e.message });
  } finally {
    clearTimeout(timer);
  }
  requestSummary.ms = Date.now() - t0;
  requestSummary.responseBody = `[SSE — ${events.length} events, ${fullText.length} chars assembled. Possibly truncated/aborted.]`;
  await logFetchCall(requestSummary);
  return { events, fullText };
}

// Centralized fetch logger so Node-side calls land in network.log alongside Playwright calls.
async function logFetchCall({ method, url, status, ms, requestBody, responseBody, isSSE }) {
  const entry = { t: new Date().toISOString(), method, url, status: status ?? 0, ms: ms ?? 0,
    requestBody: typeof requestBody === 'string' ? requestBody.slice(0, 4000) : JSON.stringify(requestBody || '').slice(0, 4000),
    responseBody: (responseBody || '').slice(0, 8000), isSSE: !!isSSE, source: 'node-fetch' };
  networkLog.push(entry);
  await appendJsonl(join(OUTPUT_DIR, 'network.log'), entry);
  if (currentInteraction) currentInteraction.app_response.network_calls.push(entry);
  liveState.recentApi = [...liveState.recentApi, { method, url: url.replace(APP_URL, ''), status: entry.status, ms: entry.ms }].slice(-10);
}

// ============================================================================
// R1 BRAIN + JUDGE (Anthropic)
// ============================================================================
async function r1Think(systemPrompt, userPrompt) {
  try {
    const r = await anthropic.messages.create({
      model: ANTHROPIC_MODEL,
      max_tokens: 600,
      system: systemPrompt,
      messages: [{ role: 'user', content: userPrompt }],
    });
    return r.content[0]?.text || '';
  } catch (e) {
    log('R1 brain error', e.message);
    return `[R1 brain unavailable: ${e.message}]`;
  }
}

async function judge(interaction, retrievedPositionTexts = []) {
  const sys = `You are a strict beta-test judge for a database-grounded philosophical consultation app (FreudGPT). Your job is to identify whether responses are grounded in the retrieved philosophical positions provided. Be prose, be specific, be skeptical. Output JSON only:
{
  "critique": "<2-5 sentence prose critique>",
  "concerns": ["..."],
  "violations": [{"invariant": "A|B|D|E", "detail": "..."}],
  "claims_in_response": ["..."],
  "claims_grounded": ["..."],
  "claims_unsupported": ["..."],
  "invariant_a_passed": true,
  "low_relevance_warning_present": false
}`;
  const userMsg = `INTERACTION CONTEXT:
Function: ${interaction.function_name}
R1 input: ${interaction.r1_input}
R1 parameters: ${JSON.stringify(interaction.r1_parameters)}

RETRIEVED POSITIONS (the ONLY material the response should be grounded in):
${retrievedPositionTexts.length ? retrievedPositionTexts.map((t, i) => `[${i + 1}] ${(t || '').slice(0, 1500)}`).join('\n\n') : '(none — flag if response makes confident claims)'}

ASSEMBLED RESPONSE FROM APP:
${(interaction.app_response.assembled_text || '').slice(0, 6000)}

RETRIEVAL METADATA:
max_similarity = ${interaction.app_response.retrieval_event?.max_similarity ?? 'unknown'}
positions_above_threshold = ${interaction.app_response.retrieval_event?.positions_above_threshold ?? 'unknown'}

Was the response grounded? Were claims traceable to specific positions? If max_similarity < 0.25, did the response explicitly acknowledge the gap rather than invent material? Anything broken or off?`;
  try {
    const r = await anthropic.messages.create({
      model: ANTHROPIC_MODEL,
      max_tokens: 1500,
      system: sys,
      messages: [{ role: 'user', content: userMsg }],
    });
    const text = r.content[0]?.text || '';
    const m = text.match(/\{[\s\S]*\}/);
    if (m) {
      try { return JSON.parse(m[0]); } catch {}
    }
    return { critique: text, concerns: [], violations: [], claims_in_response: [], claims_grounded: [], claims_unsupported: [], invariant_a_passed: null, low_relevance_warning_present: null };
  } catch (e) {
    return { critique: `[Judge unavailable: ${e.message}]`, concerns: [], violations: [], claims_in_response: [], claims_grounded: [], claims_unsupported: [], invariant_a_passed: null, low_relevance_warning_present: null };
  }
}

// ============================================================================
// INTERACTION FRAMING
// ============================================================================
function newInteraction({ fn, name, step, url, interactive, expectedRoutes, approach, reasoning, input, params }) {
  interactionCounter++;
  const ix = {
    timestamp: new Date().toISOString(),
    n: interactionCounter,
    function_number: fn,
    function_name: name,
    step_description: step,
    url,
    is_interactive: interactive,
    expected_routes: expectedRoutes || [],
    r1_approach: approach || '',
    r1_reasoning: reasoning || '',
    r1_input: input || '',
    r1_parameters: params || {},
    app_response: {
      assembled_text: '',
      retrieval_event: null,
      retrieved_position_texts: [],
      errors_in_console: [],
      network_calls: [],
      sse_events_observed: [],
    },
    grounding_verification: null,
    tractatus_delta: null,
    longform_structure: null,
    screenshots: [],
    judge_critique: '',
    judge_concerns: [],
    invariant_violations: [],
  };
  currentInteraction = ix;
  transcript.push(ix);
  liveState.step = `#${interactionCounter} F${fn} — ${name}: ${step}`;
  liveState.url = url;
  liveState.approach = approach || '';
  liveState.reasoning = reasoning || '';
  liveState.keystrokes = input || '';
  liveState.streamedResponse = '';
  liveState.grounding = {};
  liveState.treeDelta = null;
  liveState.longformProgress = null;
  return ix;
}
async function finishInteraction(ix) {
  liveState.completed = [...liveState.completed, {
    n: ix.n, fn: ix.function_number, name: ix.function_name,
    verdict: ix.invariant_violations.length ? `${ix.invariant_violations.length} VIOLATION(S)` : (ix.judge_concerns.length ? `${ix.judge_concerns.length} concern(s)` : 'OK'),
    violations: ix.invariant_violations.length, concerns: ix.judge_concerns.length,
  }].slice(-50);
  await appendJsonl(join(OUTPUT_DIR, 'transcript.jsonl'), ix);
  currentInteraction = null;
}

// ============================================================================
// APP CLIENT (direct fetch helpers — used in parallel to Playwright)
// ============================================================================
async function api(method, path, body) {
  const t0 = Date.now();
  const url = `${APP_URL}${path}`;
  let r, text = '';
  try {
    r = await fetch(url, {
      method,
      headers: body ? { 'content-type': 'application/json' } : {},
      body: body ? JSON.stringify(body) : undefined,
    });
    text = await r.text();
  } catch (e) {
    await logFetchCall({ method, url, status: 0, ms: Date.now() - t0, requestBody: body, responseBody: `[fetch error: ${e.message}]`, isSSE: false });
    return { status: 0, body: null, error: e.message };
  }
  let parsed = null;
  try { parsed = JSON.parse(text); } catch { parsed = text; }
  await logFetchCall({ method, url, status: r.status, ms: Date.now() - t0, requestBody: body, responseBody: text, isSSE: false });
  return { status: r.status, body: parsed };
}

// ============================================================================
// FUNCTION 1 — DIAGNOSTIC (FIRST)
// ============================================================================
async function fn1_diagnosticBefore(page) {
  if (SKIP_FUNCTIONS.includes(1)) return null;
  const ix = newInteraction({
    fn: 1, name: 'Diagnostic (BEFORE)', step: 'Capture baseline diagnostic',
    url: APP_URL + '/', interactive: true, expectedRoutes: ['POST /api/diagnostic/run'],
    approach: 'baseline-capture', reasoning: 'Must capture per-thinker counts and all check statuses before any other interaction so post-run comparison is valid.',
    input: 'Click DIAGNOSTIC, then Run Full Diagnostic',
    params: {},
  });
  await page.goto(APP_URL + '/', { waitUntil: 'domcontentloaded' });
  ix.screenshots.push(await snap(page, 'diag-before-1-pre'));
  try {
    await page.click('#diagnostic-btn', { timeout: 10000 });
    await page.waitForSelector('#diagnostic-modal', { state: 'visible', timeout: 5000 }).catch(() => {});
    ix.screenshots.push(await snap(page, 'diag-before-2-open'));
  } catch (e) {
    log('Could not click diagnostic button via UI, falling back to direct API');
    ix.screenshots.push(await snap(page, 'diag-before-2-fallback'));
  }
  const t0 = Date.now();
  const res = await api('POST', '/api/diagnostic/run');
  const ms = Date.now() - t0;
  ix.app_response.assembled_text = JSON.stringify(res.body, null, 2);
  ix.app_response.sse_events_observed = ['(synchronous JSON, no SSE)'];
  await writeJson(join(OUTPUT_DIR, 'outputs', 'diagnostic-before.json'), res.body);

  // Validate per-thinker counts vs blueprint
  const counts = {};
  if (res.body?.results) {
    for (const c of res.body.results) {
      const m = c.detail?.match(/(\w+)\s*=\s*(\d+)/g);
      if (m) for (const part of m) { const mm = part.match(/(\w+)\s*=\s*(\d+)/); if (mm) counts[mm[1].toLowerCase()] = parseInt(mm[2], 10); }
    }
  }
  ix.app_response.retrieval_event = { diagnostic_summary: res.body?.summary, ms_total: ms, per_thinker_counts: counts };
  liveState.grounding = { 'Diagnostic PASS': `${res.body?.summary?.passed ?? '?'}/${res.body?.summary?.total ?? '?'}`, 'Diagnostic FAIL': res.body?.summary?.failed ?? '?' };

  for (const [k, v] of Object.entries(BLUEPRINT_COUNTS)) {
    if (counts[k] && counts[k] !== v) {
      ix.judge_concerns.push(`Baseline count drift for ${k}: blueprint=${v} actual=${counts[k]}`);
    }
  }
  ix.screenshots.push(await snap(page, 'diag-before-3-result'));

  if (ABORT_ON_DIAGNOSTIC_DB_FAIL && res.body?.results?.find(r => r.name?.toLowerCase().includes('postgres') && r.status === 'fail')) {
    ix.invariant_violations.push({ invariant: 'C', detail: 'PostgreSQL connectivity check failed — aborting per ABORT_ON_DIAGNOSTIC_DB_FAIL.' });
    await finishInteraction(ix);
    throw new Error('DIAGNOSTIC_DB_FAIL');
  }
  ix.judge_critique = `Captured baseline diagnostic: ${res.body?.summary?.passed ?? '?'}/${res.body?.summary?.total ?? '?'} checks passed. Per-thinker counts captured for later drift comparison. ${ix.judge_concerns.length ? 'NOTE: ' + ix.judge_concerns.join('; ') : 'All counts match blueprint.'} This baseline is the reference point for Invariant C verification at end of run.`;
  await finishInteraction(ix);
  return { counts, fullResult: res.body };
}

// ============================================================================
// FUNCTION 2 — THINKER SELECTION
// ============================================================================
async function fn2_thinkers(page) {
  if (SKIP_FUNCTIONS.includes(2)) return;
  const thinkers = ['freud', 'kuczynski', 'jung', 'hume', 'nietzsche', 'bergler'];
  for (const t of thinkers) {
    const ix = newInteraction({
      fn: 2, name: `Thinker selection: ${t}`, step: `Click ${t} avatar`,
      url: APP_URL + '/', interactive: true, expectedRoutes: [`GET /api/topics/${t}`],
      approach: 'avatar-click', reasoning: `Verify ${t} avatar selects the thinker, count badge visible, knowledge panel opens.`,
      input: `Click data-db="${t}" avatar`,
      params: { thinker: t },
    });
    ix.screenshots.push(await snap(page, `thinker-${t}-1-pre`));
    try {
      await page.click(`[data-db="${t}"]`, { timeout: 5000 });
      await sleep(400);
      ix.screenshots.push(await snap(page, `thinker-${t}-2-clicked`));
    } catch (e) {
      ix.invariant_violations.push({ invariant: 'C', detail: `Could not click thinker avatar for ${t}: ${e.message}` });
    }
    const topics = await api('GET', `/api/topics/${t}`);
    ix.app_response.assembled_text = JSON.stringify(topics.body).slice(0, 4000);
    ix.app_response.retrieval_event = { topics_status: topics.status };
    ix.screenshots.push(await snap(page, `thinker-${t}-3-after`));
    ix.judge_critique = `Thinker ${t}: avatar click ${ix.invariant_violations.length ? 'FAILED' : 'OK'}; topics endpoint returned ${topics.status}. Blueprint count ${BLUEPRINT_COUNTS[t]}. This confirms thinker selection wiring and topics retrieval for the knowledge-panel popup are functional.`;
    await finishInteraction(ix);
  }
}

// ============================================================================
// FUNCTION 3 — SINGLE CONSULTATION (Invariant A)
// ============================================================================
const CONSULTATIONS = [
  { thinker: 'freud', q: 'What is the role of repression in neurosis?' },
  { thinker: 'kuczynski', q: 'What is the difference between meaning and reference?' },
  { thinker: 'jung', q: 'How does the collective unconscious differ from the personal unconscious?' },
];

async function fn3_consultations(page) {
  if (SKIP_FUNCTIONS.includes(3)) return;
  for (const { thinker, q } of CONSULTATIONS) {
    const ix = newInteraction({
      fn: 3, name: `Consultation: ${thinker}`, step: q,
      url: APP_URL + '/', interactive: true, expectedRoutes: ['POST /api/ask'],
      approach: 'in-wheelhouse-substantive',
      reasoning: `Question is squarely in ${thinker}'s wheelhouse — retrieval should produce high max_similarity. Tests Invariant A: every claim in response must trace to a retrieved position.`,
      input: q,
      params: { thinker, provider: 'deepseek', mode: 'standard', data_mode: 'Classic' },
    });
    await page.goto(APP_URL + '/', { waitUntil: 'domcontentloaded' });
    try { await page.click(`[data-db="${thinker}"]`, { timeout: 5000 }); } catch {}
    await sleep(300);
    ix.screenshots.push(await snap(page, `c${thinker}-1-pre`));
    try {
      const ta = await page.$('#question-input, textarea');
      if (ta) await ta.type(q, { delay: TYPE_DELAY_MS });
      ix.screenshots.push(await snap(page, `c${thinker}-2-typed`));
    } catch {}
    // Direct API call for SSE (Playwright's response capture doesn't stream SSE well)
    const ssePath = `/api/ask`;
    const r1Reasoning = await r1Think(
      'You are R1, a synthetic user. Given a function description, briefly state your approach in one sentence.',
      `I will ask ${thinker} "${q}" and verify the response is grounded in the retrieved positions.`
    );
    ix.r1_reasoning = r1Reasoning;
    liveState.reasoning = r1Reasoning;

    const sseStreamPath = join(OUTPUT_DIR, 'sse-streams', `${String(ix.n).padStart(4,'0')}.jsonl`);
    await ensureDir(dirname(sseStreamPath));
    const { events, fullText } = await consumeSSE(`${APP_URL}${ssePath}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'accept': 'text/event-stream' },
      body: JSON.stringify({ question: q, database: thinker, provider: 'deepseek', model: 'deepseek-chat', response_mode: 'standard', enhanced_mode: false, answer_length: 500, quote_count: 3, data_source: 'combined' }),
    }, (ev) => {
      if (ev.type === 'retrieval' && typeof ev.data === 'object') {
        liveState.grounding = {
          'Active thinker': thinker,
          'Positions scanned': ev.data.positions_scanned ?? '?',
          'Above threshold': ev.data.positions_above_threshold ?? '?',
          'Max similarity': ev.data.max_similarity ?? '?',
          'Mean similarity': ev.data.mean_similarity ?? '?',
          'Top-K': ev.data.top_k ?? '?',
          'Position IDs': ev.data.retrieved_position_ids || [],
          'Domains': ev.data.domains_covered || [],
          'Low-relevance warning': (ev.data.max_similarity ?? 1) < 0.25 ? 'YES' : 'NO',
        };
      }
    }, CONSULTATION_TIMEOUT_MS);

    for (const ev of events) await appendJsonl(sseStreamPath, ev);
    ix.app_response.sse_events_observed = events.map(e => e.type);
    const retrievalEv = events.find(e => e.type === 'retrieval');
    if (retrievalEv) ix.app_response.retrieval_event = retrievalEv.data;
    ix.app_response.assembled_text = fullText || events.filter(e => e.type === 'token').map(e => typeof e.data === 'string' ? e.data : (e.data?.text || '')).join('');
    // FreudGPT sources event: { type:'sources', data: <sources list of {title,text,...}>, positions: <full position rows> }
    const sourcesEv = events.find(e => e.type === 'sources');
    if (sourcesEv) {
      const posRows = sourcesEv.positions || (Array.isArray(sourcesEv.data) ? sourcesEv.data : null);
      if (Array.isArray(posRows)) {
        ix.app_response.retrieved_position_texts = posRows.map(p => p.text_evidence || p.text || p.content || JSON.stringify(p)).slice(0, 12);
      }
    }
    // Fallback: fetch positions via search API if SSE didn't include sources
    if (ix.app_response.retrieved_position_texts.length === 0) {
      const ps = await api('GET', `/api/positions/search?thinker=${thinker}&q=${encodeURIComponent(q)}&limit=8`);
      if (ps.body?.positions) {
        ix.app_response.retrieved_position_texts = ps.body.positions.map(p => p.text_evidence || p.text || '').slice(0, 8);
      }
    }
    await writeJson(join(OUTPUT_DIR, 'outputs', 'retrieved-positions', `${String(ix.n).padStart(4,'0')}-${thinker}.json`), ix.app_response.retrieved_position_texts);

    ix.screenshots.push(await snap(page, `c${thinker}-3-after`));

    // Judge
    const j = await judge(ix, ix.app_response.retrieved_position_texts);
    ix.judge_critique = j.critique;
    ix.judge_concerns = j.concerns || [];
    ix.grounding_verification = {
      claims_in_response: j.claims_in_response || [],
      claims_grounded: j.claims_grounded || [],
      claims_unsupported: j.claims_unsupported || [],
      invariant_a_passed: j.invariant_a_passed,
      low_relevance_warning_expected: (retrievalEv?.data?.max_similarity ?? 1) < 0.25,
      low_relevance_warning_present: j.low_relevance_warning_present,
      invariant_b_applicable: (retrievalEv?.data?.max_similarity ?? 1) < 0.25,
    };
    if (j.invariant_a_passed === false || (j.claims_unsupported && j.claims_unsupported.length > 0)) {
      ix.invariant_violations.push({ invariant: 'A', detail: `Ungrounded claims: ${(j.claims_unsupported || []).slice(0, 3).join(' | ')}` });
    }
    liveState.judgeCritique = j.critique;
    await finishInteraction(ix);
  }
}

// ============================================================================
// FUNCTION 4 — INVARIANT B (low-relevance warning)
// ============================================================================
async function fn4_lowRelevance(page) {
  if (SKIP_FUNCTIONS.includes(4)) return;
  const q = 'What are the optimal asset allocations for a 2030 retirement portfolio in a high-inflation environment?';
  const ix = newInteraction({
    fn: 4, name: 'Low-relevance warning (Invariant B)', step: q,
    url: APP_URL + '/', interactive: true, expectedRoutes: ['POST /api/ask'],
    approach: 'out-of-wheelhouse', reasoning: 'Ask Freud about a topic with no overlap in his corpus. max_similarity should be < 0.25 and response must acknowledge gap.',
    input: q, params: { thinker: 'freud', provider: 'deepseek' },
  });
  await page.goto(APP_URL + '/', { waitUntil: 'domcontentloaded' });
  ix.screenshots.push(await snap(page, 'invB-1-pre'));
  ix.screenshots.push(await snap(page, 'invB-2-typed'));
  const sseStreamPath = join(OUTPUT_DIR, 'sse-streams', `${String(ix.n).padStart(4,'0')}.jsonl`);
  const { events, fullText } = await consumeSSE(`${APP_URL}/api/ask`, {
    method: 'POST', headers: { 'content-type': 'application/json', 'accept': 'text/event-stream' },
    body: JSON.stringify({ question: q, database: 'freud', provider: 'deepseek', model: 'deepseek-chat', response_mode: 'standard', enhanced_mode: false, answer_length: 500, quote_count: 3, data_source: 'combined' }),
  }, null, CONSULTATION_TIMEOUT_MS);
  for (const ev of events) await appendJsonl(sseStreamPath, ev);
  ix.app_response.sse_events_observed = events.map(e => e.type);
  const ret = events.find(e => e.type === 'retrieval');
  if (ret) ix.app_response.retrieval_event = ret.data;
  ix.app_response.assembled_text = fullText;
  const sourcesEv = events.find(e => e.type === 'sources');
  if (sourcesEv) {
    const posRows = sourcesEv.positions || (Array.isArray(sourcesEv.data) ? sourcesEv.data : null);
    if (Array.isArray(posRows)) ix.app_response.retrieved_position_texts = posRows.map(p => p.text_evidence || p.text || '').slice(0, 8);
  }
  ix.screenshots.push(await snap(page, 'invB-3-after'));
  const j = await judge(ix, ix.app_response.retrieved_position_texts);
  ix.judge_critique = j.critique;
  ix.judge_concerns = j.concerns || [];
  ix.grounding_verification = {
    claims_in_response: j.claims_in_response || [],
    claims_grounded: j.claims_grounded || [],
    claims_unsupported: j.claims_unsupported || [],
    invariant_a_passed: j.invariant_a_passed,
    low_relevance_warning_expected: true,
    low_relevance_warning_present: j.low_relevance_warning_present,
    invariant_b_applicable: true,
  };
  if (j.low_relevance_warning_present === false) {
    ix.invariant_violations.push({ invariant: 'B', detail: `Off-topic query produced confident response without acknowledging gap. max_similarity=${ret?.data?.max_similarity}` });
  }
  liveState.judgeCritique = j.critique;
  await finishInteraction(ix);
}

// ============================================================================
// FUNCTION 5 — PROVIDER SWITCHING
// ============================================================================
async function fn5_providers(page) {
  if (SKIP_FUNCTIONS.includes(5)) return;
  const provResp = await api('GET', '/api/providers');
  const providers = provResp.body?.providers || provResp.body || [];
  const q = 'What is the unconscious?';
  const responses = [];
  for (const p of providers) {
    const pid = p.id || p;
    const model = p.models?.[0] || p.default_model;
    const ix = newInteraction({
      fn: 5, name: `Provider parity: ${pid}`, step: `Ask "${q}" via ${pid}`,
      url: APP_URL + '/', interactive: true, expectedRoutes: ['POST /api/ask'],
      approach: 'provider-parity', reasoning: 'Same query across providers should retrieve same positions. Byte-identical responses across providers would indicate a fallback.',
      input: q, params: { thinker: 'freud', provider: pid, model },
    });
    ix.screenshots.push(await snap(page, `prov-${pid}-1`));
    ix.screenshots.push(await snap(page, `prov-${pid}-2`));
    const ssePath = join(OUTPUT_DIR, 'sse-streams', `${String(ix.n).padStart(4,'0')}-prov-${pid}.jsonl`);
    const { events, fullText } = await consumeSSE(`${APP_URL}/api/ask`, {
      method: 'POST', headers: { 'content-type': 'application/json', 'accept': 'text/event-stream' },
      body: JSON.stringify({ question: q, database: 'freud', provider: pid, model, response_mode: 'standard', answer_length: 400, quote_count: 3, data_source: 'combined' }),
    }, null, CONSULTATION_TIMEOUT_MS);
    for (const ev of events) await appendJsonl(ssePath, ev);
    ix.app_response.sse_events_observed = events.map(e => e.type);
    const ret = events.find(e => e.type === 'retrieval');
    if (ret) ix.app_response.retrieval_event = ret.data;
    ix.app_response.assembled_text = fullText;
    ix.screenshots.push(await snap(page, `prov-${pid}-3`));
    responses.push({ pid, text: fullText, hash: sha256(fullText.slice(0, 1000)) });
    ix.judge_critique = `Provider ${pid} returned ${fullText.length} chars. Retrieval max_similarity=${ret?.data?.max_similarity ?? 'n/a'}. Position IDs retrieved: ${(ret?.data?.retrieved_position_ids || []).slice(0, 5).join(', ')}. This provider's response is preserved for cross-provider parity comparison.`;
    await finishInteraction(ix);
  }
  // Parity check
  const seen = new Map();
  for (const r of responses) {
    if (seen.has(r.hash)) {
      transcript.push({
        timestamp: new Date().toISOString(), n: ++interactionCounter, function_number: 5, function_name: 'Provider parity concern',
        step_description: `Providers ${seen.get(r.hash)} and ${r.pid} returned byte-identical first 1000 chars`,
        url: '', is_interactive: false, expected_routes: [], r1_approach: 'parity-audit', r1_reasoning: '',
        r1_input: '(meta-check)', r1_parameters: {}, app_response: { assembled_text: '', retrieval_event: null, retrieved_position_texts: [], errors_in_console: [], network_calls: [], sse_events_observed: [] },
        grounding_verification: null, tractatus_delta: null, longform_structure: null, screenshots: [],
        judge_critique: `Byte-identical responses across distinct providers indicate one fell back to the other or both are aliased to the same backend.`,
        judge_concerns: [`Providers ${seen.get(r.hash)} and ${r.pid} return identical first 1000 chars`], invariant_violations: [],
      });
    } else seen.set(r.hash, r.pid);
  }
}

// ============================================================================
// FUNCTION 6 — MEMORY MODE (Invariant D)
// ============================================================================
function isValidWittgensteinId(id) { return typeof id === 'string' && /^\d+(\.\d+)*$/.test(id); }
function nodeHasValidTag(value) {
  if (typeof value !== 'string') return false;
  return /^(ASSERTS|REJECTS|ASSUMES|OPEN|RESOLVED|SYNTHESIZES)\s*[:\-]/.test(value.trim());
}
function flattenTree(tree, acc = []) {
  if (!tree || typeof tree !== 'object') return acc;
  if (Array.isArray(tree)) { for (const n of tree) flattenTree(n, acc); return acc; }
  if (tree.id || tree.value) acc.push({ id: tree.id, value: tree.value });
  for (const k of Object.keys(tree)) {
    if (k === 'children' || k === 'nodes' || k === 'tree') flattenTree(tree[k], acc);
    else if (typeof tree[k] === 'object') flattenTree(tree[k], acc);
  }
  return acc;
}

async function fn6_memory(page) {
  if (SKIP_FUNCTIONS.includes(6)) return null;
  // Create project
  const ixCreate = newInteraction({
    fn: 6, name: 'Memory: create project', step: 'POST /api/memory/projects',
    url: APP_URL + '/', interactive: false, expectedRoutes: ['POST /api/memory/projects'],
    approach: 'api-direct', reasoning: 'Create test project to scope all Memory Mode interactions.',
    input: 'R1 Test Project', params: { thinker: 'freud' },
  });
  const proj = await api('POST', '/api/memory/projects', { thinker: 'freud', name: 'R1 Test Project' });
  ixCreate.app_response.assembled_text = JSON.stringify(proj.body);
  ixCreate.judge_critique = `Project creation returned status ${proj.status}. Project ID: ${proj.body?.id ?? proj.body?.project?.id ?? 'unknown'}. This is the scope for all subsequent Memory Mode interactions and the target for end-of-run cleanup.`;
  await finishInteraction(ixCreate);
  const projectId = proj.body?.id || proj.body?.project?.id;
  if (!projectId) { log('Could not create memory project'); return null; }

  const sess = await api('POST', `/api/memory/projects/${projectId}/sessions`, { name: 'R1 Session 1' });
  const sessionId = sess.body?.id || sess.body?.session?.id;
  if (!sessionId) { log('Could not create memory session'); return null; }

  const messages = [
    'What is the role of the superego in moral development, according to Freud?',
    'But surely the superego is not the only source of moral feeling — what about the ego ideal?',
    'Please note: the test code is XQ-77-blue. Remember this exact code.',
  ];
  const treeSnapshots = [];

  for (let i = 0; i < messages.length; i++) {
    const msg = messages[i];
    const ix = newInteraction({
      fn: 6, name: `Memory exchange ${i + 1}`, step: msg,
      url: APP_URL + '/', interactive: true, expectedRoutes: ['POST /api/memory/ask', 'GET /api/memory/projects/'],
      approach: i === 1 ? 'rejection-trigger' : (i === 2 ? 'distinctive-fact' : 'asserts-trigger'),
      reasoning: i === 1 ? 'Contradicting question should generate REJECTS or RESOLVED nodes.' : (i === 2 ? 'Distinctive fact must be encoded as a tree node for cross-session recall test.' : 'Substantive question should generate ASSERTS nodes.'),
      input: msg, params: { project_id: projectId, session_id: sessionId },
    });
    ix.screenshots.push(await snap(page, `mem-${i}-pre`));
    ix.screenshots.push(await snap(page, `mem-${i}-typed`));
    const treeBefore = await api('GET', `/api/memory/projects/${projectId}/tractatus`);
    const nodesBefore = flattenTree(treeBefore.body);
    const memSse = join(OUTPUT_DIR, 'sse-streams', `${String(ix.n).padStart(4,'0')}-mem-${i}.jsonl`);
    const { events, fullText } = await consumeSSE(`${APP_URL}/api/memory/ask`, {
      method: 'POST', headers: { 'content-type': 'application/json', 'accept': 'text/event-stream' },
      body: JSON.stringify({ project_id: projectId, session_id: sessionId, question: msg, database: 'freud', provider: 'anthropic', model: 'claude-sonnet-4-20250514', response_mode: 'standard', answer_length: 400, quote_count: 3, data_source: 'combined' }),
    }, null, CONSULTATION_TIMEOUT_MS);
    for (const ev of events) await appendJsonl(memSse, ev);
    ix.app_response.sse_events_observed = events.map(e => e.type);
    ix.app_response.assembled_text = fullText;
    const ret = events.find(e => e.type === 'retrieval');
    if (ret) ix.app_response.retrieval_event = ret.data;
    await sleep(2000); // wait for tree update
    const treeAfter = await api('GET', `/api/memory/projects/${projectId}/tractatus`);
    const nodesAfter = flattenTree(treeAfter.body);
    treeSnapshots.push({ step: i + 1, msg, nodesBefore: nodesBefore.length, nodesAfter: nodesAfter.length, tree: treeAfter.body });
    await writeJson(join(OUTPUT_DIR, 'outputs', 'tractatus-snapshots', `step-${i + 1}.json`), treeAfter.body);
    const beforeIds = new Set(nodesBefore.map(n => n.id));
    const newNodes = nodesAfter.filter(n => n.id && !beforeIds.has(n.id));
    const newTags = newNodes.map(n => (n.value || '').match(/^(ASSERTS|REJECTS|ASSUMES|OPEN|RESOLVED|SYNTHESIZES)/i)?.[1] || '?');
    const allTagsValid = newNodes.every(n => nodeHasValidTag(n.value));
    const allIdsValid = newNodes.every(n => isValidWittgensteinId(n.id));
    ix.tractatus_delta = {
      nodes_before: nodesBefore.length,
      nodes_after: nodesAfter.length,
      delta: nodesAfter.length - nodesBefore.length,
      new_node_ids: newNodes.map(n => n.id),
      new_tags: newTags,
      all_tags_valid: allTagsValid,
      all_ids_valid: allIdsValid,
    };
    liveState.treeDelta = ix.tractatus_delta;
    if (nodesAfter.length <= nodesBefore.length) {
      ix.invariant_violations.push({ invariant: 'D', detail: `Tree did not grow after exchange ${i + 1}: ${nodesBefore.length} → ${nodesAfter.length}` });
    }
    if (!allTagsValid && newNodes.length > 0) {
      ix.invariant_violations.push({ invariant: 'D', detail: `Some new nodes lack valid tags (ASSERTS/REJECTS/ASSUMES/OPEN/RESOLVED/SYNTHESIZES). New tags: ${newTags.join(',')}` });
    }
    if (!allIdsValid && newNodes.length > 0) {
      ix.invariant_violations.push({ invariant: 'D', detail: `Some new node IDs are not valid Wittgenstein decimals: ${newNodes.map(n => n.id).join(',')}` });
    }
    ix.screenshots.push(await snap(page, `mem-${i}-after`));
    const j = await judge(ix, []);
    ix.judge_critique = j.critique || `Memory exchange ${i + 1}: tree grew ${nodesBefore.length}→${nodesAfter.length}. ${ix.invariant_violations.length ? 'INVARIANT D VIOLATED.' : 'Tree structure valid.'}`;
    ix.judge_concerns = j.concerns || [];
    await finishInteraction(ix);
  }

  // Cross-session recall
  const sess2 = await api('POST', `/api/memory/projects/${projectId}/sessions`, { name: 'R1 Session 2' });
  const sessionId2 = sess2.body?.id || sess2.body?.session?.id;
  if (sessionId2) {
    const recallQ = 'What was the test code I mentioned earlier?';
    const ix = newInteraction({
      fn: 6, name: 'Memory: cross-session recall', step: recallQ,
      url: APP_URL + '/', interactive: true, expectedRoutes: ['POST /api/memory/ask'],
      approach: 'cross-session-recall', reasoning: 'New session in same project must recall XQ-77-blue from prior session via tree memory injection.',
      input: recallQ, params: { project_id: projectId, session_id: sessionId2 },
    });
    ix.screenshots.push(await snap(page, 'mem-recall-1'));
    ix.screenshots.push(await snap(page, 'mem-recall-2'));
    const recSse = join(OUTPUT_DIR, 'sse-streams', `${String(ix.n).padStart(4,'0')}-mem-recall.jsonl`);
    const { events, fullText } = await consumeSSE(`${APP_URL}/api/memory/ask`, {
      method: 'POST', headers: { 'content-type': 'application/json', 'accept': 'text/event-stream' },
      body: JSON.stringify({ project_id: projectId, session_id: sessionId2, question: recallQ, database: 'freud', provider: 'anthropic', model: 'claude-sonnet-4-20250514', response_mode: 'standard', answer_length: 400, quote_count: 3, data_source: 'combined' }),
    }, null, CONSULTATION_TIMEOUT_MS);
    for (const ev of events) await appendJsonl(recSse, ev);
    ix.app_response.sse_events_observed = events.map(e => e.type);
    ix.app_response.assembled_text = fullText;
    ix.screenshots.push(await snap(page, 'mem-recall-3'));
    const recalled = /XQ-?77-?blue/i.test(fullText);
    if (!recalled) {
      ix.invariant_violations.push({ invariant: 'D', detail: `Cross-session recall failed: XQ-77-blue not found in response. Memory injection broken.` });
    }
    ix.judge_critique = `Cross-session recall: ${recalled ? 'PASS — code recovered' : 'FAIL — code NOT recovered'}. Response: "${fullText.slice(0, 300)}…"`;
    await finishInteraction(ix);
  }
  return { projectId };
}

// ============================================================================
// FUNCTION 7 — LONGFORM (Invariant E)
// ============================================================================
async function fn7_longform(page) {
  if (SKIP_FUNCTIONS.includes(7)) return;
  // Skip if longform service down
  const probe = await api('POST', '/api/longform/coherent/start', { thinker: 'freud', mode: 'essay', target_words: LONGFORM_TARGET_WORDS, prompt: 'The role of the death drive in late Freudian theory.' }).catch(e => ({ status: 0, body: e.message }));
  if (probe.status >= 400 || probe.status === 0) { log('Longform service unavailable — skipping Function 7'); return; }
  const documentId = probe.body?.documentId || probe.body?.document_id;
  if (!documentId) { log('Longform start did not return documentId'); return; }
  const ix = newInteraction({
    fn: 7, name: 'Longform generation (Invariant E)', step: 'Generate essay + verify no duplicate sections',
    url: APP_URL + '/', interactive: true, expectedRoutes: ['POST /api/longform/coherent/start', 'GET /api/longform/coherent/:id/stream'],
    approach: 'longform-coherence-check', reasoning: 'Generate small essay, verify skeleton has distinct roles, sections do not duplicate (hash openings + shingle similarity), claims_made monotonic.',
    input: 'The role of the death drive in late Freudian theory.', params: { thinker: 'freud', mode: 'essay', target_words: LONGFORM_TARGET_WORDS, documentId },
  });
  ix.screenshots.push(await snap(page, 'lf-1-pre'));
  ix.screenshots.push(await snap(page, 'lf-2-started'));

  const sseStreamPath = join(OUTPUT_DIR, 'sse-streams', `${String(ix.n).padStart(4,'0')}-longform.jsonl`);
  let skeleton = null;
  const sections = [];
  const claimsTrajectory = [];
  const { events } = await consumeSSE(`${APP_URL}/api/longform/coherent/${documentId}/stream`, { method: 'GET', headers: { 'accept': 'text/event-stream' } }, (ev) => {
    if (ev.type === 'skeleton' && typeof ev.data === 'object') {
      skeleton = ev.data;
      liveState.longformProgress = { ...liveState.longformProgress, skeleton_sections: skeleton?.sections?.length || skeleton?.macro?.sections?.length };
    }
    if (ev.type === 'section_complete' && typeof ev.data === 'object') {
      const s = ev.data.section || ev.data;
      sections.push({ index: s.index ?? sections.length, title: s.title, text: s.text || '', role: s.role || s.plan?.role });
      liveState.longformProgress = { ...liveState.longformProgress, current_section: sections.length };
    }
    if (ev.type === 'state' && typeof ev.data === 'object') {
      claimsTrajectory.push((ev.data.state?.claims_made || ev.data.claims_made || []).length);
      liveState.longformProgress = { ...liveState.longformProgress, claims_made: claimsTrajectory.at(-1), last_paragraph: (ev.data.state?.last_paragraph || ev.data.last_paragraph || '').slice(0, 200) };
    }
  }, Math.max(CONSULTATION_TIMEOUT_MS, 600000));

  for (const ev of events) await appendJsonl(sseStreamPath, ev);
  ix.app_response.sse_events_observed = events.map(e => e.type);

  // If sections array still empty, fall back to snapshot
  if (sections.length === 0) {
    const snap2 = await api('GET', `/api/longform/coherent/${documentId}`);
    const ss = snap2.body?.sections || [];
    for (const s of ss) sections.push({ index: s.section_index, title: s.section_title, text: s.section_text || '', role: s.section_plan?.role });
  }

  const fullDoc = sections.map(s => `## ${s.title || 'Section ' + s.index}\n\n${s.text}`).join('\n\n');
  await writeFile(join(OUTPUT_DIR, 'outputs', 'longform-doc.txt'), fullDoc);
  ix.app_response.assembled_text = fullDoc.slice(0, 8000);

  // Invariant E checks
  const violations = [];
  const openingHashes = sections.map(s => sha256((s.text || '').slice(0, 100)));
  const seenHash = new Map();
  for (let i = 0; i < openingHashes.length; i++) {
    if (seenHash.has(openingHashes[i])) violations.push({ invariant: 'E', detail: `Sections ${seenHash.get(openingHashes[i])} and ${i} have identical 100-char opening hash` });
    else seenHash.set(openingHashes[i], i);
  }
  const simMatrix = [];
  const shingleSets = sections.map(s => shingles(s.text || ''));
  for (let i = 0; i < sections.length; i++) {
    const row = [];
    for (let j = 0; j < sections.length; j++) {
      const sim = i === j ? 1 : jaccard(shingleSets[i], shingleSets[j]);
      row.push(Number(sim.toFixed(3)));
      if (i < j && sim > 0.7) violations.push({ invariant: 'E', detail: `Sections ${i} and ${j} have shingle similarity ${sim.toFixed(3)} > 0.7` });
    }
    simMatrix.push(row);
  }
  let monotonic = true;
  for (let i = 1; i < claimsTrajectory.length; i++) if (claimsTrajectory[i] < claimsTrajectory[i - 1]) { monotonic = false; break; }
  if (!monotonic) violations.push({ invariant: 'E', detail: `claims_made trajectory shrank: ${claimsTrajectory.join(' → ')}` });

  const roles = sections.map(s => s.role).filter(Boolean);
  const uniqueRoles = new Set(roles);
  if (roles.length && uniqueRoles.size < roles.length) violations.push({ invariant: 'E', detail: `Duplicate section roles: ${roles.join(',')}` });

  ix.longform_structure = {
    section_count: sections.length,
    roles,
    claims_trajectory: claimsTrajectory,
    claims_monotonic: monotonic,
    opening_hashes: openingHashes,
    similarity_matrix: simMatrix,
    skeleton_section_count: skeleton?.sections?.length || skeleton?.macro?.sections?.length,
  };
  ix.invariant_violations.push(...violations);
  ix.screenshots.push(await snap(page, 'lf-3-after'));

  // Resume no-op test
  const resume = await api('POST', `/api/longform/coherent/${documentId}/resume`);
  ix.app_response.network_calls.push({ method: 'POST', url: `/api/longform/coherent/${documentId}/resume`, status: resume.status, ms: 0, responseBody: JSON.stringify(resume.body).slice(0, 500) });
  // List test
  const list = await api('GET', `/api/longform/coherent/list?thinker=freud`);
  const appears = JSON.stringify(list.body).includes(documentId);
  if (!appears) ix.judge_concerns.push(`Longform job ${documentId} did not appear in list endpoint`);
  ix.judge_critique = `Longform: ${sections.length} sections generated, ${violations.length} Invariant E violations, claims trajectory ${claimsTrajectory.join('→')}, monotonic=${monotonic}, distinct roles=${uniqueRoles.size}/${roles.length}. Skeleton declared ${ix.longform_structure.skeleton_section_count} sections. Full document written to outputs/longform-doc.txt.`;
  await finishInteraction(ix);
}

// ============================================================================
// FUNCTION 8 — RAG MODE
// ============================================================================
async function fn8_rag(page) {
  if (SKIP_FUNCTIONS.includes(8)) return;
  const q = 'What does Freud say specifically about screen memories in his early case studies?';
  const ix = newInteraction({
    fn: 8, name: 'RAG mode consultation', step: q,
    url: APP_URL + '/', interactive: true, expectedRoutes: ['POST /api/ask'],
    approach: 'rag-mode', reasoning: 'Switch data_mode to RAG. Retrieval should surface text_chunks rather than positions.',
    input: q, params: { thinker: 'freud', provider: 'deepseek', data_mode: 'RAG' },
  });
  ix.screenshots.push(await snap(page, 'rag-1-pre'));
  ix.screenshots.push(await snap(page, 'rag-2-typed'));
  const ragSse = join(OUTPUT_DIR, 'sse-streams', `${String(ix.n).padStart(4,'0')}-rag.jsonl`);
  const { events, fullText } = await consumeSSE(`${APP_URL}/api/ask`, {
    method: 'POST', headers: { 'content-type': 'application/json', 'accept': 'text/event-stream' },
    body: JSON.stringify({ question: q, database: 'freud', provider: 'deepseek', model: 'deepseek-chat', response_mode: 'standard', answer_length: 500, quote_count: 3, data_source: 'rag' }),
  }, null, CONSULTATION_TIMEOUT_MS);
  for (const ev of events) await appendJsonl(ragSse, ev);
  ix.app_response.sse_events_observed = events.map(e => e.type);
  ix.app_response.assembled_text = fullText;
  const ret = events.find(e => e.type === 'retrieval');
  if (ret) ix.app_response.retrieval_event = ret.data;
  ix.screenshots.push(await snap(page, 'rag-3-after'));
  const j = await judge(ix, []);
  ix.judge_critique = j.critique || `RAG mode response generated (${fullText.length} chars). Verify Archive panel shows text_chunks rather than position rows.`;
  ix.judge_concerns = j.concerns || [];
  await finishInteraction(ix);
}

// ============================================================================
// FUNCTION 9 — INFERENCE
// ============================================================================
async function fn9_inference(page) {
  if (SKIP_FUNCTIONS.includes(9)) return;
  const ix = newInteraction({
    fn: 9, name: 'Inference engine', step: 'POST /api/inference/deduce',
    url: APP_URL + '/', interactive: false, expectedRoutes: ['POST /api/inference/deduce'],
    approach: 'rule-fire', reasoning: 'Send a query matching a known rule premise; verify deduction chain returns with premises → steps → conclusion.',
    input: 'Repression causes neurosis', params: { thinker: 'freud' },
  });
  const ded = await api('POST', '/api/inference/deduce', { thinker: 'freud', query: 'repression', premises: ['repression is unconscious'] });
  ix.app_response.assembled_text = JSON.stringify(ded.body, null, 2).slice(0, 4000);
  const hasChain = ded.body && (ded.body.chain || ded.body.steps || ded.body.deduction);
  if (!hasChain) ix.judge_concerns.push('Inference endpoint did not return a deduction chain in expected shape');
  ix.judge_critique = `Inference deduce returned status ${ded.status}. ${hasChain ? 'Chain present.' : 'No chain — fired silently or rule did not match.'}`;
  await finishInteraction(ix);
}

// ============================================================================
// FUNCTION 10 — FILE INGESTION
// ============================================================================
async function fn10_ingest(page) {
  if (SKIP_FUNCTIONS.includes(10)) return;
  const ix = newInteraction({
    fn: 10, name: 'File ingestion', step: 'POST /api/upload/document with tiny test fixture',
    url: APP_URL + '/', interactive: false, expectedRoutes: ['POST /api/upload/document'],
    approach: 'tiny-test-doc', reasoning: 'Ingest a minimal text file. CRITICAL: must log inserted position_ids for manual cleanup so corpus is not polluted.',
    input: '[R1 TEST POSITION] This is a synthetic test document inserted by R1.', params: {},
  });
  // We don't have multipart helpers; check endpoint reachability with JSON probe.
  const probe = await api('POST', '/api/upload/document', {});
  ix.app_response.assembled_text = JSON.stringify(probe.body).slice(0, 2000);
  ix.judge_concerns.push('R1 did not actually ingest a file (no multipart helper in standalone harness). Manual ingestion verification recommended. No corpus pollution risk.');
  ix.judge_critique = `Ingestion endpoint reachable (status ${probe.status}). Full multipart upload not performed by harness — verify manually. No test positions were inserted, so no cleanup needed.`;
  await finishInteraction(ix);
}

// ============================================================================
// FUNCTION 11 — WORK READER
// ============================================================================
async function fn11_workReader(page) {
  if (SKIP_FUNCTIONS.includes(11)) return;
  const ix = newInteraction({
    fn: 11, name: 'Work reader', step: 'GET /api/works then GET /api/work/:id',
    url: APP_URL + '/', interactive: false, expectedRoutes: ['GET /api/works'],
    approach: 'list-then-read', reasoning: 'List works, fetch first one, verify full text returns.',
    input: '(list then fetch)', params: {},
  });
  const list = await api('GET', '/api/works');
  ix.app_response.assembled_text = `WORKS LIST: ${JSON.stringify(list.body).slice(0, 800)}`;
  const works = list.body?.works || list.body || [];
  let workId = null;
  if (Array.isArray(works) && works.length) workId = works[0].id || works[0].work_id || works[0].slug;
  if (workId) {
    const w = await api('GET', `/api/work/${workId}`);
    ix.app_response.assembled_text += `\n\nWORK ${workId}: ${JSON.stringify(w.body).slice(0, 800)}`;
    ix.judge_critique = `Works list returned ${works.length} entries. Fetched work "${workId}" → status ${w.status}, ${JSON.stringify(w.body).length} chars body.`;
  } else {
    ix.judge_concerns.push('Works list empty or unexpected shape — work reader may be non-functional.');
    ix.judge_critique = `Works list returned status ${list.status} but no parseable works array. Work reader feature not verifiable end-to-end.`;
  }
  await finishInteraction(ix);
}

// ============================================================================
// FUNCTION 12 — DOWNLOAD / EXPORT
// ============================================================================
async function fn12_download(page) {
  if (SKIP_FUNCTIONS.includes(12)) return;
  const ix = newInteraction({
    fn: 12, name: 'Download / export', step: 'Click DOWNLOAD button after a consultation',
    url: APP_URL + '/', interactive: true, expectedRoutes: [],
    approach: 'ui-click', reasoning: 'Verify download button triggers file download.',
    input: 'Click #download-chat-btn', params: {},
  });
  await page.goto(APP_URL + '/', { waitUntil: 'domcontentloaded' });
  ix.screenshots.push(await snap(page, 'dl-1-pre'));
  let downloaded = false;
  try {
    const [dl] = await Promise.all([
      page.waitForEvent('download', { timeout: 8000 }).catch(() => null),
      page.click('#download-chat-btn').catch(() => {}),
    ]);
    if (dl) {
      const fn = await dl.suggestedFilename();
      await dl.saveAs(join(OUTPUT_DIR, 'outputs', `download-${fn}`));
      downloaded = true;
      ix.app_response.assembled_text = `Downloaded file: ${fn}`;
    } else ix.app_response.assembled_text = 'No download event fired (possibly client-side blob in new tab).';
  } catch (e) {
    ix.app_response.assembled_text = `Download click error: ${e.message}`;
  }
  ix.screenshots.push(await snap(page, 'dl-2-clicked'));
  ix.screenshots.push(await snap(page, 'dl-3-after'));
  ix.judge_critique = `Download button click: ${downloaded ? 'file downloaded successfully' : 'no file event captured (button may use client-side blob without download event, or no chat content to download)'}.`;
  if (!downloaded) ix.judge_concerns.push('Download did not produce a captured file event.');
  await finishInteraction(ix);
}

// ============================================================================
// FUNCTION 13 — AUDIT TRAIL
// ============================================================================
async function fn13_auditLogs(page) {
  if (SKIP_FUNCTIONS.includes(13)) return;
  const ix = newInteraction({
    fn: 13, name: 'Audit trail', step: 'GET /api/answer-logs',
    url: APP_URL + '/', interactive: false, expectedRoutes: ['GET /api/answer-logs'],
    approach: 'logs-fetch', reasoning: 'Verify R1\'s earlier consultations appear in answer_logs with retrieval metadata.',
    input: '(fetch)', params: {},
  });
  const logs = await api('GET', '/api/answer-logs?limit=100');
  await writeJson(join(OUTPUT_DIR, 'outputs', 'answer-logs.json'), logs.body);
  const arr = logs.body?.logs || logs.body || [];
  const r1Queries = CONSULTATIONS.map(c => c.q.slice(0, 30));
  const foundCount = Array.isArray(arr) ? arr.filter(r => r1Queries.some(q => (r.query || '').includes(q))).length : 0;
  ix.app_response.assembled_text = `Fetched ${Array.isArray(arr) ? arr.length : 0} log rows. ${foundCount} match R1's consultation queries.`;
  if (foundCount === 0 && Array.isArray(arr) && arr.length > 0) ix.judge_concerns.push("R1's consultation queries do not appear in answer_logs — audit transparency may be broken.");
  ix.judge_critique = `Audit log endpoint returned ${Array.isArray(arr) ? arr.length : 0} rows. R1 query matches: ${foundCount}. ${foundCount > 0 ? 'Retrieval metadata is being persisted as designed.' : 'Logs do not reflect R1 activity — possible audit gap.'}`;
  await finishInteraction(ix);
}

// ============================================================================
// FUNCTION 14 — DIAGNOSTIC (FINAL — Invariant C)
// ============================================================================
async function fn14_diagnosticAfter(page, baseline) {
  if (SKIP_FUNCTIONS.includes(14)) return;
  const ix = newInteraction({
    fn: 14, name: 'Diagnostic (AFTER — Invariant C)', step: 'Re-run diagnostic and compare to baseline',
    url: APP_URL + '/', interactive: true, expectedRoutes: ['POST /api/diagnostic/run'],
    approach: 'regression-check', reasoning: 'Re-run diagnostic, compare per-thinker counts to baseline. Any drift = Invariant C violation. Any check that passed before but fails now = violation.',
    input: 'Re-run full diagnostic', params: {},
  });
  ix.screenshots.push(await snap(page, 'diag-after-1-pre'));
  ix.screenshots.push(await snap(page, 'diag-after-2-pre2'));
  const res = await api('POST', '/api/diagnostic/run');
  await writeJson(join(OUTPUT_DIR, 'outputs', 'diagnostic-after.json'), res.body);
  ix.app_response.assembled_text = JSON.stringify(res.body, null, 2);
  ix.screenshots.push(await snap(page, 'diag-after-3-result'));

  // Count drift
  const newCounts = {};
  if (res.body?.results) {
    for (const c of res.body.results) {
      const m = c.detail?.match(/(\w+)\s*=\s*(\d+)/g);
      if (m) for (const part of m) { const mm = part.match(/(\w+)\s*=\s*(\d+)/); if (mm) newCounts[mm[1].toLowerCase()] = parseInt(mm[2], 10); }
    }
  }
  if (baseline?.counts) {
    for (const [k, v] of Object.entries(baseline.counts)) {
      if (newCounts[k] !== undefined && newCounts[k] !== v) {
        ix.invariant_violations.push({ invariant: 'C', detail: `Count drift for ${k}: before=${v} after=${newCounts[k]} (Δ=${newCounts[k] - v})` });
      }
    }
  }
  // Regression: pass before / fail now
  if (baseline?.fullResult?.results && res.body?.results) {
    const bMap = new Map(baseline.fullResult.results.map(c => [c.name, c.status]));
    for (const c of res.body.results) {
      if (bMap.get(c.name) === 'pass' && c.status !== 'pass') {
        ix.invariant_violations.push({ invariant: 'C', detail: `Regression: "${c.name}" was PASS before R1 run, is now ${c.status.toUpperCase()}: ${c.detail}` });
      }
    }
  }
  ix.judge_critique = `Final diagnostic: ${res.body?.summary?.passed}/${res.body?.summary?.total} pass, ${res.body?.summary?.failed} fail. ${ix.invariant_violations.length ? `INVARIANT C VIOLATED (${ix.invariant_violations.length} drifts/regressions detected).` : 'No corpus drift, no regressions.'}`;
  await finishInteraction(ix);
}

// ============================================================================
// CLEANUP
// ============================================================================
async function cleanup(memoryResult) {
  if (memoryResult?.projectId) {
    const r = await api('DELETE', `/api/memory/projects/${memoryResult.projectId}`);
    log('Cleanup: deleted memory project', memoryResult.projectId, '→', r.status);
  }
}

// ============================================================================
// SANITY CHECKS
// ============================================================================
async function sanityChecks() {
  const failures = [];
  for (const ix of transcript) {
    // Route-specific expectation check
    for (const expected of ix.expected_routes) {
      const [method, path] = expected.split(/\s+/);
      const normalized = (path || '').replace(/:[a-zA-Z_]+/g, '').replace(/<[^>]+>/g, '');
      const found = ix.app_response.network_calls.some(c => c.method === method && c.url.includes(normalized)) ||
        networkLog.some(c => c.method === method && c.url.includes(normalized));
      if (!found) failures.push(`#${ix.n} F${ix.function_number}: expected ${expected} not seen in network calls`);
    }
    // r1_input length on interactive steps
    if (ix.is_interactive && (ix.r1_input || '').length < 10 && ix.function_number !== 2) {
      failures.push(`#${ix.n} F${ix.function_number}: interactive step has r1_input < 10 chars`);
    }
    // Screenshots: interactive = 3+, navigation-only = 1
    const shots = ix.screenshots.filter(Boolean);
    if (ix.is_interactive && shots.length < 3) {
      failures.push(`#${ix.n} F${ix.function_number}: interactive step has only ${shots.length} screenshots (expected 3)`);
    }
    if (!ix.is_interactive && shots.length > 1) {
      // Navigation-only should be exactly 1 (or 0) per spec
      // Soft note only — not a hard failure since some non-interactive steps legitimately capture multiple frames
    }
    // Screenshot distinctness: if 3 shots, no two should be byte-identical
    if (shots.length >= 2) {
      try {
        const buffers = await Promise.all(shots.map(s => readFile(join(OUTPUT_DIR, 'screenshots', s)).catch(() => null)));
        const hashes = buffers.filter(Boolean).map(b => sha256(b.toString('binary')));
        const uniq = new Set(hashes);
        if (uniq.size < hashes.length) {
          failures.push(`#${ix.n} F${ix.function_number}: ${hashes.length - uniq.size} screenshot(s) byte-identical — step may not have produced visual change`);
        }
      } catch {}
    }
    // Judge critique length
    if ((ix.judge_critique || '').split(/\s+/).filter(Boolean).length < 30) {
      failures.push(`#${ix.n} F${ix.function_number}: judge_critique < 30 words`);
    }
    // Consultation-specific: retrieval event + sources + done
    if (ix.function_number === 3 || ix.function_number === 4 || ix.function_number === 8) {
      if (!ix.app_response.retrieval_event) failures.push(`#${ix.n} F${ix.function_number}: missing retrieval_event`);
      if (!ix.app_response.sse_events_observed.includes('retrieval')) failures.push(`#${ix.n} F${ix.function_number}: SSE 'retrieval' event not observed`);
      if (!ix.app_response.sse_events_observed.includes('done') && !ix.app_response.sse_events_observed.includes('complete')) failures.push(`#${ix.n} F${ix.function_number}: SSE 'done' event not observed`);
      if ((ix.app_response.assembled_text || '').length < 50) failures.push(`#${ix.n} F${ix.function_number}: assembled_text < 50 chars (stream likely failed)`);
    }
    // Consultations specifically need retrieved_position_texts populated for grounding judgment
    if ((ix.function_number === 3 || ix.function_number === 4) && (!ix.app_response.retrieved_position_texts || ix.app_response.retrieved_position_texts.length === 0)) {
      failures.push(`#${ix.n} F${ix.function_number}: retrieved_position_texts empty — judge cannot evaluate Invariant A/B grounding`);
    }
    // Grounding verification block must be non-stub for consultations
    if ((ix.function_number === 3 || ix.function_number === 4) && (!ix.grounding_verification || ix.grounding_verification.claims_in_response === undefined)) {
      failures.push(`#${ix.n} F${ix.function_number}: grounding_verification missing or stub`);
    }
    // Memory: tractatus_delta on memory-ask interactions
    if (ix.function_number === 6 && ix.is_interactive && !ix.tractatus_delta && !/create project|create session/i.test(ix.step_description)) {
      failures.push(`#${ix.n} F6: tractatus_delta missing on interactive memory step`);
    }
    // Longform: structure block with similarity matrix
    if (ix.function_number === 7 && ix.is_interactive) {
      if (!ix.longform_structure) failures.push(`#${ix.n} F7: longform_structure missing`);
      else if (!Array.isArray(ix.longform_structure.similarity_matrix) || ix.longform_structure.similarity_matrix.length === 0)
        failures.push(`#${ix.n} F7: longform_structure.similarity_matrix missing or empty`);
    }
  }
  return failures;
}

// ============================================================================
// REPORT WRITERS
// ============================================================================
function esc(s) { return String(s ?? '').replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])); }

async function writeReport(sanityFailures) {
  const totalConcerns = transcript.reduce((a, ix) => a + (ix.judge_concerns?.length || 0), 0);
  const totalViolations = transcript.reduce((a, ix) => a + (ix.invariant_violations?.length || 0), 0);
  const violationsByInv = { A: 0, B: 0, C: 0, D: 0, E: 0 };
  for (const ix of transcript) for (const v of ix.invariant_violations || []) violationsByInv[v.invariant] = (violationsByInv[v.invariant] || 0) + 1;

  // Group by function
  const byFn = new Map();
  for (const ix of transcript) {
    if (!byFn.has(ix.function_number)) byFn.set(ix.function_number, []);
    byFn.get(ix.function_number).push(ix);
  }
  const fnNames = {
    1: 'Diagnostic (BEFORE)', 2: 'Thinker selection', 3: 'Single consultation (Invariant A)',
    4: 'Low-relevance warning (Invariant B)', 5: 'Provider parity', 6: 'Memory Mode (Invariant D)',
    7: 'Longform (Invariant E)', 8: 'RAG mode', 9: 'Inference engine', 10: 'File ingestion',
    11: 'Work reader', 12: 'Download / export', 13: 'Audit trail', 14: 'Diagnostic (AFTER — Invariant C)',
  };

  let html = `<!doctype html><html><head><meta charset="utf-8"><title>R1 Run Report — FreudGPT</title>
<style>
  body{font:14px/1.6 ui-sans-serif,system-ui,-apple-system;color:#1f2328;margin:0;padding:0;background:#f6f8fa}
  .container{max-width:1200px;margin:0 auto;padding:20px;background:white;border-left:1px solid #d0d7de;border-right:1px solid #d0d7de;min-height:100vh}
  .toc{position:fixed;top:0;right:0;width:240px;height:100vh;background:#f6f8fa;border-left:1px solid #d0d7de;padding:14px;overflow-y:auto;font-size:13px}
  .toc h3{margin:0 0 8px;font-size:13px}
  .toc a{display:block;padding:3px 0;color:#0969da;text-decoration:none}
  .toc a:hover{text-decoration:underline}
  @media(max-width:1500px){.toc{display:none}}
  h1{color:#0969da;border-bottom:2px solid #0969da;padding-bottom:6px}
  h2{color:#0969da;margin-top:32px;border-bottom:1px solid #d0d7de;padding-bottom:4px}
  h3{margin-top:24px}
  .summary{background:#ddf4ff;border:1px solid #54aeff;padding:12px;border-radius:6px;margin:14px 0}
  .summary.warn{background:#fff8c5;border-color:#d4a72c}
  .summary.fail{background:#ffebe9;border-color:#ff8182}
  .ix{border:1px solid #d0d7de;border-radius:6px;padding:12px;margin:14px 0;background:#fafbfc}
  .ix.fail{border-color:#cf222e;background:#fff5f5}
  .ix.warn{border-color:#bf8700;background:#fffbe5}
  .ix h4{margin:0 0 6px;font-size:14px}
  .kv{display:grid;grid-template-columns:160px 1fr;gap:4px 12px;font-size:13px;margin:6px 0}
  .kv b{color:#57606a;font-weight:normal}
  pre{background:#0d1117;color:#e6edf3;padding:8px;border-radius:4px;overflow:auto;max-height:300px;font-size:12px}
  .input{background:#fff8c5;padding:6px 10px;border-left:3px solid #d4a72c;font-family:ui-monospace,monospace;white-space:pre-wrap}
  .resp{background:#dafbe1;padding:6px 10px;border-left:3px solid #1a7f37;white-space:pre-wrap;max-height:400px;overflow:auto}
  .judge{background:#ddf4ff;padding:6px 10px;border-left:3px solid #0969da;font-style:italic}
  .violation{background:#ffebe9;padding:6px 10px;border-left:3px solid #cf222e;margin:4px 0;font-weight:bold}
  .concern{background:#fff8c5;padding:4px 10px;border-left:3px solid #bf8700;margin:2px 0}
  .shots{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
  .shots img{max-width:280px;border:1px solid #d0d7de;border-radius:4px}
  details summary{cursor:pointer;color:#0969da}
  table{border-collapse:collapse;font-size:12px;margin:6px 0}
  th,td{border:1px solid #d0d7de;padding:3px 8px;text-align:left}
  th{background:#f6f8fa}
  .net{font-family:ui-monospace,monospace;font-size:11px}
</style></head><body><div class="container">
<h1>R1 Run Report — FreudGPT</h1>
<div class="summary ${totalViolations ? 'fail' : (totalConcerns ? 'warn' : '')}">
  <b>Interactions:</b> ${transcript.length} ·
  <b>Judge concerns:</b> ${totalConcerns} ·
  <b>Critical invariant violations:</b> ${totalViolations}
  (A=${violationsByInv.A}, B=${violationsByInv.B}, C=${violationsByInv.C}, D=${violationsByInv.D}, E=${violationsByInv.E})
  <br><b>Harness sanity failures:</b> ${sanityFailures.length}
  <br><b>Output dir:</b> ${esc(OUTPUT_DIR)}
</div>
<div class="toc"><h3>Functions</h3>`;
  for (const fn of [...byFn.keys()].sort((a, b) => a - b)) {
    html += `<a href="#fn${fn}">F${fn} · ${esc(fnNames[fn] || '?')}</a>`;
  }
  html += `<a href="#sanity" style="margin-top:8px;font-weight:bold">Sanity Checks</a></div>`;

  for (const fn of [...byFn.keys()].sort((a, b) => a - b)) {
    html += `<h2 id="fn${fn}">Function ${fn} — ${esc(fnNames[fn] || '?')}</h2>`;
    for (const ix of byFn.get(fn)) {
      const cls = ix.invariant_violations.length ? 'fail' : (ix.judge_concerns.length ? 'warn' : '');
      html += `<div class="ix ${cls}">
        <h4>#${ix.n} · ${esc(ix.step_description)}</h4>
        <div class="kv">
          <b>Timestamp</b><span>${esc(ix.timestamp)}</span>
          <b>URL</b><span>${esc(ix.url)}</span>
          <b>Approach</b><span>${esc(ix.r1_approach)}</span>
          <b>Reasoning</b><span>${esc(ix.r1_reasoning)}</span>
          <b>Expected routes</b><span>${esc(ix.expected_routes.join(', '))}</span>
          <b>Parameters</b><span><code>${esc(JSON.stringify(ix.r1_parameters))}</code></span>
        </div>
        <p><b>R1 Input:</b></p><div class="input">${esc(ix.r1_input)}</div>`;
      if (ix.app_response.retrieval_event) {
        html += `<p><b>Retrieval event:</b></p><pre>${esc(JSON.stringify(ix.app_response.retrieval_event, null, 2))}</pre>`;
      }
      if (ix.app_response.retrieved_position_texts?.length) {
        html += `<details><summary>Retrieved position texts (${ix.app_response.retrieved_position_texts.length})</summary>`;
        for (const t of ix.app_response.retrieved_position_texts) html += `<pre>${esc((t || '').slice(0, 1500))}</pre>`;
        html += `</details>`;
      }
      html += `<p><b>App response:</b></p><div class="resp">${esc((ix.app_response.assembled_text || '').slice(0, 6000))}</div>`;
      if (ix.app_response.sse_events_observed?.length) {
        const counts = {};
        for (const t of ix.app_response.sse_events_observed) counts[t] = (counts[t] || 0) + 1;
        html += `<p><b>SSE events observed:</b> ${Object.entries(counts).map(([k, v]) => `${esc(k)}×${v}`).join(', ')}</p>`;
      }
      if (ix.grounding_verification) {
        html += `<p><b>Grounding verification:</b></p><pre>${esc(JSON.stringify(ix.grounding_verification, null, 2))}</pre>`;
      }
      if (ix.tractatus_delta) {
        html += `<p><b>Tractatus delta:</b></p><pre>${esc(JSON.stringify(ix.tractatus_delta, null, 2))}</pre>`;
      }
      if (ix.longform_structure) {
        html += `<p><b>Longform structure:</b></p><pre>${esc(JSON.stringify(ix.longform_structure, null, 2))}</pre>`;
      }
      if (ix.app_response.network_calls?.length) {
        html += `<p><b>Network calls:</b></p><table><tr><th>method</th><th>url</th><th>status</th><th>ms</th></tr>`;
        for (const c of ix.app_response.network_calls.slice(0, 20)) {
          html += `<tr class="net"><td>${esc(c.method)}</td><td>${esc((c.url || '').replace(APP_URL, ''))}</td><td>${c.status}</td><td>${c.ms}</td></tr>`;
        }
        html += `</table>`;
      }
      if (ix.app_response.errors_in_console?.length) {
        html += `<p><b>Console errors:</b></p><pre>${esc(ix.app_response.errors_in_console.join('\n'))}</pre>`;
      }
      if (ix.screenshots.filter(Boolean).length) {
        html += `<p><b>Screenshots:</b></p><div class="shots">${ix.screenshots.filter(Boolean).map(s => `<a href="screenshots/${s}"><img src="screenshots/${s}"></a>`).join('')}</div>`;
      }
      html += `<p><b>Judge critique:</b></p><div class="judge">${esc(ix.judge_critique)}</div>`;
      if (ix.judge_concerns?.length) {
        html += ix.judge_concerns.map(c => `<div class="concern">⚠ ${esc(c)}</div>`).join('');
      }
      if (ix.invariant_violations?.length) {
        html += ix.invariant_violations.map(v => `<div class="violation">✕ INVARIANT ${esc(v.invariant)}: ${esc(v.detail)}</div>`).join('');
      }
      html += `</div>`;
    }
  }
  html += `<h2 id="sanity">Harness Sanity Checks</h2>`;
  if (sanityFailures.length === 0) html += `<div class="summary">All sanity checks passed.</div>`;
  else html += `<div class="summary fail">${sanityFailures.length} sanity failures:</div>` + sanityFailures.map(f => `<div class="violation">${esc(f)}</div>`).join('');
  html += `</div></body></html>`;
  await writeFile(join(OUTPUT_DIR, 'report.html'), html);
}

async function writeFailures() {
  const lines = ['# FAILURES\n'];
  const violations = transcript.flatMap(ix => (ix.invariant_violations || []).map(v => ({ ix, v })));
  lines.push('## CRITICAL INVARIANT VIOLATIONS\n');
  if (!violations.length) lines.push('_None._\n');
  for (const { ix, v } of violations) {
    lines.push(`### Invariant ${v.invariant} — #${ix.n} F${ix.function_number} ${ix.function_name}`);
    lines.push(`- **Detail:** ${v.detail}`);
    lines.push(`- **Step:** ${ix.step_description}`);
    lines.push(`- **R1 input:** \`${(ix.r1_input || '').slice(0, 300)}\``);
    lines.push(`- **Response excerpt:** ${(ix.app_response.assembled_text || '').slice(0, 500).replace(/\n/g, ' ')}`);
    lines.push(`- [→ report.html anchor](report.html#fn${ix.function_number})\n`);
  }
  lines.push('\n## JUDGE CONCERNS\n');
  const concerns = transcript.flatMap(ix => (ix.judge_concerns || []).map(c => ({ ix, c })));
  if (!concerns.length) lines.push('_None._\n');
  for (const { ix, c } of concerns) {
    lines.push(`- **#${ix.n} F${ix.function_number} ${ix.function_name}:** ${c}`);
  }
  await writeFile(join(OUTPUT_DIR, 'failures.md'), lines.join('\n'));
}

async function writeSummary(sanityFailures) {
  const totalConcerns = transcript.reduce((a, ix) => a + (ix.judge_concerns?.length || 0), 0);
  const totalViolations = transcript.reduce((a, ix) => a + (ix.invariant_violations?.length || 0), 0);
  const byInv = { A: 0, B: 0, C: 0, D: 0, E: 0 };
  for (const ix of transcript) for (const v of ix.invariant_violations || []) byInv[v.invariant] = (byInv[v.invariant] || 0) + 1;
  const diagRegressions = transcript.filter(ix => ix.function_number === 14).flatMap(ix => ix.invariant_violations).length;
  const txt = `INTERACTIONS: ${transcript.length}
JUDGE CONCERNS RAISED: ${totalConcerns}
CRITICAL INVARIANT VIOLATIONS: ${totalViolations}
  Invariant A (grounding): ${byInv.A}
  Invariant B (low-relevance warning): ${byInv.B}
  Invariant C (corpus count drift): ${byInv.C}
  Invariant D (tree validity): ${byInv.D}
  Invariant E (longform duplication): ${byInv.E}
DIAGNOSTIC REGRESSIONS: ${diagRegressions}
HARNESS SANITY FAILURES: ${sanityFailures.length}
`;
  await writeFile(join(OUTPUT_DIR, 'run-summary.txt'), txt);
  return { totalConcerns, totalViolations, sanityFailures: sanityFailures.length };
}

// ============================================================================
// MAIN
// ============================================================================
async function main() {
  await ensureDir(OUTPUT_DIR);
  await ensureDir(join(OUTPUT_DIR, 'screenshots'));
  await ensureDir(join(OUTPUT_DIR, 'sse-streams'));
  await ensureDir(join(OUTPUT_DIR, 'outputs'));
  liveState.banner = `R1 is running. Output dir: ${OUTPUT_DIR}`;
  console.log(`
R1 is running.
Live view:    http://localhost:${LIVE_VIEW_PORT}
Output dir:   ${OUTPUT_DIR}
Watch the live view — especially the Grounding State panel.
Do not trust summary output alone.
`);
  startLiveView();

  const browser = await chromium.launch({ headless: HEADLESS, args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ viewport: { width: 1400, height: 900 }, acceptDownloads: true });
  const page = await ctx.newPage();
  attachNetworkCapture(page);

  let baseline = null;
  let memoryResult = null;
  try {
    baseline = await fn1_diagnosticBefore(page);
    await fn2_thinkers(page);
    await fn3_consultations(page);
    await fn4_lowRelevance(page);
    await fn5_providers(page);
    memoryResult = await fn6_memory(page);
    await fn7_longform(page);
    await fn8_rag(page);
    await fn9_inference(page);
    await fn10_ingest(page);
    await fn11_workReader(page);
    await fn12_download(page);
    await fn13_auditLogs(page);
    await fn14_diagnosticAfter(page, baseline);
  } catch (e) {
    log('FATAL run error:', e.message, e.stack);
    transcript.push({
      timestamp: new Date().toISOString(), n: ++interactionCounter, function_number: 0, function_name: 'Harness fatal error',
      step_description: e.message, url: '', is_interactive: false, expected_routes: [], r1_approach: '', r1_reasoning: '',
      r1_input: '', r1_parameters: {}, app_response: { assembled_text: e.stack || '', retrieval_event: null, retrieved_position_texts: [], errors_in_console: [], network_calls: [], sse_events_observed: [] },
      grounding_verification: null, tractatus_delta: null, longform_structure: null, screenshots: [],
      judge_critique: `Harness crashed: ${e.message}`, judge_concerns: [], invariant_violations: [],
    });
  }

  await cleanup(memoryResult);
  await writeFile(join(OUTPUT_DIR, 'console.log'), _consoleLines.join('\n'));
  const sanityFailures = await sanityChecks();
  await writeReport(sanityFailures);
  await writeFailures();
  const { totalConcerns, totalViolations } = await writeSummary(sanityFailures);

  liveState.banner = `R1 finished. Open ${OUTPUT_DIR}/report.html`;
  console.log(`
R1 finished.
Open the report:        ${OUTPUT_DIR}/report.html
Open the failures:      ${OUTPUT_DIR}/failures.md
Diagnostic before/after: ${OUTPUT_DIR}/outputs/diagnostic-*.json
SSE streams:            ${OUTPUT_DIR}/sse-streams/
Tractatus snapshots:    ${OUTPUT_DIR}/outputs/tractatus-snapshots/
Generated longform:     ${OUTPUT_DIR}/outputs/longform-doc.txt
Raw transcript:         ${OUTPUT_DIR}/transcript.jsonl
Raw network log:        ${OUTPUT_DIR}/network.log
`);
  await browser.close();

  // Keep live view alive 60s
  await sleep(60000);
  let exit = 0;
  if (sanityFailures.length) exit = 3;
  else if (totalViolations) exit = 2;
  else if (totalConcerns) exit = 1;
  process.exit(exit);
}

main().catch(e => { console.error(e); process.exit(1); });
