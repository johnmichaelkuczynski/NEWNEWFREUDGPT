# R1 — FreudGPT Synthetic User Agent

R1 is a Playwright-driven synthetic user that beta-tests FreudGPT end-to-end. It produces **raw, reviewable evidence** of every interaction — verbatim inputs, full streamed responses, network bodies, screenshots, judge critiques. No green-checkmark theater.

## Install

```bash
cd tools/r1
npm install
npx playwright install chromium
```

## Run

Make sure FreudGPT is running locally (Flask on `:5000`, longform service on `:3001`). Then:

```bash
ANTHROPIC_API_KEY=sk-ant-... npm start
```

Open the live view at <http://localhost:7777> while the run is in progress. Watch the Grounding State panel.

### Smoke test (skip expensive functions)

```bash
SKIP_FUNCTIONS=5,7,10 npm start
```

### Configuration (env vars)

| Var | Default | Purpose |
|-----|---------|---------|
| `APP_URL` | `http://localhost:5000` | Target FreudGPT instance |
| `HEADLESS` | `false` | Run Playwright headless |
| `TYPE_DELAY_MS` | `15` | Per-keystroke delay (for live view) |
| `LIVE_VIEW_PORT` | `7777` | Port for live view |
| `SKIP_FUNCTIONS` | `` | Comma-separated function numbers to skip |
| `CONSULTATION_TIMEOUT_MS` | `300000` | Per-consultation timeout (5 min) |
| `LONGFORM_TARGET_WORDS` | `2000` | Word target for Function 7 |
| `ABORT_ON_DIAGNOSTIC_DB_FAIL` | `true` | Abort if pre-run diagnostic shows DB failure |
| `ANTHROPIC_MODEL` | `claude-opus-4-20250514` | R1 brain + judge model |

## What R1 tests

14 functions covering: diagnostic round-trip, thinker selection, single consultation (Invariant A — grounding), low-relevance warning (Invariant B), provider switching, Memory Mode (Invariant D — tree validity), Longform (Invariant E — no section duplication), RAG mode, inference engine, file ingestion, work reader, download/export, audit trail, final diagnostic regression check (Invariant C — corpus count drift).

## Critical invariants

| ID | Invariant | Violation Trigger |
|----|-----------|-------------------|
| **A** | Every response grounded in retrieved positions | Judge identifies claim with no basis in retrieved position texts |
| **B** | Low-relevance warning fires when max_similarity < 0.25 | Off-topic question yields confident invented response |
| **C** | Per-thinker corpus counts stable across run | Any count diff between pre and post diagnostic |
| **D** | Memory tree nodes valid (tags + Wittgenstein decimal IDs) | Malformed node value or ID |
| **E** | No duplicate longform sections | Two sections >70% shingle-overlap, or identical 100-char openings |

## Artifacts (`runs/<ISO-timestamp>/`)

```
transcript.jsonl          One JSON object per interaction
report.html               Self-contained, sticky TOC, all evidence inline
failures.md               CRITICAL VIOLATIONS first, then judge concerns
network.log               JSONL of every /api/* call + body
sse-streams/NNNN.jsonl    Full SSE event sequence per streaming interaction
outputs/
  diagnostic-before.json
  diagnostic-after.json
  longform-doc.txt
  tractatus-snapshots/
  retrieved-positions/
  answer-logs.json
console.log               Full stdout
screenshots/              Numbered PNGs (3 per interactive step)
run-summary.txt           Final counts
```

## Exit codes

- `0` — clean (no concerns, no violations)
- `1` — judge concerns raised
- `2` — critical invariant violations
- `3` — harness sanity check failed

## Anti-theater sanity checks

After the run, R1 audits its own transcript:
- Every expected route appears in network calls
- `r1_input >= 10 chars` for interactive steps
- Interactive steps have 3 screenshots, not byte-identical
- `judge_critique >= 30 words`
- Consultations have populated `retrieval_event` + `retrieved_position_texts` + `sse_events_observed` includes both `retrieval` and `done`
- Memory Mode interactions have populated `tractatus_delta`
- Longform interactions have populated `longform_structure` with section similarity matrix

If any sanity check fails: exit code `3`.
