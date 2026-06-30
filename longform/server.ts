import http from "http";
import { freudLongForm } from "./freudLongForm";
import { kuczynskiLongForm } from "./kuczynskiLongForm";
import { jungLongForm } from "./jungLongForm";
import { nietzscheLongForm } from "./nietzscheLongForm";
import { berglerLongForm } from "./berglerLongForm";
import { humeLongForm } from "./humeLongForm";
import { processDocumentTask } from "./processDocumentTask";
import { generateLongFormEssay } from "./generateLongFormEssay";
import {
  startCoherentLongForm,
  runCoherentJob,
  ProgressEvent,
} from "./coherentLongForm";
import {
  readDocument,
  readSections,
  listDocuments,
  setStatus,
  deleteDocument,
  ensureSchema,
} from "./coherenceState";

const PORT = 3001;

const longFormHandlers: Record<string, (topic: string) => Promise<string>> = {
  freud: freudLongForm,
  kuczynski: kuczynskiLongForm,
  jung: jungLongForm,
  nietzsche: nietzscheLongForm,
  bergler: berglerLongForm,
  hume: humeLongForm,
};

// In-process pub/sub for SSE clients
type Listener = (e: ProgressEvent) => void;
const listeners: Map<string, Set<Listener>> = new Map();

function emit(documentId: string, event: ProgressEvent) {
  const set = listeners.get(documentId);
  if (set) for (const fn of set) try { fn(event); } catch {}
}

function subscribe(documentId: string, fn: Listener): () => void {
  if (!listeners.has(documentId)) listeners.set(documentId, new Set());
  listeners.get(documentId)!.add(fn);
  return () => {
    const set = listeners.get(documentId);
    if (set) {
      set.delete(fn);
      if (set.size === 0) listeners.delete(documentId);
    }
  };
}

async function readJsonBody(req: http.IncomingMessage): Promise<any> {
  let body = "";
  for await (const chunk of req) body += chunk;
  return body ? JSON.parse(body) : {};
}

function sendJson(res: http.ServerResponse, status: number, payload: any) {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify(payload));
}

async function handleSSE(documentId: string, req: http.IncomingMessage, res: http.ServerResponse) {
  res.writeHead(200, {
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache, no-transform",
    Connection: "keep-alive",
    "X-Accel-Buffering": "no",
  });

  // Send initial snapshot of doc + already-completed sections so client can resume display
  const doc = await readDocument(documentId);
  if (!doc) {
    res.write(`event: error\ndata: ${JSON.stringify({ message: "Document not found" })}\n\n`);
    res.end();
    return;
  }

  res.write(`event: snapshot\ndata: ${JSON.stringify({
    document_id: documentId,
    thinker: doc.thinker,
    user_prompt: doc.user_prompt,
    mode: doc.mode,
    target_words: doc.target_words,
    total_sections: doc.total_sections,
    current_section: doc.current_section,
    status: doc.status,
    skeleton: doc.skeleton,
    state: doc.state,
  })}\n\n`);

  const sections = await readSections(documentId);
  for (const s of sections) {
    res.write(`event: section_complete\ndata: ${JSON.stringify({
      index: s.section_index,
      total: doc.total_sections,
      title: s.section_title,
      text: s.section_text,
      wordCount: s.word_count,
    })}\n\n`);
  }

  if (doc.status === "complete") {
    res.write(`event: complete\ndata: ${JSON.stringify({ documentId })}\n\n`);
    res.end();
    return;
  }
  if (doc.status === "failed") {
    res.write(`event: error\ndata: ${JSON.stringify({ message: doc.error || "Job failed" })}\n\n`);
    res.end();
    return;
  }

  // Live subscription
  const heartbeat = setInterval(() => {
    try { res.write(`: keepalive\n\n`); } catch {}
  }, 15000);

  const unsubscribe = subscribe(documentId, (event) => {
    try {
      res.write(`event: ${event.type}\ndata: ${JSON.stringify(event)}\n\n`);
      if (event.type === "complete" || event.type === "error") {
        clearInterval(heartbeat);
        unsubscribe();
        res.end();
      }
    } catch {}
  });

  req.on("close", () => {
    clearInterval(heartbeat);
    unsubscribe();
  });
}

