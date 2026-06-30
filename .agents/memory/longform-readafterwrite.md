---
name: Longform document read-after-write null
description: coherentLongForm worker crash when readDocument returns null after saveSkeleton.
---

In the longform coherence worker, reading the document immediately after persisting the skeleton can transiently return null (read-after-write / lease/status transition race). A non-null assertion on that read crashes the whole job ("Cannot read properties of null (reading 'state')") and the UI then shows 0 generated chars.

**How to apply:** never assert non-null on a post-write re-read in the worker; fall back to the already-loaded in-memory doc and `emptyState()`. Resume correctness is still preserved because state is reconstructed from persisted section rows afterward.

**Why:** this single null-deref was the root cause of the longform/dialogue feature producing empty output despite the API otherwise working.
