const fs = require('fs');
const path = require('path');
const { createCanvas, GlobalFonts } = require('@napi-rs/canvas');

// ---------- fonts ----------
const FONTS = path.join(__dirname, 'fonts');
GlobalFonts.registerFromPath(path.join(FONTS, 'PlayfairDisplay.ttf'), 'Playfair');
GlobalFonts.registerFromPath(path.join(FONTS, 'PlayfairDisplay-Italic.ttf'), 'PlayfairItalic');
GlobalFonts.registerFromPath(path.join(FONTS, 'Inter.ttf'), 'Inter');

const SCALE = 1.5;
const VW = 1280, VH = 720;
const W = VW * SCALE, H = VH * SCALE;
const FPS = 30;
const DUR = 20.0;
const TOTAL = Math.round(DUR * FPS);
const OUT = path.join(__dirname, 'frames');

// ---------- palette (real app) ----------
const C = {
  coral: '#F97316',
  teal: '#0F766E',
  tealDeep: '#0B5650',
  tealBright: '#14B8A6',
  italicAccent: '#5EEAD4',
  mint: '#F0FDFA',
  ink: '#13212B',
  inkSoft: '#3A4A55',
  muted: '#6B7C8A',
  faint: '#9AA8B2',
  border: '#E3E9E8',
  appBg: '#FFFDFB',
  panelBg: '#FFFFFF',
};

// ---------- helpers ----------
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const easeOut = t => 1 - Math.pow(1 - t, 3);
const easeInOut = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const seg = (t, s, e) => clamp((t - s) / (e - s), 0, 1);

function rr(ctx, x, y, w, h, r) {
  r = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}
function setFont(ctx, family, size, weight) { ctx.font = `${weight || 400} ${size}px ${family}`; }
function lsText(ctx, text, cx, y, ls, align) {
  let total = 0;
  for (const ch of text) total += ctx.measureText(ch).width + ls;
  total -= ls;
  let x = align === 'center' ? cx - total / 2 : (align === 'right' ? cx - total : cx);
  for (const ch of text) { ctx.fillText(ch, x, y); x += ctx.measureText(ch).width + ls; }
  return total;
}
function wrap(ctx, text, maxW) {
  const words = text.split(' ');
  const lines = []; let line = '';
  for (const w of words) {
    const test = line ? line + ' ' + w : w;
    if (ctx.measureText(test).width > maxW && line) { lines.push(line); line = w; }
    else line = test;
  }
  if (line) lines.push(line);
  return lines;
}
function logo(ctx, cx, cy, s, alpha) {
  ctx.save();
  ctx.globalAlpha = alpha == null ? 1 : alpha;
  ctx.shadowColor = 'rgba(0,0,0,0.3)';
  ctx.shadowBlur = s * 0.26; ctx.shadowOffsetY = s * 0.07;
  const g = ctx.createLinearGradient(cx, cy - s / 2, cx, cy + s / 2);
  g.addColorStop(0, '#11968B'); g.addColorStop(1, '#0F766E');
  ctx.fillStyle = g;
  rr(ctx, cx - s / 2, cy - s / 2, s, s, s * 0.22); ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.fillStyle = '#FFFDFB';
  setFont(ctx, 'Playfair', s * 0.66, 700);
  ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
  ctx.fillText('F', cx - s * 0.02, cy + s * 0.24);
  ctx.fillStyle = C.coral;
  ctx.beginPath(); ctx.arc(cx + s * 0.215, cy - s * 0.2, s * 0.092, 0, Math.PI * 2); ctx.fill();
  ctx.restore();
}

