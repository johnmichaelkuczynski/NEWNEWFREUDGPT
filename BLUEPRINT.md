# FREUDGPT — THE THINKER'S WORKSHOP — COMPLETE APPLICATION BLUEPRINT

================================================================================
## PART 1: APPLICATION FUNCTIONS

The app has 10 core functions:

### 1. PHILOSOPHICAL CONSULTATION (Ask a Thinker)
- **Location:** Home page → main input ("Pose your question to the thinker…") → Consult button
- **Purpose:** Pose any question to one of 6 thinkers and receive a streaming, database-grounded answer
- **Inputs:** Thinker selection (avatar), question text, provider + model, mode (Standard / Dialogue), enhanced toggle, popups toggle, answer-length slider, quotes slider, data mode (Classic / RAG), text size
- **Flow:** Question → semantic search over `positions` table → top-K retrieval + context expansion → prompt assembled with verbatim positions → streamed LLM response (token-by-token SSE) → source positions surfaced in The Archive panel
- **Endpoint:** `POST /api/ask` (SSE stream)
- **Output:** Streaming prose in The Dialogue (70% panel) + synchronized source positions in The Archive (30% panel)

### 2. THINKER SELECTION & PROFILES
- **Location:** Home page → primary thinker row (Freud, ZHI/Kuczynski, Jung) + Related Thinkers header strip (Hume, Nietzsche, Bergler)
- **Purpose:** Switch active philosophical database; each thinker has its own corpus, style, and per-thinker count badge
- **Thinkers:** freud (19,077), kuczynski (17,499), jung (2,910), nietzsche (2,838), bergler (1,924), hume (1,114) — total **45,362 positions**
- **Flow:** Click avatar → active thinker state updated → next query uses that thinker's positions + style prompt
- **Endpoint:** `GET /api/databases`, `GET /api/topics/<thinker>`
- **Output:** Active-thinker pill + position count; knowledge panel popup with domains and starter questions

### 3. MEMORY MODE (Tractatus Trees)
- **Location:** Home page → Memory toggle + project/session controls strip
- **Purpose:** Project-scoped persistent memory; after each exchange Claude updates a Wittgenstein-style numbered knowledge tree (ASSERTS / REJECTS / ASSUMES / OPEN / RESOLVED)
- **Flow:** Pick project + session → ask question → response generated with tiered memory context (meta-trees + current tree + cross-session messages) → tree updated → archived at 500 nodes → meta-tree synthesized every 10 archives
- **Endpoints:** `GET/POST /api/memory/projects`, `DELETE/POST /api/memory/projects/:id`, `POST /api/memory/projects/:id/rename`, `GET/POST /api/memory/projects/:id/sessions`, `PATCH/DELETE /api/memory/sessions/:id`, `GET /api/memory/sessions/:id/transcript`, `GET /api/memory/projects/:id/tractatus`, `GET /api/memory/projects/:id/memory-hierarchy`, `POST /api/memory/ask`
- **Output:** Memory-aware streaming response + viewable tree (🌳 Tree button) + downloadable JSON of all trees + archives + meta-trees

### 4. LONGFORM GENERATION (NeuroText-style Coherence Skeleton)
- **Location:** Header → 📚 LONGFORM button → modal with thinker / mode / word-target / prompt
- **Purpose:** Generate coherent, non-self-repetitive long outputs (essays, dialogues, lectures) up to ~50K words
- **Architecture:** Two-tier skeleton (macro plan → micro plan per section) + persistent state DB (claims_made, positions_cited, examples_used, open_threads, last_paragraph) + READ→GENERATE→EXTRACT→MERGE→WRITE loop per section
- **Modes:** essay (continuous argument), dialogue (named interlocutor turns), lecture (numbered teaching units)
- **Endpoints:** `POST /api/longform/coherent/start`, `GET /api/longform/coherent/:id/stream` (SSE: snapshot/status/skeleton/section_start/section_complete/state/complete/error), `GET /api/longform/coherent/:id`, `DELETE /api/longform/coherent/:id`, `POST /api/longform/coherent/:id/resume`, `GET /api/longform/coherent/list?thinker=…`
- **Output:** Live per-section streaming with role tags, cumulative word counter, download-as-text, resumable on interruption

### 5. INFERENCE ENGINE (Forward-Chaining Deduction)
- **Location:** Internal — invoked when high-confidence rules match a query
- **Purpose:** Executable philosophical reasoning — deduce theoretical conclusions from a thinker's rule base *before* generating LLM prose, so answers reflect the thinker's actual reasoning chain rather than paraphrase
- **Per-thinker engines:** `freud_engine.py`, `kuczynski_engine.py`, `jung_engine.py`, `hume_engine.py`, `nietzsche_engine.py`, `bergler_engine.py` (each with its own `<thinker>_rules_full.json`)
- **Endpoints:** `POST /api/inference/deduce`, `POST /api/inference/search`, `POST /api/inference/history`
- **Output:** Deduction chain (premises → intermediate steps → conclusion) injected into the LLM prompt as a scaffold

