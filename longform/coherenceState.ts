import pg from "pg";
import { randomUUID } from "crypto";

const { Pool } = pg;
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export const WORKER_ID = randomUUID();
export const LEASE_TTL_SECONDS = 180; // a section finishing within 3 minutes refreshes lease

export interface SkeletonSection {
  index: number;
  title: string;
  role: string;
  word_target: number;
  claims_to_make: string[];
  positions_to_use: string[];
  examples_to_use: string[];
  bridge_from_prior: string;
  bridge_to_next: string;
  must_not_repeat: string[];
}

export interface Skeleton {
  thesis: string;
  central_concepts: string[];
  arc: string;
  sections: SkeletonSection[];
}

export interface LongFormState {
  thesis: string;
  central_concepts: string[];
  claims_made: string[];
  positions_cited: string[];
  examples_used: string[];
  open_threads: string[];
  resolved_threads: string[];
  section_summaries: { i: number; title: string; summary: string }[];
  last_paragraph: string;
  current_stage: string;
}

export interface StateUpdate {
  new_claims: string[];
  new_positions_cited: string[];
  new_examples: string[];
  new_open_threads: string[];
  resolved: string[];
  section_summary: string;
  last_paragraph: string;
  next_stage?: string;
}

export interface DocumentRecord {
  document_id: string;
  thinker: string;
  user_prompt: string;
  mode: string;
  target_words: number;
  total_sections: number;
  current_section: number;
  skeleton: Skeleton | null;
  state: LongFormState;
  status: string;
  error?: string | null;
  worker_id?: string | null;
  lease_until?: Date | null;
}

export function emptyState(): LongFormState {
  return {
    thesis: "",
    central_concepts: [],
    claims_made: [],
    positions_cited: [],
    examples_used: [],
    open_threads: [],
    resolved_threads: [],
    section_summaries: [],
    last_paragraph: "",
    current_stage: "intro",
  };
}

function uniqueAppend(existing: string[], incoming: string[], cap: number): string[] {
  const set = new Set(existing.map((s) => s.trim().toLowerCase()));
  const out = [...existing];
  for (const item of incoming) {
    const key = item.trim().toLowerCase();
    if (key && !set.has(key)) {
      set.add(key);
      out.push(item.trim());
    }
  }
  if (out.length > cap) return out.slice(out.length - cap);
  return out;
}

export function applyStateUpdate(
  state: LongFormState,
  update: StateUpdate,
  sectionIndex: number,
  sectionTitle: string
): LongFormState {
  const next: LongFormState = {
    ...state,
    // Larger caps for 50K-word horizon: 25 sections × ~10 claims = 250
    claims_made: uniqueAppend(state.claims_made, update.new_claims || [], 600),
    positions_cited: uniqueAppend(state.positions_cited, update.new_positions_cited || [], 600),
    examples_used: uniqueAppend(state.examples_used, update.new_examples || [], 300),
    open_threads: uniqueAppend(
      (state.open_threads || []).filter(
        (t) =>
          !(update.resolved || []).some(
            (r) => r.trim().toLowerCase() === t.trim().toLowerCase()
          )
      ),
      update.new_open_threads || [],
      80
    ),
    resolved_threads: uniqueAppend(state.resolved_threads, update.resolved || [], 200),
    section_summaries: [
      ...(state.section_summaries || []),
      {
        i: sectionIndex,
        title: sectionTitle,
        summary: (update.section_summary || "").trim(),
      },
    ].slice(-100),
    last_paragraph: (update.last_paragraph || state.last_paragraph || "").trim(),
    current_stage: update.next_stage || state.current_stage,
  };
  return next;
}

// Reconstruct full state by replaying state_after from sections in order.
// Used as a safety net during resume to defend against any state drift.
export async function reconstructStateFromSections(documentId: string): Promise<{ state: LongFormState | null; lastSectionIndex: number }> {
  const r = await pool.query(
    `SELECT section_index, state_after FROM longform_sections
     WHERE document_id = $1 ORDER BY section_index DESC LIMIT 1`,
    [documentId]
  );
  if (!r.rows.length) return { state: null, lastSectionIndex: -1 };
  return { state: r.rows[0].state_after, lastSectionIndex: r.rows[0].section_index };
}

