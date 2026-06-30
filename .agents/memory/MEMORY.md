# Memory Index

- [Long recordings need workflows](long-running-jobs.md) — detached/background bash processes FREEZE between calls; bash caps at 2min. Run long Playwright/ffmpeg jobs as console workflows.
- [Longform read-after-write null](longform-readafterwrite.md) — readDocument() can transiently return null right after saveSkeleton(); always fall back to the in-memory doc.