### 6. CONTENT INGESTION (File Watcher + Manual Upload)
- **Location:** Background workflow `ingest-watcher` monitoring `ingest/` folder; manual upload via 📎 button on chat input
- **Purpose:** Add new philosophical works to the corpus without manual scripting
- **Supported formats:** .txt, .json, .pdf, .docx
- **Flow:** File dropped in `ingest/` → text extracted (PyPDF2 / python-docx) → embeddings generated (OpenAI `text-embedding-3-small`) → positions inserted to `positions` table → file moved to `ingest/processed/` (or `ingest/failed/`)
- **Endpoints:** `POST /api/upload`, `POST /api/upload/document`
- **Output:** New positions immediately searchable; status surfaced in workflow logs

### 7. RAG OVER SOURCE TEXTS
- **Location:** Data mode dropdown → "RAG" → query uses full source texts (not just position extracts)
- **Purpose:** Search verbatim chunks of original philosophical works for evidence the position database may not contain
- **Backing store:** `text_chunks` table (**33,533 chunks** across all thinkers; PostgreSQL full-text search with ts_rank)
- **Endpoint:** integrated into `/api/ask` when data-mode = RAG
- **Output:** Verbatim source passages with file + chunk index; surfaced in The Archive

### 8. WORK READER (In-app Library)
- **Location:** Knowledge panel → "Read full work" links → in-app reader
- **Purpose:** Read full philosophical works from `texts/` folder without leaving the app
- **Endpoints:** `GET /api/works`, `GET /api/work/<work_id>`
- **Output:** Paginated full-text reader with archive-style typography

### 9. DOWNLOAD / EXPORT
- **Location:** Header → 📥 DOWNLOAD button (chat); Longform modal → Download-as-text per document; Memory tree → Download JSON
- **Purpose:** Persist sessions outside the app
- **Endpoint:** client-side blob generation from session state + server `GET /api/memory/sessions/:id/transcript`
- **Output:** .txt / .json export files

### 10. SYSTEM DIAGNOSTIC
- **Location:** Header → 🩺 DIAGNOSTIC button (visible on every view)
- **Purpose:** Beta-test harness — verify all APIs, DB, and formal HTTP/CRUD/SSE flow mechanics without judging answer content quality
- **Checks (20 total):** PostgreSQL connect; positions populated; per-thinker counts; text_chunks populated; required schema (8 tables); longform service health (:3001); 6 AI provider pings (Anthropic, OpenAI, DeepSeek, Perplexity, xAI Grok, OpenAI embeddings); direct DB position query; `/api/positions/search` round-trip; chat streaming round-trip (real Anthropic streaming primitive); memory project create→list→delete; longform job create→list→delete (no LLM tokens consumed); SSE endpoint headers; `/api/databases`; `/api/providers`
- **Endpoint:** `POST /api/diagnostic/run`
- **Output:** JSON `{ summary: {total, passed, failed}, results: [{ name, category, status, detail, ms }] }` rendered as categorized pass/fail dashboard with latency per check

================================================================================
## PART 2: COMPLETE FILE TREE