export async function ensureSchema(): Promise<void> {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS longform_documents (
      id SERIAL PRIMARY KEY,
      document_id TEXT UNIQUE NOT NULL,
      thinker TEXT NOT NULL,
      user_prompt TEXT NOT NULL,
      mode TEXT DEFAULT 'essay',
      target_words INTEGER DEFAULT 15000,
      total_sections INTEGER DEFAULT 0,
      current_section INTEGER DEFAULT 0,
      skeleton JSONB,
      state JSONB DEFAULT '{}'::jsonb,
      status TEXT DEFAULT 'planning',
      error TEXT,
      worker_id TEXT,
      lease_until TIMESTAMP,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    )
  `);
  await pool.query(`
    CREATE TABLE IF NOT EXISTS longform_sections (
      id SERIAL PRIMARY KEY,
      document_id TEXT NOT NULL,
      section_index INTEGER NOT NULL,
      section_title TEXT,
      section_plan JSONB,
      section_text TEXT,
      word_count INTEGER DEFAULT 0,
      state_after JSONB,
      created_at TIMESTAMP DEFAULT NOW(),
      UNIQUE(document_id, section_index)
    )
  `);
  // Bring older deployments forward
  await pool.query(`ALTER TABLE longform_documents ADD COLUMN IF NOT EXISTS worker_id TEXT`);
  await pool.query(`ALTER TABLE longform_documents ADD COLUMN IF NOT EXISTS lease_until TIMESTAMP`);
  await pool.query(`CREATE INDEX IF NOT EXISTS idx_longform_sections_doc ON longform_sections(document_id)`);
  await pool.query(`CREATE INDEX IF NOT EXISTS idx_longform_documents_status ON longform_documents(status)`);
  await pool.query(`CREATE INDEX IF NOT EXISTS idx_longform_lease ON longform_documents(worker_id, lease_until)`);
}

export async function createDocument(record: Omit<DocumentRecord, "current_section" | "status" | "skeleton" | "state" | "total_sections"> & { total_sections?: number }): Promise<void> {
  await pool.query(
    `INSERT INTO longform_documents
     (document_id, thinker, user_prompt, mode, target_words, total_sections, status, state, updated_at)
     VALUES ($1,$2,$3,$4,$5,$6,'planning',$7::jsonb,NOW())`,
    [
      record.document_id,
      record.thinker,
      record.user_prompt,
      record.mode,
      record.target_words,
      record.total_sections || 0,
      JSON.stringify(emptyState()),
    ]
  );
}

export async function saveSkeleton(documentId: string, skeleton: Skeleton): Promise<void> {
  const initState = emptyState();
  initState.thesis = skeleton.thesis;
  initState.central_concepts = skeleton.central_concepts || [];
  await pool.query(
    `UPDATE longform_documents
     SET skeleton = $1::jsonb,
         total_sections = $2,
         status = 'generating',
         state = $3::jsonb,
         updated_at = NOW()
     WHERE document_id = $4`,
    [JSON.stringify(skeleton), skeleton.sections.length, JSON.stringify(initState), documentId]
  );
}

export async function readDocument(documentId: string): Promise<DocumentRecord | null> {
  const r = await pool.query(
    `SELECT document_id, thinker, user_prompt, mode, target_words, total_sections,
            current_section, skeleton, state, status, error, worker_id, lease_until
     FROM longform_documents WHERE document_id = $1`,
    [documentId]
  );
  if (!r.rows.length) return null;
  const row = r.rows[0];
  return {
    document_id: row.document_id,
    thinker: row.thinker,
    user_prompt: row.user_prompt,
    mode: row.mode,
    target_words: row.target_words,
    total_sections: row.total_sections,
    current_section: row.current_section,
    skeleton: row.skeleton,
    state: row.state || emptyState(),
    status: row.status,
    error: row.error,
    worker_id: row.worker_id,
    lease_until: row.lease_until,
  };
}

/**
 * Atomically commit one section: write the section row, update document state +
 * current_section pointer, and refresh the lease — all in a single transaction.
 */
export async function commitSection(
  documentId: string,
  sectionIndex: number,
  title: string,
  plan: SkeletonSection,
  text: string,
  stateAfter: LongFormState
): Promise<void> {
  const wordCount = text.split(/\s+/).filter(Boolean).length;
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    await client.query(
      `INSERT INTO longform_sections
        (document_id, section_index, section_title, section_plan, section_text, word_count, state_after)
       VALUES ($1,$2,$3,$4::jsonb,$5,$6,$7::jsonb)
       ON CONFLICT (document_id, section_index)
       DO UPDATE SET section_text = EXCLUDED.section_text,
                     word_count = EXCLUDED.word_count,
                     state_after = EXCLUDED.state_after,
                     section_plan = EXCLUDED.section_plan,
                     section_title = EXCLUDED.section_title`,
      [documentId, sectionIndex, title, JSON.stringify(plan), text, wordCount, JSON.stringify(stateAfter)]
    );
    await client.query(
      `UPDATE longform_documents
       SET state = $1::jsonb,
           current_section = GREATEST(current_section, $2),
           lease_until = NOW() + ($3 || ' seconds')::interval,
           updated_at = NOW()
       WHERE document_id = $4`,
      [JSON.stringify(stateAfter), sectionIndex + 1, String(LEASE_TTL_SECONDS), documentId]
    );
    await client.query("COMMIT");
  } catch (e) {
    await client.query("ROLLBACK");
    throw e;
  } finally {
    client.release();
  }
}

export async function readSections(documentId: string): Promise<{ section_index: number; section_title: string; section_text: string; word_count: number }[]> {
  const r = await pool.query(
    `SELECT section_index, section_title, section_text, word_count
     FROM longform_sections WHERE document_id = $1 ORDER BY section_index ASC`,
    [documentId]
  );
  return r.rows;
}

export async function setStatus(documentId: string, status: string, errorMsg?: string): Promise<void> {
  if (status === "complete" || status === "failed" || status === "paused") {
    // Release the lease when terminal/paused
    if (errorMsg) {
      await pool.query(
        `UPDATE longform_documents SET status = $1, error = $2, worker_id = NULL, lease_until = NULL, updated_at = NOW() WHERE document_id = $3`,
        [status, errorMsg, documentId]
      );
    } else {
      await pool.query(
        `UPDATE longform_documents SET status = $1, error = NULL, worker_id = NULL, lease_until = NULL, updated_at = NOW() WHERE document_id = $2`,
        [status, documentId]
      );
    }
  } else {
    if (errorMsg) {
      await pool.query(
        `UPDATE longform_documents SET status = $1, error = $2, updated_at = NOW() WHERE document_id = $3`,
        [status, errorMsg, documentId]
      );
    } else {
      await pool.query(
        `UPDATE longform_documents SET status = $1, error = NULL, updated_at = NOW() WHERE document_id = $2`,
        [status, documentId]
      );
    }
  }
}

/**
 * Try to acquire a lease on a document for this worker. Returns true if acquired.
 * Refuses if another worker holds an unexpired lease.
 */
export async function acquireLease(documentId: string): Promise<boolean> {
  const r = await pool.query(
    `UPDATE longform_documents
     SET worker_id = $1,
         lease_until = NOW() + ($2 || ' seconds')::interval,
         updated_at = NOW()
     WHERE document_id = $3
       AND status NOT IN ('complete')
       AND (worker_id IS NULL OR worker_id = $1 OR lease_until IS NULL OR lease_until < NOW())
     RETURNING document_id`,
    [WORKER_ID, String(LEASE_TTL_SECONDS), documentId]
  );
  return r.rowCount! > 0;
}

export async function refreshLease(documentId: string): Promise<void> {
  await pool.query(
    `UPDATE longform_documents
     SET lease_until = NOW() + ($1 || ' seconds')::interval,
         updated_at = NOW()
     WHERE document_id = $2 AND worker_id = $3`,
    [String(LEASE_TTL_SECONDS), documentId, WORKER_ID]
  );
}

export async function releaseLease(documentId: string): Promise<void> {
  await pool.query(
    `UPDATE longform_documents
     SET worker_id = NULL, lease_until = NULL, updated_at = NOW()
     WHERE document_id = $1 AND worker_id = $2`,
    [documentId, WORKER_ID]
  );
}

export async function listDocuments(thinker?: string, limit = 30): Promise<any[]> {
  const params: any[] = [];
  let where = "";
  if (thinker) {
    params.push(thinker);
    where = `WHERE thinker = $1`;
  }
  params.push(limit);
  const r = await pool.query(
    `SELECT document_id, thinker, user_prompt, mode, target_words, total_sections,
            current_section, status, created_at, updated_at, worker_id, lease_until,
            COALESCE((SELECT SUM(word_count) FROM longform_sections WHERE document_id = ld.document_id), 0) AS total_words
     FROM longform_documents ld
     ${where}
     ORDER BY updated_at DESC
     LIMIT $${params.length}`,
    params
  );
  return r.rows;
}

export async function deleteDocument(documentId: string): Promise<void> {
  await pool.query(`DELETE FROM longform_sections WHERE document_id = $1`, [documentId]);
  await pool.query(`DELETE FROM longform_documents WHERE document_id = $1`, [documentId]);
}
