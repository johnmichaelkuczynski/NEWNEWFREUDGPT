# FreudGPT - The Thinker's Workshop

## Overview
FreudGPT is an intelligent conversational AI application designed to provide in-depth, streaming responses grounded in the works of various thinkers in psychology and philosophy. It aims to make extensive philosophical works accessible and interactive through semantic search over comprehensive databases. The project's vision is to evolve from simple impersonation to "executable philosophical reasoning" by employing forward-chaining inference engines to deduce theoretical principles before generating LLM prose. The application currently supports Freud (with supplementary positions from Kernberg, Reich, Stekel, and Bergler), Kuczynski, Jung, Hume, and Nietzsche, encompassing approximately 24,532 unique philosophical positions (including 257 Bergler positions).

## User Preferences
- **App Name**: The app's name is **FreudGPT**. Use this name in the README, the app UI, the promo video, the YouTube description, and anywhere else relevant.
- **YouTube Title Format**: The title in any YouTube description must be exactly `FreudGPT`. It is NOT a course — never append "course", "AI-Powered Course", taglines, descriptors, or sales language to the title.
- **API Integration**: Prefers direct Anthropic API integration over Replit AI Integrations
- **Response Style**: AI responses must faithfully represent Kuczynski's actual arguments, examples, and rigorous writing style, not glib paraphrases. This means quoting or very closely paraphrasing the actual text from positions, using his exact examples and rhetorical questions, preserving his step-by-step argumentative structure, and matching his rigorous, technical, methodical, and detailed tone. The AI should not summarize, simplify, or "make accessible" his work.
- **Argumentation**: The AI prompt is configured to not argue against user input when they present a position; it defaults to SUPPORT/EXPAND mode, but acknowledges mismatches if retrieved positions conflict.
- **Database-Grounded Responses**: The prompt is designed to make database positions the PRIMARY content source. When low-relevance is detected (similarity < 0.25), the system warns the thinker to acknowledge gaps honestly rather than hallucinate. The LLM is constrained to: (1) quote verbatim or very closely paraphrase database positions, (2) refuse to invent terminology not in the sources, (3) explicitly acknowledge when retrieved positions don't address the question. This ensures faithful presentation of actual philosophical content.

## Recent Changes (May 2026 - LONGFORM COHERENCE SKELETON)

### NeuroText-style Long-form Generation
- **Goal**: Generate coherent, non-self-repetitive long outputs (up to ~50K words) for essays, dialogues, and lectures. Replaces the prior "many small essays cobbled together" failure mode.
- **Architecture (adapted from NeuroText)**:
  - **Two-tier skeleton** (`longform/generateSkeleton.ts`): macro plan (thesis + arc + N sections with distinct roles & word targets) → micro plan per section (claims_to_make, positions_to_use, examples_to_use, bridge_from_prior, bridge_to_next, must_not_repeat).
  - **Persistent state DB** (`longform_documents` + `longform_sections` tables in PostgreSQL): tracks `claims_made`, `positions_cited`, `examples_used`, `open_threads`, `resolved_threads`, `section_summaries`, `last_paragraph`, `current_stage` across the entire generation.
  - **READ → GENERATE → EXTRACT → MERGE → WRITE pattern** per section (`longform/coherentLongForm.ts`):
    1. READ accumulated state from DB
    2. GENERATE section with skeleton + state + RAG positions + anti-repetition lists
    3. EXTRACT state delta (`extractStateUpdate` LLM call returns JSON: new claims, new examples, resolved/new threads, last_paragraph)
    4. MERGE delta into state with deduplication
    5. WRITE section + new state to DB
  - **Resume support**: jobs persist; can be resumed via `POST /longform/coherent/:id/resume`.