```
/
├── BLUEPRINT.md                         # This document
├── README.md                            # Public-facing product overview (NEUROTEXT-style)
├── replit.md                            # Project overview, user preferences, recent changes
├── app.py                               # MAIN FLASK BACKEND (3,299 lines, ~45 routes)
├── search.py                            # Semantic search + context expansion + RAG
├── conversation_manager.py              # Per-session memory + self-contradiction detection
├── ingest.py                            # Manual ingestion pipeline
├── chunk_texts.py                       # Source-text chunker for RAG (texts/ → text_chunks)
├── migrate_to_postgres.py               # JSON → PostgreSQL importer
│
├── <thinker>_engine.py                  # Per-thinker forward-chaining inference engine
│   freud_engine.py / kuczynski_engine.py / jung_engine.py /
│   hume_engine.py / nietzsche_engine.py / bergler_engine.py
├── <thinker>_rules_full.json            # Per-thinker rule base (premises + inferences)
│
├── longform/                            # TypeScript long-form generation service (port 3001)
│   ├── server.ts                        # Express server + SSE routes
│   ├── coherenceState.ts                # Persistent state schema + merge/dedupe logic
│   ├── generateSkeleton.ts              # Macro plan (thesis + arc + sections) + micro plans
│   ├── generateCoherentSection.ts       # READ→GENERATE→EXTRACT→MERGE→WRITE per section
│   ├── coherentLongForm.ts              # Job orchestrator + resume + worker leasing
│   ├── extractDocumentSections.ts       # Heading / structure extraction for source docs
│   ├── processDocumentTask.ts           # Document-driven long-form pipeline
│   ├── inference.ts                     # Bridge to per-thinker rule engines
│   ├── generateLongFormEssay.ts         # Legacy single-shot path
│   ├── generateLongFormOutline.ts       # Legacy outline path
│   ├── generateStrictOutline.ts         # Outline-first variant
│   ├── generateSection.ts               # Section generator (legacy)
│   ├── <thinker>LongForm.ts             # Per-thinker prompt configuration
│   ├── openai.ts                        # OpenAI client wrapper
│   └── index.ts                         # Entrypoint
│
├── templates/
│   └── index.html                       # Single-page Workshop UI (506 lines)
│
├── static/
│   ├── app.js                           # Frontend logic (2,757 lines)
│   └── style.css                        # Bright Wellness theme (3,202 lines)
│
├── scripts/
│   ├── watch_ingest.py                  # File-watcher workflow (background)
│   ├── add_*_positions.py               # One-off position-batch importers
│   ├── generate_bergler_embeddings.py   # Per-thinker embedding generators
│   ├── ai_position_extractor.py         # LLM-based position extractor
│   └── ... (40+ extraction / ingestion utilities)
│
├── extraction_scripts/                  # Older / archival extractors
├── ingest/                              # Drop folder for auto-ingestion
│   ├── processed/                       # Successfully ingested
│   └── failed/                          # Failed ingestion (with logs)
├── texts/                               # Full-text corpus (source PDFs/TXTs)
├── data/                                # JSON backups of position databases
├── input/                               # Raw extraction inputs
├── exports/                             # Generated downloads
│
├── kuczynski_*.json / freud_*.json / …  # Per-thinker JSON corpora (backups)
├── requirements.txt                     # Python deps
├── pyproject.toml / uv.lock             # Python project config
├── package.json / package-lock.json     # Node deps (longform service)
├── runtime.txt                          # Python runtime pin
└── render.yaml                          # Deploy config (Render fallback)
```

================================================================================
## PART 3: FILE DESCRIPTIONS

### BACKEND (Python / Flask)

| File | Purpose |
|------|---------|
| `app.py` | **MAIN BACKEND** (3,299 lines). All Flask routes. SSE streaming. Lazy-initialized provider clients (Anthropic, OpenAI, DeepSeek, Perplexity, Grok). Diagnostic harness. Memory mode endpoints. Longform proxy to TS service. |
| `search.py` | Semantic search (cosine similarity over OpenAI embeddings). `expand_with_context()` fetches related/adjacent positions via explicit related_positions field, same `work_id`, or list-index adjacency. Returns ranked positions + RAG chunks. |
| `conversation_manager.py` | Per-session message history + self-contradiction detection across turns. |
| `ingest.py` | Manual ingestion pipeline: extract text → generate embeddings → insert positions. |
| `chunk_texts.py` | Splits files in `texts/` into ~500-word chunks → inserts into `text_chunks` table for RAG. |
| `migrate_to_postgres.py` | One-time importer: per-thinker JSON corpora → `positions` table. |
| `<thinker>_engine.py` | Forward-chaining inference engine for each thinker. Loads rules from `<thinker>_rules_full.json`, matches query → produces deduction chain → returns premises + intermediate steps + conclusion. |
| `scripts/watch_ingest.py` | Background `ingest-watcher` workflow. Polls `ingest/` for new files, dispatches to ingest pipeline, moves results to `processed/` or `failed/`. |

### LONGFORM SERVICE (TypeScript / Express, port 3001)

| File | Purpose |
|------|---------|
| `longform/server.ts` | Express server. Routes: `/longform/coherent/start`, `/:id/stream` (SSE), `/:id`, `/:id/resume`, `/list`. Proxied through Flask under `/api/longform/coherent/*`. |
| `longform/coherenceState.ts` | State schema: `claims_made`, `positions_cited`, `examples_used`, `open_threads`, `resolved_threads`, `section_summaries`, `last_paragraph`, `current_stage`. Merge with deduplication. `packAntiRepeat()` builds full-memory window of prior claims/examples for each section prompt. |
| `longform/generateSkeleton.ts` | Macro plan (thesis + arc + N sections with distinct roles & word targets) → micro plan per section (claims_to_make, positions_to_use, examples_to_use, bridge_from_prior, bridge_to_next, must_not_repeat). |
| `longform/generateCoherentSection.ts` | Per-section LLM call assembling skeleton + state + RAG positions + anti-repetition lists. Returns section text + state delta. |
| `longform/coherentLongForm.ts` | Job orchestrator: per-section READ→GENERATE→EXTRACT→MERGE→WRITE loop. Atomic `commitSection` transaction. Worker leasing (`worker_id` + `lease_until`) prevents duplicate workers picking up the same job. `ensureSchema()` at boot. |
| `longform/extractDocumentSections.ts` | Parses headings / structure from uploaded source docs. |
| `longform/processDocumentTask.ts` | Document-driven long-form (use source doc as input rather than free prompt). |
| `longform/inference.ts` | Bridges TS service to Python inference engines. |
| `longform/<thinker>LongForm.ts` | Per-thinker prompt configuration (style, register, characteristic moves). |