// ---------- REAL DATA (from live /api/ask) ----------
const Q = 'Why do we repeat the very things that wound us?';
const ANSWER = 'My view is that the phenomenon of repeating that which wounds us can be understood through the concept of the \u201Ccompulsion to repeat,\u201D a notion deeply embedded within the architecture of our instincts. This compulsion represents an unconscious drive to recreate past experiences, including those that are painful, as a means of working through unresolved conflicts. When an individual encounters a disruption in their psychic equilibrium, an instinct arises to restore the previous state, even if it involves reliving distressing events. This repetition is not just a passive occurrence but an active, albeit unconscious, endeavor to bring about resolution.';
const SOURCES = [
  { d: 'Dream Distortion and Censorship', t: 'There was always an apprehension that things might not have been done properly. Everything must be checked and repeated, doubts assailed first one and then another of the safety measures.' },
  { d: 'Critique of Existing Theories', t: 'Order is a kind of compulsion to repeat which, when a regulation has been laid down once and for all, decides when, where and how a thing shall be done.' },
  { d: 'Symptom Formation', t: 'We have learnt that the patient repeats instead of remembering, and repeats under the conditions of resistance.' },
];
const SCANNED = '14,409';
const MINDS = [
  { n: 'Freud', c: '19,077' },
  { n: 'ZHI', c: '17,499' },
  { n: 'Jung', c: '2,910' },
  { n: 'Hume', c: '1,114' },
  { n: 'Nietzsche', c: '2,838' },
  { n: 'Bergler', c: '1,924' },
];

// ---------- dark bg ----------
function darkBg(ctx, t) {
  const g = ctx.createLinearGradient(0, 0, VW, VH);
  g.addColorStop(0, '#123E3A'); g.addColorStop(0.45, '#0C2622'); g.addColorStop(1, '#081715');
  ctx.fillStyle = g; ctx.fillRect(0, 0, VW, VH);
  const gx = VW * (0.34 + 0.05 * Math.sin(t * 0.5)), gy = VH * (0.42 + 0.05 * Math.cos(t * 0.4));
  let rg = ctx.createRadialGradient(gx, gy, 0, gx, gy, VW * 0.5);
  rg.addColorStop(0, 'rgba(20,184,166,0.18)'); rg.addColorStop(1, 'rgba(20,184,166,0)');
  ctx.fillStyle = rg; ctx.fillRect(0, 0, VW, VH);
  const v = ctx.createRadialGradient(VW / 2, VH / 2, VH * 0.3, VW / 2, VH / 2, VH * 0.85);
  v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,0.45)');
  ctx.fillStyle = v; ctx.fillRect(0, 0, VW, VH);
}

// ---------- OPEN ----------
function sceneOpen(ctx, t) {
  darkBg(ctx, t);
  const cx = VW / 2;
  const la = easeOut(seg(t, 0.2, 1.0));
  logo(ctx, cx, VH * 0.34 + lerp(18, 0, la), 92 * lerp(0.86, 1, la), la);
  const wa = easeOut(seg(t, 0.7, 1.5));
  ctx.save(); ctx.globalAlpha = wa; ctx.fillStyle = '#FFFDFB';
  setFont(ctx, 'Playfair', 56, 700); ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
  ctx.fillText('FreudGPT', cx, VH * 0.555 + lerp(16, 0, wa)); ctx.restore();
  const sa = easeOut(seg(t, 1.2, 2.1));
  ctx.save(); ctx.globalAlpha = sa; ctx.fillStyle = C.italicAccent;
  setFont(ctx, 'PlayfairItalic', 40, 500); ctx.textAlign = 'center';
  ctx.fillText('The Thinker\u2019s Workshop', cx, VH * 0.64 + lerp(12, 0, sa)); ctx.restore();
}

