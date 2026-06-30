import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const VIDS = path.resolve('video_build/demo/vids');
const TMP = path.resolve('video_build/demo/enc');
const OUT = path.resolve('exports/FreudGPT_Demo.mp4');
fs.mkdirSync(TMP, { recursive: true });
fs.mkdirSync(path.dirname(OUT), { recursive: true });

const FPS = 30;
const sh = (cmd) => { console.log('$', cmd.slice(0, 160)); execSync(cmd, { stdio: 'inherit' }); };

// all webm segments in numeric order
const segs = fs.readdirSync(VIDS).filter(f => f.endsWith('.webm')).sort();
if (!segs.length) { console.error('no webm segments found in', VIDS); process.exit(1); }

const parts = [];
for (const webm of segs) {
  const base = webm.replace(/\.webm$/, '');
  const src = path.join(VIDS, webm);
  const cutsFile = path.join(VIDS, base + '.cuts.json');
  let cuts = [];
  if (fs.existsSync(cutsFile)) { try { cuts = JSON.parse(fs.readFileSync(cutsFile, 'utf8')); } catch { } }
  cuts = (cuts || []).filter(c => c && c.b - c.a > 1.0).sort((a, b) => a.a - b.a);
  const dst = path.join(TMP, base + '.mp4');

  let vf;
  if (cuts.length) {
    const expr = cuts.map(c => `between(t,${c.a},${c.b})`).join('+');
    vf = `select='not(${expr})',setpts=N/FRAME_RATE/TB,scale=1280:720,fps=${FPS}`;
  } else {
    vf = `scale=1280:720,fps=${FPS}`;
  }
  sh(`ffmpeg -y -i "${src}" -vf "${vf}" -an -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p "${dst}" 2>/dev/null`);
  parts.push(dst);
  const dur = execSync(`ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "${dst}"`).toString().trim();
  console.log(`  ${base}: ${cuts.length} cut(s) -> ${dur}s`);
}

// concat
const listFile = path.join(TMP, 'list.txt');
fs.writeFileSync(listFile, parts.map(p => `file '${p}'`).join('\n'));
sh(`ffmpeg -y -f concat -safe 0 -i "${listFile}" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r ${FPS} "${OUT}" 2>/dev/null`);

const dur = execSync(`ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "${OUT}"`).toString().trim();
const mb = (fs.statSync(OUT).size / 1e6).toFixed(2);
console.log(`\n✓ ${OUT}\n  duration ${dur}s, ${mb} MB, ${parts.length} segments`);