### FRONTEND

| File | Purpose |
|------|---------|
| `templates/index.html` | Single-page Workshop UI (506 lines). Header (logo + Related Thinkers strip + Diagnostic / Longform / Download / Clear buttons). Dual panel: The Dialogue (70%) + The Archive (30%). Input section: thinker avatars, sliders (answer length, quotes), toggles (enhanced, popups, memory), mode dropdown, data dropdown, text-size slider, chat input, upload button. Modals: login, topics, knowledge, longform, diagnostic, tractatus viewer. |
| `static/app.js` | **FRONTEND LOGIC** (2,757 lines). SSE consumption for streaming responses + diagnostic + longform progress. Thinker switching. Memory project/session CRUD. Tractatus tree rendering. Longform modal with skeleton viewer + per-section streaming + cumulative word count. Diagnostic modal with categorized pass/fail rendering. Download/clear/upload handlers. |
| `static/style.css` | **THEME** (3,202 lines). Bright Wellness palette (deep teal `#0F766E`, off-white `#FFFDFB`, mint `#F0FDFA`, coral-orange `#F97316`). Playfair Display (headings), Inter (body), Crimson Pro (quotes). Dual-panel resizable layout. Modal styles. Diagnostic dashboard styles. Orbiting-emoji + typewriter animations. |

================================================================================
## PART 4: DATABASE SCHEMA (PostgreSQL — Neon)

**19 tables total.** Core tables drive the app; others support legacy / future features.

### `positions` — Philosophical positions (PRIMARY content store)
```
id              SERIAL PRIMARY KEY
position_id     TEXT UNIQUE            -- Original ID from JSON source
thinker         TEXT                   -- freud | kuczynski | jung | hume | nietzsche | bergler
title           TEXT                   -- Position title / topic
text_evidence   TEXT                   -- The philosophical position text
domain          TEXT                   -- Philosophy domain category
source          TEXT
work_title      TEXT
year            INTEGER
work_id         TEXT                   -- For context-expansion adjacency
related_positions TEXT[]               -- Explicit related-position ids
list_index      INTEGER                -- Index within work (adjacency fallback)
embedding       BYTEA                  -- Cached text-embedding-3-small vector
```
**Per-thinker counts:** freud 19,077 · kuczynski 17,499 · jung 2,910 · nietzsche 2,838 · bergler 1,924 · hume 1,114 = **45,362**

### `text_chunks` — RAG corpus (verbatim source-text passages)
```
id            SERIAL PRIMARY KEY
thinker       TEXT
source_file   TEXT
chunk_text    TEXT
chunk_index   INTEGER
```
**Total chunks:** 33,533. Searched via PostgreSQL full-text + ts_rank.

### `memory_projects` — Memory Mode projects (thinker-scoped)
```
id          SERIAL PRIMARY KEY
thinker     TEXT NOT NULL
name        TEXT NOT NULL
tractatus   JSONB                     -- Current Wittgenstein-style numbered tree
node_count  INTEGER DEFAULT 0
created_at  TIMESTAMP DEFAULT now()
updated_at  TIMESTAMP DEFAULT now()
```

### `memory_sessions` — Chat sessions inside a project
```
id          SERIAL PRIMARY KEY
project_id  INTEGER FK → memory_projects.id
name        TEXT
transcript  JSONB                     -- Full message log
created_at  TIMESTAMP DEFAULT now()
updated_at  TIMESTAMP DEFAULT now()
```

### `tractatus_archive` — Archived trees (one per 500-node fill)
```
id              SERIAL PRIMARY KEY
project_id      INTEGER FK → memory_projects.id
archive_tier    INTEGER                -- 1=raw archive, 2=compressed
tractatus       JSONB
archived_at     TIMESTAMP DEFAULT now()
```
**Compression rule:** at 500 nodes → archive raw → compress to ~100 nodes → reset current tree.
**Meta-Tractatus rule:** every 10 archives → Claude generates ~150-node meta-tree with SYNTHESIZES: tags. Up to 3 most recent meta-trees loaded into prompt (8K chars each).