// ---------- WORKSHOP (real two-panel app) ----------
function pill(ctx, x, y, label, w) {
  const h = 26;
  ctx.strokeStyle = C.teal; ctx.lineWidth = 1.4;
  ctx.fillStyle = '#FFFFFF';
  rr(ctx, x, y, w, h, h / 2); ctx.fill(); ctx.stroke();
  ctx.fillStyle = C.teal; setFont(ctx, 'Inter', 10, 700);
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  lsText(ctx, label, x + w / 2, y + h / 2 + 1, 0.8, 'center');
  ctx.textBaseline = 'alphabetic';
}
function panel(ctx, x, y, w, h, title) {
  ctx.save();
  ctx.shadowColor = 'rgba(15,40,38,0.10)'; ctx.shadowBlur = 18; ctx.shadowOffsetY = 6;
  ctx.fillStyle = C.panelBg;
  rr(ctx, x, y, w, h, 16); ctx.fill();
  ctx.restore();
  ctx.save();
  rr(ctx, x, y, w, h, 16); ctx.clip();
  // teal header
  const hh = 42;
  const g = ctx.createLinearGradient(x, y, x, y + hh);
  g.addColorStop(0, '#0F8077'); g.addColorStop(1, '#0F766E');
  ctx.fillStyle = g; ctx.fillRect(x, y, w, hh);
  // icon
  ctx.fillStyle = 'rgba(255,255,255,0.9)';
  rr(ctx, x + 18, y + hh / 2 - 7, 14, 14, 4); ctx.fill();
  ctx.fillStyle = '#FFFDFB';
  setFont(ctx, 'Playfair', 19, 700); ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
  ctx.fillText(title, x + 42, y + hh / 2 + 1);
  ctx.textBaseline = 'alphabetic';
  ctx.restore();
  // border
  ctx.strokeStyle = C.border; ctx.lineWidth = 1;
  rr(ctx, x, y, w, h, 16); ctx.stroke();
  return y + hh;
}