- **Modes**: `essay` (continuous argument), `dialogue` (named interlocutor turns), `lecture` (numbered teaching units). Mode-specific skeleton prompts and section prompts.
- **Anti-repetition**: each section prompt explicitly lists prior claims & examples that MUST NOT be restated. Each macro section has a unique role (intro / distinction / objection / reply / synthesis / etc.) — no two sections may have overlapping gists.
- **Bridging**: each section's first sentence must continue from the prior section's last paragraph (carried in state). No "Section N:" headings, no "in conclusion" phrasing.
- **Endpoints (TypeScript service on :3001, proxied through Flask)**:
  - `POST /api/longform/coherent/start` — kick off job, returns `documentId`
  - `GET /api/longform/coherent/:id/stream` — SSE: `snapshot`, `status`, `skeleton`, `section_start`, `section_complete`, `state`, `complete`, `error`
  - `GET /api/longform/coherent/:id` — full snapshot
  - `POST /api/longform/coherent/:id/resume` — resume interrupted job
  - `DELETE /api/longform/coherent/:id` — delete job
  - `GET /api/longform/coherent/list?thinker=...` — list past jobs
- **UI**: "Longform" button in header opens modal with thinker/mode/word-target/prompt inputs. Live progress shows skeleton (collapsible), per-section streaming with role tags, cumulative word counter, and download-as-text. History view with resume/delete.
- **DB tables**: `longform_documents` (id, document_id UUID, thinker, user_prompt, mode, target_words, total_sections, current_section, skeleton JSONB, state JSONB, status, error, timestamps); `longform_sections` (id, document_id, section_index, section_title, section_plan JSONB, section_text, word_count, state_after JSONB, unique on (doc_id, section_index)).
- **Files added**: `longform/coherenceState.ts`, `longform/generateSkeleton.ts`, `longform/generateCoherentSection.ts`, `longform/coherentLongForm.ts`. `longform/server.ts` extended with new routes.

## Recent Changes (January 2026 - RESTORE POINT)

### Argument Synthesis Architecture (Major Prompt Overhaul)
- **From Quote-Stitching to Argument Synthesis**: Prompt rewritten to instruct LLM to UNDERSTAND the arguments in retrieved positions and synthesize them into coherent answers, rather than mechanically stitching quotes together.
- **Answer Structure**: Responses now follow thesis → supporting reasons → conclusion structure.
- **Grounding Balance**: Maintains strict database grounding ("every major claim must be traceable to a specific position") while allowing natural prose presentation.
- **Minimum Paraphrase Requirement**: Each response must include at least N close paraphrases from specific positions (tied to quote_count setting).

### Context Expansion System
- **expand_with_context()**: New method in search.py that fetches related/adjacent positions for fuller argument context.
- **Three fallback strategies**: (1) Explicit related_positions field, (2) Adjacent positions from same work_id, (3) List-index based adjacency as fallback.
- **All DB formats supported**: Added work_id, related_positions, and list_index to all position loading branches.

### Retrieval Transparency
- **Real-time SSE streaming**: Retrieval metadata (positions scanned, similarity scores, domains) streamed to frontend before AI response.
- **answer_logs table**: PostgreSQL table storing complete audit trail per query.
- **Context expansion logged**: Metadata includes context_positions_added and total_positions_used.