### `answer_logs` — Retrieval transparency audit trail
```
id                          SERIAL PRIMARY KEY
query                       TEXT NOT NULL
thinker                     TEXT NOT NULL
provider                    TEXT
model                       TEXT
positions_scanned           INTEGER
positions_above_threshold   INTEGER
max_similarity              REAL
mean_similarity             REAL
top_k                       INTEGER
retrieved_position_ids      TEXT[]
retrieved_scores            REAL[]
domains_covered             TEXT[]
response_text               TEXT
response_word_count         INTEGER
created_at                  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```
Logged per query. Includes `context_positions_added` + `total_positions_used` in metadata.

### `longform_documents` — Longform jobs
```
id                SERIAL PRIMARY KEY
document_id       UUID UNIQUE
thinker           TEXT
user_prompt       TEXT
mode              TEXT                  -- essay | dialogue | lecture
target_words      INTEGER
total_sections    INTEGER
current_section   INTEGER
skeleton          JSONB                 -- Macro + micro plans
state             JSONB                 -- Live state (claims, positions cited, threads, last_paragraph)
status            TEXT                  -- queued | running | complete | error | paused
error             TEXT
worker_id         TEXT                  -- Lease holder
lease_until       TIMESTAMP             -- Lease expiry
created_at        TIMESTAMP DEFAULT now()
updated_at        TIMESTAMP DEFAULT now()
```

### `longform_sections` — Per-section output + state snapshot
```
id              SERIAL PRIMARY KEY
document_id     TEXT FK → longform_documents.document_id
section_index   INTEGER
section_title   TEXT
section_plan    JSONB
section_text    TEXT
word_count      INTEGER DEFAULT 0
state_after     JSONB                  -- State snapshot after this section
created_at      TIMESTAMP DEFAULT now()
UNIQUE (document_id, section_index)
```

### Other tables (legacy / supporting)
`users`, `sessions`, `messages`, `conversations`, `figures`, `figure_conversations`, `arguments`, `quotes`, `persona_settings`, `response_progress`, `texts` — used by older flows; not on the critical path for current Workshop UI.

================================================================================
## PART 5: AI PROVIDER CONFIGURATION

| Provider | Label | Models | Use Cases |
|----------|-------|--------|-----------|
| Anthropic | **ZHI 1** | claude-sonnet-4-20250514, claude-opus-4-20250514 | Consultation, Memory tree generation, Longform section authoring, Diagnostic ping |
| OpenAI | **ZHI 2** | gpt-4o, gpt-4o-mini, o1, o1-mini | Consultation, Embeddings (text-embedding-3-small), Diagnostic ping |
| Grok (xAI) | **ZHI 3** | grok-4, grok-3-beta, grok-3-mini-beta, grok-code-fast-1 | Consultation, Diagnostic ping |
| DeepSeek | **ZHI 4** *(DEFAULT)* | deepseek-chat, deepseek-reasoner | Consultation (cost-efficient long contexts), Diagnostic ping |
| Perplexity | **ZHI 5** | sonar-pro, sonar, sonar-reasoning | Research-augmented consultation, Diagnostic ping |

**All providers:**
- Lazy-initialized clients — missing API keys do **not** crash module load; they fail clearly only when invoked.
- Selectable per session via provider + model dropdowns.
- Token-by-token SSE streaming.
- Pinged live (4-token completion) on every `/api/diagnostic/run`.

**Specialized services:**
- **OpenAI Embeddings** (`text-embedding-3-small`, dim=1536): cached on `positions.embedding`; cosine similarity via scikit-learn.
- **PyPDF2 / python-docx:** document text extraction.

================================================================================
## PART 6: PROMPT & RESPONSE SYSTEM

### Response Modes
- **Standard Mode:** strict word count + quote requirements driven by sliders (answer length, quotes). Detailed, comprehensive responses with mandatory minimum lengths.
- **Dialogue Mode:** natural conversational tone; thinker may give short answers, ask clarifying questions, challenge user assumptions, or push back intellectually. No strict length floor.
- **Enhanced Toggle:** enables creative theoretical extension and modern-knowledge integration.

### Argument Synthesis (vs Quote-Stitching)
The prompt instructs the LLM to **understand** the arguments in retrieved positions and synthesize them into a coherent answer (thesis → supporting reasons → conclusion), not mechanically stitch quotes.

