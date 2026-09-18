# Tool-site Action Classification

Use only when `mode=tool_site`.

## FEATURE

Use when the finding changes how the existing tool behaves.

Examples:

- preserve EXIF
- batch processing
- target file-size control
- detect full-resolution images behind thumbnails
- extrusion depth slider

A feature can be DIRECT or INFERRED.

## PAGE_CANDIDATE

Use when the evidence reveals a **distinct job, input/output pair, destination, or constraint** that users describe independently from the core task.

Examples:

- PNG to STL
- logo to STL
- QR code for PDF
- download all images from website
- compress image for upload

Required fields:

- candidate query wording
- user evidence supporting the job
- why the job is distinct
- `seo_validation_status: REQUIRED`

Do not treat Reddit recurrence as keyword-volume proof.

## HOMEPAGE_COPY

Use when the evidence is primarily about trust, simplicity, positioning, or a promise that strengthens the core page.

Examples:

- local processing
- no upload
- no signup
- static QR does not depend on a hosted redirect
- no CLI required

Do not make absolute claims stronger than the evidence/product implementation supports.

## FAQ_GUIDE

Use for conceptual confusion, edge cases, limitations, and workflows.

Examples:

- static vs dynamic QR
- why lossy compression cannot be literally lossless
- Markdown reference.docx behavior
- logo extrusion vs depth-map photo-to-STL

## Tie-break rule

When a finding could map to multiple actions, choose the **primary user outcome**:

- changes the tool → FEATURE
- distinct searchable job → PAGE_CANDIDATE
- trust/positioning → HOMEPAGE_COPY
- explanation/workflow → FAQ_GUIDE

Secondary actions may be noted, but do not duplicate every finding into every bucket.