### Memory Mode (Tractatus Trees)
- **Two modes**: Free-form (no memory, default) and Memory Mode (project-based persistent memory)
- **Projects**: Scoped per thinker. Each project has a Tractatus tree (JSONB knowledge graph)
- **Sessions**: Multiple chat sessions per project, each with stored transcript
- **Tractatus Tree**: After each exchange, Claude analyzes conversation and updates tree with Wittgenstein-style numbered nodes (ASSERTS, REJECTS, ASSUMES, OPEN, RESOLVED)
- **Compression**: When tree hits 500 nodes → archived → compressed to ~100 nodes → reset
- **Meta-Tractatus**: Every 10 archived trees → Claude generates a ~150-node meta-tree synthesizing thousands of exchanges. Uses SYNTHESIZES: tag for cross-tree patterns. Up to 3 most recent meta-trees loaded into prompt (8K chars each)
- **Tiered Memory**: Meta-trees (8K each) + current tree (12K chars) + archived tiers loaded into prompt with decreasing budgets
- **Download**: Users can download all trees (current + archives + meta-trees) as JSON from the tree viewer
- **Default ON**: Memory Mode is enabled by default
- **Cross-session context**: Recent messages from other sessions in same project (15K cap)
- **DB tables**: memory_projects, memory_sessions, tractatus_archive, meta_tractatus
- **API**: /api/memory/* endpoints for CRUD + /api/memory/ask for memory-aware chat

### Formatting
- Responses use plain prose only - no markdown (**, ##), no source citations (Source 1, etc.)
- Source positions sent without numbering labels
- LLM never refuses to answer - always engages even with tangential positions

### Auto-Ingestion
- File watcher (scripts/watch_ingest.py) monitors `ingest/` folder
- Supports .txt, .json, .pdf, .docx files
- Processed files moved to ingest/processed/, failed to ingest/failed/
- Runs as background workflow (ingest-watcher)

## System Architecture

### UI/UX: The Thinker's Workshop
- **Theme**: Bright Wellness with a color palette of deep teal (#0F766E), warm off-white (#FFFDFB), light mint (#F0FDFA), and coral-orange accents (#F97316).
- **Typography**: Playfair Display (headings), Inter (body), Crimson Pro (quotes).
- **Layout**: Dual-panel design with "The Dialogue" (70%) for real-time AI responses and "The Archive" (30%) for synchronized source texts. Panels are resizable and settings persist.
- **Thinker Organization**: Primary thinkers (Freud, ZHI, Jung) in the main input section; related/ancillary thinkers (Hume, Nietzsche, Bergler) in a header strip.
- **Interactive Features**: Avatar-based thinker selection, knowledge panel popups, source highlighting, styled controls, in-app reader for full philosophical works (from `texts/` folder), and animations (orbiting emojis, typewriter effects, panel transitions).

### Technical Implementations
- **Core Functionality**: Multi-database support (Freud, Kuczynski, Jung, Hume, Nietzsche, Bergler), semantic search, streaming AI responses, multi-AI provider integration, conversation memory with self-contradiction detection, content ingestion (PDF, DOCX), and source citations.
- **Response Modes**: 
  - **Standard Mode**: Strict word count and quote requirements based on slider settings. Detailed, comprehensive responses with mandatory minimum lengths.
  - **Dialogue Mode**: Natural conversational interaction where the thinker can give short answers when appropriate, ask clarifying questions, challenge the user's assumptions, and push back intellectually. No strict length requirements - responses adapt to the question's complexity.
  - **Enhanced Toggle**: Enables creative theoretical extension and modern knowledge integration.
- **Backend**: Flask for application logic, SSE streaming, and semantic search integration.
- **Frontend**: Minimal HTML, CSS, and vanilla JavaScript.
- **Data Management**: Philosophical positions stored in PostgreSQL database (Neon) with 22,937 positions across 6 thinkers. Semantic search uses cached pre-computed embeddings. Databases and embeddings are lazy-loaded. JSON files retained as backup.
- **ML/NLP**: OpenAI's `text-embedding-3-small` for embeddings, scikit-learn for cosine similarity. `PyPDF2` and `python-docx` for text extraction.
- **Design Decisions**: Emphasizes faithful representation of thinkers' styles, token-by-token streaming, a simplified data model focusing on philosophical positions, and CPU-only PyTorch for Replit compatibility. Prompt hardening ensures verbatim quotes and exact formulations. Canonical Query Mapping is used for key philosophical queries.

## External Dependencies
- **AI Providers**: Anthropic Claude, OpenAI, DeepSeek, Perplexity, Grok (xAI).
- **Python Libraries**: Flask, sentence-transformers, scikit-learn, PyTorch (CPU), PyPDF2, python-docx, Gunicorn, gevent, psycopg2-binary.

## Database Schema
- **PostgreSQL Table**: `positions`
  - `id` (SERIAL PRIMARY KEY)
  - `position_id` (TEXT UNIQUE) - Original ID from JSON sources
  - `thinker` (TEXT) - freud, jung, kuczynski, hume, nietzsche, bergler
  - `title` (TEXT) - Position title/topic
  - `text_evidence` (TEXT) - The philosophical position text
  - `domain` (TEXT) - Philosophy domain category
  - `source` (TEXT), `work_title` (TEXT), `year` (INTEGER)
- **Migration Script**: `migrate_to_postgres.py` imports JSON to PostgreSQL
- **API Endpoint**: `/api/positions/search?thinker=freud&q=search_term&limit=50`
- **RAG Table**: `text_chunks` - 4,489 chunks from source texts (texts/ folder)
  - `id`, `thinker`, `source_file`, `chunk_text`, `chunk_index`
  - Chunking script: `chunk_texts.py`
  - RAG search uses PostgreSQL full-text search with ts_rank scoring