### Grounding Rules
- Every major claim must be traceable to a specific retrieved position.
- Each response must include ≥ N close paraphrases from positions (N tied to quotes slider).
- LLM must quote verbatim or very closely paraphrase database positions.
- LLM must **refuse** to invent terminology not present in sources.
- LLM must **explicitly acknowledge** when retrieved positions don't address the question (warning fires when `max_similarity < 0.25`).
- LLM never refuses to engage — always responds, even with tangential positions, but flags the mismatch.

### Argumentation Stance
The prompt defaults to **SUPPORT / EXPAND** when the user presents a position. It does not argue against the user. It acknowledges mismatches when retrieved positions conflict with the user's claim.

### Formatting
- Plain prose only — no markdown (`**`, `##`), no source citations (`Source 1`, etc.).
- Source positions are sent to the LLM without numbering labels.
- The Archive panel displays the actual positions used, surfaced after streaming completes.

### Context Expansion (`search.py::expand_with_context()`)
Three fallback strategies for fetching adjacent context:
1. Explicit `related_positions` field on the position.
2. Adjacent positions from the same `work_id`.
3. List-index based adjacency as last resort.

### Canonical Query Mapping
Key philosophical queries (e.g. "What is the unconscious?") map to canonical retrieval sets to guarantee consistent surfacing of central positions.

================================================================================
## PART 7: TEST FLOW LOGIC

### CONSULTATION FLOW
1. User picks thinker (avatar) + provider + model + mode + sliders.
2. Types question → presses Enter / Consult.
3. `POST /api/ask` → embedding generated → top-K positions retrieved → `expand_with_context()` expands.
4. Per-thinker inference engine runs if applicable → deduction chain appended.
5. Prompt assembled (positions + chain + memory if Memory Mode) → streamed to chosen provider.
6. SSE events: `retrieval` (metadata: scanned/threshold/similarity/domains) → `token` (prose chunks) → `sources` (final position list) → `done`.
7. UI streams tokens into The Dialogue; populates The Archive after retrieval event.
8. Audit row written to `answer_logs`.

### MEMORY MODE FLOW
1. Create / select project (thinker-scoped) → create / select session.
2. Memory toggle ON → `POST /api/memory/ask` instead of `/api/ask`.
3. Server loads tiered context: meta-trees (3 × 8K) + current tree (12K) + cross-session messages (15K cap).
4. Response generated → Claude analyzes exchange → updates Tractatus tree with numbered nodes (ASSERTS/REJECTS/ASSUMES/OPEN/RESOLVED).
5. At 500 nodes → archive raw → compress to ~100 → reset. At 10 archives → meta-tractatus.
6. 🌳 Tree button opens viewer; user can download all trees as JSON.

### LONGFORM FLOW
1. Header → 📚 LONGFORM → modal: thinker + mode + word target + prompt.
2. `POST /api/longform/coherent/start` → Flask proxies to TS service (`:3001`) → job created in `longform_documents` (status=queued).
3. UI opens SSE on `/api/longform/coherent/:id/stream`. Initial `snapshot` event hydrates UI.
4. Worker leases job (`worker_id` + `lease_until`) → generates skeleton (macro + micro plans) → emits `skeleton` event.
5. Per section: `section_start` → READ state → GENERATE section (streamed) → EXTRACT state delta (`extractStateUpdate` LLM call → JSON) → MERGE with dedup → atomic `commitSection` transaction → `section_complete` + `state` events.
6. After final section: `complete` event with full text + word counts.
7. Crash / interruption → job remains in DB → `POST /api/longform/coherent/:id/resume` re-leases and continues from `current_section`.

### DIAGNOSTIC FLOW
1. Header → 🩺 DIAGNOSTIC button → modal opens.
2. "▶ Run Full Diagnostic" → `POST /api/diagnostic/run` (synchronous, ~10–20s).
3. Server executes 20 checks across 3 categories:
   - **System (6):** PostgreSQL connect · positions populated · per-thinker counts · text_chunks populated · required schema (8 tables) · longform service health (`:3001`).
   - **AI Providers (6):** Anthropic ping · OpenAI ping · DeepSeek ping · Perplexity ping · xAI Grok ping · OpenAI embedding service (dim verification).
   - **Functional (8):** direct DB position query · `/api/positions/search` · chat streaming round-trip (real Anthropic streaming primitive) · memory project create→list→delete · longform job create→list→delete (no LLM tokens) · longform SSE endpoint reachability + headers · `/api/databases` · `/api/providers`.
4. Returns JSON `{ summary: {total, passed, failed}, results: [{name, category, status, detail, ms}] }`.
5. UI renders summary card (PASS=N/20 / FAIL=N) + per-row icon ✅/❌, name, detail, latency ms, grouped by category.

================================================================================
## PART 8: API REFERENCE

