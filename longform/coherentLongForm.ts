import { randomUUID } from "crypto";
import {
  createDocument,
  saveSkeleton,
  readDocument,
  commitSection,
  readSections,
  setStatus,
  applyStateUpdate,
  reconstructStateFromSections,
  emptyState,
  acquireLease,
  refreshLease,
  releaseLease,
  WORKER_ID,
  LongFormState,
} from "./coherenceState";
import { generateSkeleton } from "./generateSkeleton";
import { generateCoherentSection, extractStateUpdate } from "./generateCoherentSection";

export interface StartParams {
  thinker: string;
  prompt: string;
  mode?: string; // essay | dialogue | lecture
  targetWords?: number;
}

export type ProgressEvent =
  | { type: "status"; status: string; message: string }
  | { type: "skeleton"; skeleton: any }
  | { type: "section_start"; index: number; total: number; title: string; role: string; wordTarget: number }
  | { type: "section_complete"; index: number; total: number; title: string; text: string; wordCount: number; cumulativeWords: number }
  | { type: "state"; state: any }
  | { type: "complete"; documentId: string; totalWords: number; totalSections: number }
  | { type: "error"; message: string };

export async function startCoherentLongForm(
  params: StartParams,
  onEvent?: (e: ProgressEvent) => void
): Promise<string> {
  const documentId = randomUUID();
  const thinker = params.thinker;
  const prompt = params.prompt;
  const mode = params.mode || "essay";
  const targetWords = Math.max(2000, Math.min(80000, params.targetWords || 15000));

  await createDocument({
    document_id: documentId,
    thinker,
    user_prompt: prompt,
    mode,
    target_words: targetWords,
  });

  // Kick off async processing — do not await
  runCoherentJob(documentId, onEvent).catch((err) => {
    console.error(`Job ${documentId} failed:`, err);
    setStatus(documentId, "failed", String(err)).catch(() => {});
    onEvent?.({ type: "error", message: String(err) });
  });

  return documentId;
}

export async function runCoherentJob(
  documentId: string,
  onEvent?: (e: ProgressEvent) => void
): Promise<void> {
  // Acquire exclusive lease before doing any work
  const acquired = await acquireLease(documentId);
  if (!acquired) {
    const doc = await readDocument(documentId);
    const heldBy = doc?.worker_id || "unknown";
    const leaseUntil = doc?.lease_until ? new Date(doc.lease_until).toISOString() : "?";
    throw new Error(
      `Job ${documentId} is locked (status=${doc?.status}, worker=${heldBy}, lease_until=${leaseUntil}). Cannot start a second runner.`
    );
  }

  const doc = await readDocument(documentId);
  if (!doc) throw new Error(`Document ${documentId} not found`);

  // Heartbeat: refresh the lease every 60s while the job runs
  const heartbeat = setInterval(() => {
    refreshLease(documentId).catch((e) => console.error(`Lease refresh failed for ${documentId}:`, e));
  }, 60_000);

  try {
    onEvent?.({ type: "status", status: "planning", message: "Building coherence skeleton..." });

    let skeleton = doc.skeleton;
    if (!skeleton) {
      skeleton = await generateSkeleton(
        doc.thinker,
        doc.user_prompt,
        doc.mode,
        doc.target_words,
        (msg) => onEvent?.({ type: "status", status: "planning", message: msg })
      );
      await saveSkeleton(documentId, skeleton);
    }
    onEvent?.({ type: "skeleton", skeleton });

    // Reload state after skeleton save (it now has thesis/central_concepts populated)
    const refreshed = await readDocument(documentId);
    const baseDoc = refreshed || doc;
    let state: LongFormState = baseDoc.state || emptyState();

    // Resume safety: if sections exist, prefer the latest section's state_after as ground truth
    const existingSections = await readSections(documentId);
    let startSection = baseDoc.current_section || 0;
    if (existingSections.length > 0) {
      const recon = await reconstructStateFromSections(documentId);
      if (recon.state) {
        state = recon.state;
      }
      startSection = Math.max(startSection, existingSections[existingSections.length - 1].section_index + 1);
    }

    onEvent?.({
      type: "status",
      status: "generating",
      message: `Skeleton built (${skeleton.sections.length} sections). Generating from section ${startSection + 1}...`,
    });
    await setStatus(documentId, "generating");

    let cumulativeWords = existingSections.reduce((sum, s) => sum + (s.word_count || 0), 0);

    for (let i = startSection; i < skeleton.sections.length; i++) {
      const sectionPlan = skeleton.sections[i];

      onEvent?.({
        type: "section_start",
        index: i,
        total: skeleton.sections.length,
        title: sectionPlan.title,
        role: sectionPlan.role,
        wordTarget: sectionPlan.word_target,
      });

      const text = await generateCoherentSection(doc.thinker, skeleton, state, sectionPlan, doc.mode);
      const update = await extractStateUpdate(doc.thinker, sectionPlan, text, state, skeleton);
      const newState = applyStateUpdate(state, update, i, sectionPlan.title);

      // Atomic: section row + document state + current_section, all in one transaction
      await commitSection(documentId, i, sectionPlan.title, sectionPlan, text, newState);

      state = newState;
      const wc = text.split(/\s+/).filter(Boolean).length;
      cumulativeWords += wc;

      onEvent?.({
        type: "section_complete",
        index: i,
        total: skeleton.sections.length,
        title: sectionPlan.title,
        text,
        wordCount: wc,
        cumulativeWords,
      });
      onEvent?.({ type: "state", state: newState });
    }

    await setStatus(documentId, "complete");
    onEvent?.({
      type: "complete",
      documentId,
      totalWords: cumulativeWords,
      totalSections: skeleton.sections.length,
    });
  } catch (err) {
    console.error(`Job ${documentId} error:`, err);
    await setStatus(documentId, "failed", String(err));
    onEvent?.({ type: "error", message: String(err) });
    throw err;
  } finally {
    clearInterval(heartbeat);
    try { await releaseLease(documentId); } catch {}
  }
}