function sceneWorkshop(ctx, t) {
  const lt = t - 3.0;
  // app bg
  ctx.fillStyle = C.appBg; ctx.fillRect(0, 0, VW, VH);
  // header
  logo(ctx, 36, 30, 34, 1);
  ctx.fillStyle = C.ink; setFont(ctx, 'Playfair', 19, 700);
  ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  ctx.fillText('FreudGPT', 58, 27);
  ctx.fillStyle = C.muted; setFont(ctx, 'Inter', 8, 600);
  lsText(ctx, 'THE THINKER\u2019S WORKSHOP', 58, 41, 0.5, 'left');
  // header pills (right)
  const pills = [['DIAGNOSTIC', 92], ['LONGFORM', 82], ['DOWNLOAD', 86], ['CLEAR', 60]];
  let px = VW - 16;
  for (let i = pills.length - 1; i >= 0; i--) { px -= pills[i][1]; pill(ctx, px, 17, pills[i][0], pills[i][1]); px -= 8; }
  ctx.strokeStyle = C.border; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(0, 58); ctx.lineTo(VW, 58); ctx.stroke();

  // panels
  const M = 16, pTop = 66, pBot = 552, pH = pBot - pTop;
  const dlgX = M, dlgW = Math.round((VW - 2 * M - 14) * 0.65);
  const archX = dlgX + dlgW + 14, archW = VW - M - archX;

  // ---- Dialogue ----
  const dContentY = panel(ctx, dlgX, pTop, dlgW, pH, 'The Dialogue');
  ctx.save();
  rr(ctx, dlgX, pTop, dlgW, pH, 16); ctx.clip();
  const pad = 24; let y = dContentY + 28;
  // user question
  ctx.fillStyle = C.teal; setFont(ctx, 'Inter', 10, 800);
  ctx.textAlign = 'left';
  lsText(ctx, 'YOU', dlgX + pad, y, 1.2, 'left'); y += 18;
  const qShown = Q.slice(0, Math.floor(clamp(lt / 0.6, 0, 1) * Q.length));
  ctx.fillStyle = C.ink; setFont(ctx, 'Inter', 17, 600);
  wrap(ctx, qShown, dlgW - pad * 2).forEach((l, i) => ctx.fillText(l, dlgX + pad, y + i * 24));
  y += 24 + 22;
  // assistant header
  if (lt > 0.7) {
    ctx.fillStyle = C.teal;
    ctx.beginPath(); ctx.arc(dlgX + pad + 13, y - 4, 13, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#FFFDFB'; setFont(ctx, 'Playfair', 15, 700);
    ctx.textAlign = 'center'; ctx.fillText('F', dlgX + pad + 13, y + 1); ctx.textAlign = 'left';
    ctx.fillStyle = C.ink; setFont(ctx, 'Inter', 14, 700);
    ctx.fillText('Sigmund Freud', dlgX + pad + 34, y - 5);
    ctx.fillStyle = C.faint; setFont(ctx, 'Inter', 11, 500);
    ctx.fillText('grounded in his own works', dlgX + pad + 34, y + 9);
    y += 30;
    // answer typewriter
    const shown = Math.floor(clamp((lt - 0.9) / 5.5, 0, 1) * ANSWER.length);
    ctx.fillStyle = C.inkSoft; setFont(ctx, 'Inter', 15.5, 400);
    const lines = wrap(ctx, ANSWER.slice(0, shown), dlgW - pad * 2);
    const maxLines = Math.floor((pBot - y - 16) / 25);
    const vis = lines.slice(-maxLines);
    vis.forEach((l, i) => ctx.fillText(l, dlgX + pad, y + i * 25));
    if (shown < ANSWER.length && Math.floor(lt * 2) % 2 === 0) {
      const lastW = ctx.measureText(vis[vis.length - 1] || '').width;
      ctx.fillStyle = C.teal;
      ctx.fillRect(dlgX + pad + lastW + 3, y + (vis.length - 1) * 25 - 13, 8, 16);
    }
  }
  ctx.restore();

  // ---- Archive ----
  const aContentY = panel(ctx, archX, pTop, archW, pH, 'The Archive');
  ctx.save();
  rr(ctx, archX, pTop, archW, pH, 16); ctx.clip();
  const apad = 16; let ay = aContentY + 18;
  // status line
  if (lt > 0.6) {
    const sa = easeOut(seg(lt, 0.6, 1.0));
    ctx.globalAlpha = sa;
    ctx.fillStyle = C.tealBright;
    ctx.beginPath(); ctx.arc(archX + apad + 4, ay - 4, 4, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = C.muted; setFont(ctx, 'Inter', 11, 600);
    ctx.textAlign = 'left';
    ctx.fillText('Searched ' + SCANNED + ' positions \u00B7 6 sources', archX + apad + 16, ay);
    ctx.globalAlpha = 1;
    ay += 22;
  }
  SOURCES.forEach((s, i) => {
    const appear = easeOut(clamp((lt - 0.9 - i * 0.5) / 0.6, 0, 1));
    if (appear <= 0) return;
    setFont(ctx, 'PlayfairItalic', 13, 500);
    const lines = wrap(ctx, '\u201C' + s.t + '\u201D', archW - apad * 2 - 28);
    const shownLines = lines.slice(0, 3);
    const cardH = 30 + shownLines.length * 19 + 14;
    ctx.save();
    ctx.globalAlpha = appear;
    ctx.translate(0, lerp(14, 0, appear));
    ctx.fillStyle = '#F6FAFA'; ctx.strokeStyle = C.border; ctx.lineWidth = 1;
    rr(ctx, archX + apad, ay, archW - apad * 2, cardH, 10); ctx.fill(); ctx.stroke();
    ctx.fillStyle = C.teal;
    rr(ctx, archX + apad, ay, 3, cardH, 2); ctx.fill();
    ctx.fillStyle = C.teal; setFont(ctx, 'Inter', 9, 800); ctx.textAlign = 'left';
    lsText(ctx, s.d.toUpperCase(), archX + apad + 14, ay + 20, 0.6, 'left');
    ctx.fillStyle = C.inkSoft; setFont(ctx, 'PlayfairItalic', 13, 500);
    shownLines.forEach((l, j) => ctx.fillText(l, archX + apad + 14, ay + 38 + j * 19));
    ctx.restore();
    ay += cardH + 12;
  });
  ctx.restore();

  // ---- controls bar ----
  const cy = 562, ch = 54;
  ctx.save();
  ctx.shadowColor = 'rgba(15,40,38,0.08)'; ctx.shadowBlur = 12; ctx.shadowOffsetY = 4;
  ctx.fillStyle = C.panelBg; rr(ctx, M, cy, VW - 2 * M, ch, 12); ctx.fill();
  ctx.restore();
  ctx.strokeStyle = C.border; ctx.lineWidth = 1; rr(ctx, M, cy, VW - 2 * M, ch, 12); ctx.stroke();
  const ctrls = [
    { l: 'ANSWER LENGTH', v: 110, f: 0.55 },
    { l: 'QUOTES', v: 2, f: 0.2 },
    { l: 'CREATIVITY', v: 10, f: 1.0 },
  ];
  let ccx = M + 26;
  const colW = 220;
  ctrls.forEach((c) => {
    ctx.fillStyle = C.muted; setFont(ctx, 'Inter', 9, 800); ctx.textAlign = 'left';
    lsText(ctx, c.l, ccx, cy + 20, 0.8, 'left');
    ctx.fillStyle = '#E6ECEB'; rr(ctx, ccx, cy + 30, 140, 5, 3); ctx.fill();
    ctx.fillStyle = C.teal; rr(ctx, ccx, cy + 30, 140 * c.f, 5, 3); ctx.fill();
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(ccx + 140 * c.f, cy + 32, 7, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = C.teal; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(ccx + 140 * c.f, cy + 32, 7, 0, Math.PI * 2); ctx.stroke();
    ctx.fillStyle = C.ink; setFont(ctx, 'Inter', 12, 700); ctx.textAlign = 'left';
    ctx.fillText(String(c.v), ccx + 156, cy + 36);
    ccx += colW;
  });
  // MODE + MEMORY (right)
  ctx.fillStyle = C.muted; setFont(ctx, 'Inter', 9, 800); ctx.textAlign = 'left';
  lsText(ctx, 'MODE', VW - 360, cy + 20, 0.8, 'left');
  ctx.fillStyle = C.ink; setFont(ctx, 'Inter', 12, 600);
  ctx.fillText('Standard', VW - 360, cy + 38);
  // memory toggle (on)
  const tgx = VW - 130, tgy = cy + 18, tgw = 40, tgh = 20;
  ctx.fillStyle = C.teal; rr(ctx, tgx, tgy, tgw, tgh, tgh / 2); ctx.fill();
  ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(tgx + tgw - tgh / 2, tgy + tgh / 2, tgh / 2 - 3, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = C.ink; setFont(ctx, 'Inter', 11, 700); ctx.textAlign = 'left';
  ctx.fillText('MEMORY', tgx + tgw + 8, cy + 32);

  // ---- input bar ----
  const iy = 626, ih = 60;
  ctx.strokeStyle = lt < 0.7 ? C.ink : C.border; ctx.lineWidth = lt < 0.7 ? 2 : 1.4;
  ctx.fillStyle = '#fff'; rr(ctx, M, iy, VW - 2 * M - 160, ih, 12); ctx.fill(); ctx.stroke();
  ctx.fillStyle = C.muted; setFont(ctx, 'Inter', 15, 400); ctx.textAlign = 'left';
  ctx.fillText('Pose your question to the thinker\u2026', M + 22, iy + ih / 2 + 5);
  // consult button
  const bw = 140, bx = VW - M - bw;
  const bg = ctx.createLinearGradient(bx, iy, bx + bw, iy);
  bg.addColorStop(0, '#FB8B3C'); bg.addColorStop(1, '#F97316');
  ctx.fillStyle = bg; rr(ctx, bx, iy, bw, ih, 12); ctx.fill();
  ctx.fillStyle = '#fff'; setFont(ctx, 'Inter', 16, 700);
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('Consult  \u2192', bx + bw / 2, iy + ih / 2 + 1);
  ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
}

// ---------- STATS (real counts) ----------
function sceneStats(ctx, t) {
  const lt = t - 13.0;
  ctx.fillStyle = C.appBg; ctx.fillRect(0, 0, VW, VH);
  const cx = VW / 2;
  ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
  const ha = easeOut(seg(lt, 0.1, 0.7));
  ctx.save(); ctx.globalAlpha = ha;
  ctx.fillStyle = C.ink; setFont(ctx, 'Playfair', 50, 700);
  // "Grounded in 45,362 positions." with teal number
  const a = 'Grounded in ', b = '45,362', c = ' positions.';
  const wa = ctx.measureText(a).width;
  setFont(ctx, 'Playfair', 50, 700); const wb = ctx.measureText(b).width;
  const wc = ctx.measureText(c).width;
  const totW = wa + wb + wc; let sx = cx - totW / 2;
  ctx.textAlign = 'left';
  ctx.fillStyle = C.ink; ctx.fillText(a, sx, VH * 0.2 + 12); sx += wa;
  ctx.fillStyle = C.teal; ctx.fillText(b, sx, VH * 0.2 + 12); sx += wb;
  ctx.fillStyle = C.ink; ctx.fillText(c, sx, VH * 0.2 + 12);
  ctx.textAlign = 'center';
  ctx.fillStyle = C.muted; setFont(ctx, 'Inter', 17, 400);
  ctx.fillText('Across six thinkers \u2014 their actual words, not summaries.', cx, VH * 0.2 + 48);
  ctx.restore();
  // grid 3x2
  const cols = 3, gap = 26, gridW = 900, cardW = (gridW - gap * (cols - 1)) / cols, cardH = 140;
  const gx0 = cx - gridW / 2, gy0 = VH * 0.34;
  MINDS.forEach((m, i) => {
    const r = Math.floor(i / cols), c2 = i % cols;
    const X = gx0 + c2 * (cardW + gap), Y = gy0 + r * (cardH + gap);
    const appear = easeOut(clamp((lt - 0.3 - i * 0.09) / 0.55, 0, 1));
    ctx.save(); ctx.globalAlpha = appear; ctx.translate(0, lerp(20, 0, appear));
    ctx.shadowColor = 'rgba(15,40,38,0.08)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 5;
    ctx.fillStyle = '#fff'; rr(ctx, X, Y, cardW, cardH, 16); ctx.fill();
    ctx.shadowColor = 'transparent';
    ctx.strokeStyle = C.border; ctx.lineWidth = 1.2; rr(ctx, X, Y, cardW, cardH, 16); ctx.stroke();
    const ax = X + cardW / 2, ay = Y + 44;
    const g = ctx.createLinearGradient(ax, ay - 26, ax, ay + 26);
    g.addColorStop(0, '#15534D'); g.addColorStop(1, '#0E1A1A');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(ax, ay, 27, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#CFEAE5'; setFont(ctx, 'Playfair', 26, 700);
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(m.n[0], ax, ay + 1); ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = C.ink; setFont(ctx, 'Inter', 17, 600);
    ctx.fillText(m.n, ax, Y + 96);
    ctx.fillStyle = C.teal; setFont(ctx, 'Inter', 13, 700);
    ctx.fillText(m.c + ' positions', ax, Y + 118);
    ctx.restore();
  });
}

// ---------- CLOSE ----------
function sceneClose(ctx, t) {
  darkBg(ctx, t);
  const cx = VW / 2, lt = t - 16.8;
  const ea = easeOut(seg(lt, 0.1, 0.6));
  ctx.save(); ctx.globalAlpha = ea; ctx.fillStyle = 'rgba(207,234,229,0.55)';
  setFont(ctx, 'Inter', 13, 700); ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
  lsText(ctx, 'PSYCHOLOGY AND PHILOSOPHY', cx, VH * 0.27, 3, 'center'); ctx.restore();
  const h1 = easeOut(seg(lt, 0.25, 0.95));
  ctx.save(); ctx.globalAlpha = h1; ctx.fillStyle = '#FFFDFB';
  setFont(ctx, 'Playfair', 70, 700); ctx.textAlign = 'center';
  ctx.fillText('Think alongside', cx, VH * 0.42 + lerp(14, 0, h1)); ctx.restore();
  const h2 = easeOut(seg(lt, 0.55, 1.25));
  ctx.save(); ctx.globalAlpha = h2; ctx.fillStyle = C.italicAccent;
  setFont(ctx, 'PlayfairItalic', 70, 600); ctx.textAlign = 'center';
  ctx.fillText('the great minds.', cx, VH * 0.535 + lerp(14, 0, h2)); ctx.restore();
  const sa = easeOut(seg(lt, 1.0, 1.6));
  ctx.save(); ctx.globalAlpha = sa; ctx.fillStyle = 'rgba(231,239,238,0.82)';
  setFont(ctx, 'Inter', 17, 400); ctx.textAlign = 'center';
  ctx.fillText('Real questions. Real sources. Their actual words.', cx, VH * 0.625); ctx.restore();
  const pa = easeOut(seg(lt, 1.4, 2.0));
  ctx.save(); ctx.globalAlpha = pa; ctx.translate(0, lerp(10, 0, pa));
  const pw = 246, ph = 50, ppx = cx - pw / 2, py = VH * 0.7;
  const pg = ctx.createLinearGradient(ppx, py, ppx + pw, py);
  pg.addColorStop(0, '#15B8A6'); pg.addColorStop(1, '#0F766E');
  ctx.fillStyle = pg; rr(ctx, ppx, py, pw, ph, ph / 2); ctx.fill();
  ctx.fillStyle = '#04241F'; setFont(ctx, 'Inter', 16, 700);
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('Start the dialogue  \u2192', cx, py + ph / 2 + 1);
  ctx.restore(); ctx.textBaseline = 'alphabetic';
}

// ---------- MASTER ----------
function frame(ctx, t) {
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, VW, VH);
  const aWork = clamp(seg(t, 3.0, 3.5) - seg(t, 12.6, 13.1), 0, 1);
  const aStats = clamp(seg(t, 12.8, 13.3) - seg(t, 16.5, 17.0), 0, 1);
  const aOpen = 1 - seg(t, 2.7, 3.4);
  const aClose = seg(t, 16.7, 17.2);
  if (aWork > 0) { ctx.save(); ctx.globalAlpha = aWork; sceneWorkshop(ctx, t); ctx.restore(); }
  if (aStats > 0) { ctx.save(); ctx.globalAlpha = aStats; sceneStats(ctx, t); ctx.restore(); }
  if (aOpen > 0) { ctx.save(); ctx.globalAlpha = aOpen; sceneOpen(ctx, t); ctx.restore(); }
  if (aClose > 0) { ctx.save(); ctx.globalAlpha = aClose; sceneClose(ctx, t); ctx.restore(); }
}

// ---------- RUN ----------
const only = process.argv[2] ? parseInt(process.argv[2]) : null;
const canvas = createCanvas(W, H);
const ctx = canvas.getContext('2d');
ctx.textDrawingMode = 'glyph';
function render(i) {
  const t = i / FPS;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, W, H);
  ctx.scale(SCALE, SCALE);
  ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  frame(ctx, t);
  fs.writeFileSync(path.join(OUT, `f_${String(i).padStart(4, '0')}.png`), canvas.toBuffer('image/png'));
}
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
if (only !== null) { render(only); console.log('frame', only); }
else { for (let i = 0; i < TOTAL; i++) { render(i); if (i % 60 === 0) console.log('frame', i, '/', TOTAL); } console.log('done', TOTAL); }