### Consultation & Search
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ask` | POST | Pose question → SSE stream (retrieval + tokens + sources + done) |
| `/api/positions/search` | GET | Search positions by thinker + query (`?thinker=&q=&limit=`) |
| `/api/databases` | GET | List configured thinker databases |
| `/api/providers` | GET | List enabled AI providers + models |
| `/api/topics/<thinker>` | GET | Topics / starter questions for a thinker |
| `/api/works` | GET | List source works in `texts/` |
| `/api/work/<work_id>` | GET | Full text of one work |
| `/api/random-quotes` | GET | Random position quotes (for splash) |
| `/api/answer-logs` | GET | Retrieval audit trail |

### Memory Mode
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/memory/projects` | GET / POST | List / create projects |
| `/api/memory/projects/:id` | DELETE | Delete project |
| `/api/memory/projects/:id/rename` | POST | Rename |
| `/api/memory/projects/:id/sessions` | GET / POST | List / create sessions |
| `/api/memory/sessions/:id` | PATCH / DELETE | Rename / delete session |
| `/api/memory/sessions/:id/transcript` | GET | Full transcript |
| `/api/memory/projects/:id/tractatus` | GET | Current tree |
| `/api/memory/projects/:id/memory-hierarchy` | GET | Current + archives + meta-trees |
| `/api/memory/ask` | POST | Memory-aware streaming ask |

### Longform
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/longform/coherent/start` | POST | Start job → `{ documentId }` |
| `/api/longform/coherent/:id/stream` | GET | SSE stream (snapshot/status/skeleton/section_start/section_complete/state/complete/error) |
| `/api/longform/coherent/:id` | GET | Full snapshot |
| `/api/longform/coherent/:id` | DELETE | Delete job |
| `/api/longform/coherent/:id/resume` | POST | Resume interrupted job |
| `/api/longform/coherent/list?thinker=…` | GET | List past jobs |
| `/api/longform/essay` | POST | Legacy single-shot essay |
| `/api/longform/document` | POST | Document-driven longform |

### Inference
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/inference/deduce` | POST | Run forward-chaining deduction |
| `/api/inference/search` | POST | Search rule base |
| `/api/inference/history` | POST | Past deductions |

### Ingestion
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upload` | POST | Upload position-file |
| `/api/upload/document` | POST | Upload PDF/DOCX/TXT for extraction |

### Session
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/login` | POST | Stub login |
| `/api/logout` | POST | Stub logout |
| `/api/check-session` | GET | Current session status |
| `/api/reset-conversation` | POST | Clear in-memory conversation |

