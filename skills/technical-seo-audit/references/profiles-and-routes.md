# Profiles and Route Policy

| Route class | Toolsite | SaaS | Hybrid | Typical paths |
| --- | --- | --- | --- | --- |
| `PUBLIC_TOOL` | INDEX | INDEX | INDEX | `/tools/*`, converters, downloaders, generators |
| `MARKETING` | INDEX | INDEX | INDEX | `/pricing`, `/features/*`, `/product/*` |
| `SEO_LANDING` | INDEX | INDEX | INDEX | `/solutions/*`, `/use-cases/*`, `/compare/*` |
| `CONTENT` | INDEX | INDEX | INDEX | `/guides/*`, `/blog/*`, `/resources/*` |
| `INTEGRATION` | INDEX | INDEX | INDEX | `/integrations/*` |
| `DOCS` | INDEX by default | INDEX by default | INDEX by default | `/docs/*` |
| `AUTH` | REVIEW | REVIEW | REVIEW | `/login`, `/signup`, reset-password |
| `APP` | EXCLUDE | EXCLUDE | EXCLUDE | `/dashboard/*`, `/app/*`, `/workspace/*` |
| `ACCOUNT` | EXCLUDE | EXCLUDE | EXCLUDE | `/settings`, `/billing`, `/account` |
| `TRANSACTIONAL` | EXCLUDE | EXCLUDE | EXCLUDE | `/checkout`, `/success`, `/payment` |
| `SYSTEM` | EXCLUDE | EXCLUDE | EXCLUDE | `/api/*`, callbacks, webhooks |
| `UNKNOWN` | UNASSESSED | UNASSESSED | UNASSESSED | anything ambiguous |

`generic` keeps `UNKNOWN` unassessed and uses only obvious public/private route classes. `auto` detects a site-level default from observed route evidence, then reclassifies checked URLs. Automatic classification must remain visible and overridable.
