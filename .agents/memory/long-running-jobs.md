---
name: Long-running jobs in this repl
description: How to run multi-minute Playwright recordings and ffmpeg encodes reliably.
---

Long jobs (Playwright screen recordings, ffmpeg encode/concat of large webms) routinely exceed the 2-minute bash timeout, and detached/background processes started from bash are SUSPENDED (no CPU progress) between tool calls.

**How to apply:** run such jobs as a supervised console workflow (no port) via configureWorkflow/getWorkflowStatus/removeWorkflow in code_execution. Poll getWorkflowStatus until state is `finished`, then removeWorkflow. The demo recorder/encoder live under `video_build/demo/` (driver.mjs records segment webms + per-segment `<name>.cuts.json`; encode.mjs applies ffmpeg `select=not(between...)` cuts, scales 1280x720@30, numerically concats to `exports/`).

**Why:** prior attempts that ran recordings via detached bash never progressed and silently produced empty/partial output.