### Diagnostic
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/diagnostic/run` | POST | Run 20-check self-test |

### Static / Misc
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Workshop UI |
| `/download-embeddings` | GET | Bulk embeddings export |
| `/raw_chain` | GET / POST | Raw deduction chain debug |

================================================================================
## PART 9: ENVIRONMENT SECRETS

| Secret | Required | Purpose |
|--------|----------|---------|
| `DATABASE_URL` | **YES** | Neon PostgreSQL connection string |
| `ANTHROPIC_API_KEY` | YES (for ZHI 1 + memory trees) | Claude consultation, Tractatus generation, Longform |
| `OPENAI_API_KEY` | **YES** | Embeddings (`text-embedding-3-small`) — without this, no semantic search. Also ZHI 2 consultation. |
| `DEEPSEEK_API_KEY` | YES (DEFAULT provider) | ZHI 4 consultation |
| `PERPLEXITY_API_KEY` | NO (optional ZHI 5) | Research-augmented consultation; provider hidden if unset |
| `XAI_API_KEY` | NO (optional ZHI 3) | Grok consultation; provider hidden if unset |
| `PGHOST` / `PGUSER` / `PGPASSWORD` / `PGDATABASE` / `PGPORT` | auto | Set by Replit alongside DATABASE_URL |

**Lazy-init policy:** all provider clients are wrapped in try/except at module load. A missing key disables that provider in `/api/providers` but does **not** crash the server.

================================================================================
## PART 10: KEY ARCHITECTURAL DECISIONS

### LAZY-INITIALIZED PROVIDER CLIENTS
Anthropic, OpenAI, DeepSeek, Perplexity, and Grok clients are each constructed in a try/except. Missing API keys do not crash startup; the provider simply doesn't appear in `/api/providers` and the diagnostic check for it reports FAIL with a clear reason.

### TWO-PROCESS ARCHITECTURE: FLASK + TYPESCRIPT LONGFORM SERVICE
The main app is Flask (port 5000). Long-form generation runs in a separate TypeScript / Express service (port 3001) so it can use streaming primitives, atomic DB transactions, worker leasing, and a richer typed state model without bloating the Flask process. Flask proxies all `/api/longform/coherent/*` requests to the TS service. The diagnostic verifies the TS service is reachable.

### NEUROTEXT-STYLE COHERENCE SKELETON FOR LONGFORM
Replaces the "many small essays cobbled together" failure mode. Two-tier skeleton (macro plan with distinct section roles → micro plan per section with explicit `must_not_repeat` lists), persistent state DB tracking claims_made / positions_cited / examples_used / open_threads / last_paragraph, and a READ→GENERATE→EXTRACT→MERGE→WRITE loop per section. Each section's first sentence must bridge from the prior section's last paragraph. Each section has a unique role (intro / distinction / objection / reply / synthesis / …). No two sections may have overlapping gists.

### RESUMABLE LONGFORM JOBS WITH WORKER LEASING
Jobs persist in `longform_documents`. Workers acquire a lease (`worker_id` + `lease_until`) before claiming a job, so duplicate workers can't pick up the same job. Interrupted jobs can be resumed from `current_section` via `POST /api/longform/coherent/:id/resume`. `commitSection` is atomic — section text + state-after snapshot land in the same transaction.

### MEMORY MODE: TRACTATUS TREES WITH TIERED ARCHIVAL
Project-scoped persistent memory. After each exchange, Claude updates a Wittgenstein-numbered tree (ASSERTS / REJECTS / ASSUMES / OPEN / RESOLVED). At 500 nodes → raw archive → compress to ~100 nodes → reset. At 10 archives → meta-tractatus (~150 nodes with SYNTHESIZES: tags). Prompt loads up to 3 most recent meta-trees (8K each) + current tree (12K) + cross-session messages (15K cap). Effectively unbounded conversation memory.

### DATABASE-GROUNDED RESPONSES WITH HARDENED PROMPT
The prompt forces the LLM to quote / paraphrase actual positions, refuses invention of terminology not in sources, and requires explicit acknowledgement when retrieved positions don't address the question. When `max_similarity < 0.25`, a low-relevance warning fires so the thinker acknowledges gaps rather than hallucinating.

### CONTEXT EXPANSION WITH 3-STRATEGY FALLBACK
`expand_with_context()` enriches retrieved positions with related/adjacent positions via: (1) explicit `related_positions` field, (2) same `work_id`, (3) list-index adjacency. Guarantees fuller argument context even when the source corpus lacks explicit cross-references.

### PER-THINKER FORWARD-CHAINING INFERENCE ENGINES
Six Python engines (`<thinker>_engine.py`) deduce theoretical conclusions from rule bases (`<thinker>_rules_full.json`) before LLM prose generation. The deduction chain (premises → intermediate steps → conclusion) is injected as a scaffold so answers reflect the thinker's reasoning, not paraphrase.

### SSE STREAMING WITH RETRIEVAL TRANSPARENCY
`/api/ask` emits a `retrieval` event before the first token containing positions scanned, similarity scores, domains covered. Users see *what* was retrieved before *what* was generated. Every query writes a complete audit row to `answer_logs`.

### AUTO-INGESTION VIA FILE WATCHER
`scripts/watch_ingest.py` runs as a background workflow polling `ingest/`. Drop a .txt / .json / .pdf / .docx file → it's extracted, embedded, inserted, and moved to `processed/` (or `failed/` with diagnostics). No manual scripting needed to add new corpora.

### SELF-DIAGNOSING APP (BETA TEST HARNESS)
`/api/diagnostic/run` is the canonical health-check. 20 checks across 3 categories. Exercises every external dependency (5 LLM providers + embeddings + DB + longform service) **and** the app's own HTTP surface (positions search, chat streaming, memory CRUD, longform CRUD, SSE headers) **and** validates required schema. Runs in ~10–20 seconds. Surfaces real bugs (stale model IDs, missing tables, exhausted API credits, broken SSE) before users do.

### CACHED EMBEDDINGS + CPU-ONLY PYTORCH
Per-position embeddings are pre-computed and cached on the row (`embedding` column). Search is a cosine-similarity sweep in NumPy / scikit-learn — no GPU required. Replit-compatible.

### AUTH DEFERRED — DIAGNOSTIC FIRST
Login / logout endpoints are stubbed for the beta phase. The DIAGNOSTIC button is unauthenticated so the app can be exercised end-to-end without an account. Auth hardening is a post-beta task.

### THINKER ORGANIZATION: PRIMARY vs RELATED
Primary thinkers (Freud, ZHI/Kuczynski, Jung) live in the main input section as large avatars. Related/ancillary thinkers (Hume, Nietzsche, Bergler) live in a compact header strip with smaller avatars and inline counts. Reflects corpus size and conceptual centrality.