async function handleRequest(req: http.IncomingMessage, res: http.ServerResponse) {
  const url = req.url || "";
  const method = req.method || "GET";

  try {
    // SSE stream for coherent jobs
    const sseMatch = url.match(/^\/longform\/coherent\/([^/]+)\/stream$/);
    if (sseMatch && method === "GET") {
      return handleSSE(sseMatch[1], req, res);
    }

    if (url === "/longform/coherent/start" && method === "POST") {
      const data = await readJsonBody(req);
      const { thinker, prompt, mode, targetWords } = data;
      if (!thinker || !prompt) return sendJson(res, 400, { error: "thinker and prompt are required" });

      const idRef: { id: string } = { id: "" };
      const documentId = await startCoherentLongForm(
        { thinker, prompt, mode, targetWords },
        (event) => { if (idRef.id) emit(idRef.id, event); }
      );
      idRef.id = documentId;

      return sendJson(res, 200, { success: true, documentId });
    }

    if (url.startsWith("/longform/coherent/list") && method === "GET") {
      const params = new URL(`http://x${url}`).searchParams;
      const thinker = params.get("thinker") || undefined;
      const limit = parseInt(params.get("limit") || "30", 10);
      const docs = await listDocuments(thinker, limit);
      return sendJson(res, 200, { documents: docs });
    }

    const resumeMatch = url.match(/^\/longform\/coherent\/([^/]+)\/resume$/);
    if (resumeMatch && method === "POST") {
      const docId = resumeMatch[1];
      const doc = await readDocument(docId);
      if (!doc) return sendJson(res, 404, { error: "Not found" });
      if (doc.status === "complete") {
        return sendJson(res, 400, { error: "Job already complete" });
      }
      // Refuse if another worker holds an unexpired lease
      if (doc.worker_id && doc.lease_until && new Date(doc.lease_until).getTime() > Date.now()) {
        return sendJson(res, 409, {
          error: "Job is already running on another worker",
          worker_id: doc.worker_id,
          lease_until: doc.lease_until,
        });
      }
      runCoherentJob(docId, (e) => emit(docId, e)).catch((err) =>
        console.error(`Resume ${docId} failed:`, err)
      );
      return sendJson(res, 200, { success: true });
    }

    const idMatch = url.match(/^\/longform\/coherent\/([^/]+)$/);
    if (idMatch && method === "GET") {
      const docId = idMatch[1];
      const doc = await readDocument(docId);
      if (!doc) return sendJson(res, 404, { error: "Not found" });
      const sections = await readSections(docId);
      const totalWords = sections.reduce((sum, s) => sum + (s.word_count || 0), 0);
      return sendJson(res, 200, {
        document: doc,
        sections,
        total_words: totalWords,
      });
    }

    if (idMatch && method === "DELETE") {
      await deleteDocument(idMatch[1]);
      return sendJson(res, 200, { success: true });
    }

    // Existing endpoints
    if (url === "/longform/essay" && method === "POST") {
      const data = await readJsonBody(req);
      const { philosopher, topic } = data;
      const handler = longFormHandlers[philosopher?.toLowerCase()];
      const essay = handler
        ? await handler(topic)
        : await generateLongFormEssay(philosopher || "Philosopher", topic);
      return sendJson(res, 200, { success: true, essay, wordCount: essay.split(/\s+/).length });
    }

    if (url === "/longform/document" && method === "POST") {
      const data = await readJsonBody(req);
      const { philosopher, fullText, task } = data;
      const result = await processDocumentTask({ philosopher, fullText, task });
      return sendJson(res, 200, { success: true, result, wordCount: result.split(/\s+/).length });
    }

    if (url === "/health" && method === "GET") {
      return sendJson(res, 200, { status: "ok", service: "longform" });
    }

    sendJson(res, 404, { error: "Not found" });
  } catch (error) {
    console.error("Error:", error);
    sendJson(res, 500, { error: String(error) });
  }
}

const server = http.createServer(handleRequest);

ensureSchema()
  .then(() => console.log("✓ Long-form schema ensured"))
  .catch((e) => console.error("Schema bootstrap failed:", e));

server.listen(PORT, () => {
  console.log(`Long-form service running on port ${PORT}`);
  console.log(`Endpoints:`);
  console.log(`  POST   /longform/essay`);
  console.log(`  POST   /longform/document`);
  console.log(`  POST   /longform/coherent/start`);
  console.log(`  GET    /longform/coherent/:id`);
  console.log(`  GET    /longform/coherent/:id/stream  (SSE)`);
  console.log(`  POST   /longform/coherent/:id/resume`);
  console.log(`  DELETE /longform/coherent/:id`);
  console.log(`  GET    /longform/coherent/list?thinker=...`);
  console.log(`  GET    /health`);
  console.log(`Supported philosophers: ${Object.keys(longFormHandlers).join(", ")}`);
});
