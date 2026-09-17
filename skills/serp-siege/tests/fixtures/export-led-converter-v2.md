# SERP Siege — export-led converter V2 fixture

## Execution Frame
- **Selected direction:** build a markdown converter suite
- **Primary job:** convert markdown into common output formats
- **Target scope:** export-proven converter pages
- **Destination:** `NOT_SUPPLIED`
- **Destination Basis:** `MISSING`: no destination supplied
- **Planning Confidence:** `HIGH`

### Assumptions
| Assumption | Basis | Execution Impact | Confidence | Validation |
|---|---|---|---|---|
| supplied exports match US/en | `USER_SUPPLIED_THIRD_PARTY`: Ahrefs exports | supports relative prioritization | `HIGH` | preserve provider/date |

## Search Landscape Summary
- **Primary job:** markdown conversion
- **Primary keyword cluster:** markdown converters
- **SERP structure:** not exhaustively refreshed
- **Competitor pattern:** multiple dedicated conversion pages
- **Execution-relevant coverage gaps:** not required for demand admission
- **Major unknowns:** live SERP weakness for supporting pages
- **Research coverage:** two supplied competitor exports

## Evidence Dataset
| Dataset | Source | Scope | Market | Data Date | Metric Semantics | Evidence |
|---|---|---|---|---|---|---|
| a-top-pages.csv | Ahrefs | competitor Top Pages | US/en | 2026-09-16 | third-party traffic estimate | `USER_SUPPLIED_THIRD_PARTY`: supplied export A |
| b-keywords.csv | Ahrefs | competitor Organic Keywords | US/en | 2026-09-16 | position/volume estimates | `USER_SUPPLIED_THIRD_PARTY`: supplied export B |

## Competitor Map
| Competitor | Positioning | Main Tool | Coverage | Strength | Weakness | Evidence |
|---|---|---|---|---|---|---|
| A | converter suite | md to pdf | broad | repeated pages | unknown UX | `USER_SUPPLIED_THIRD_PARTY`: a-top-pages.csv |
| B | document tools | md to docx | broad | repeated queries | unknown UX | `USER_SUPPLIED_THIRD_PARTY`: b-keywords.csv |

## Keyword Cluster Map
| Cluster | Type | Primary Keyword | Intent | Supporting Queries | Page Decision | Priority | Evidence |
|---|---|---|---|---|---|---|---|
| md-pdf | `FORMAT` | markdown to pdf | convert | md to pdf | `NEW_TOOL_PAGE` | `P0` | `USER_SUPPLIED_THIRD_PARTY`: A+B exports |
| md-docx | `FORMAT` | markdown to word | convert | md to docx | `NEW_TOOL_PAGE` | `P0` | `USER_SUPPLIED_THIRD_PARTY`: A+B exports |

## Demand Evidence Map
| Cluster | Demand Proof | Sources | Metric Context | Strength | Evidence |
|---|---|---|---|---|---|
| md-pdf | repeated Top Pages and keywords | A; B | same provider/market/date | `STRONG` | `USER_SUPPLIED_THIRD_PARTY`: A+B rows |
| md-docx | repeated Top Pages and keywords | A; B | same provider/market/date | `STRONG` | `USER_SUPPLIED_THIRD_PARTY`: A+B rows |

## Feature Coverage Map
| Feature | Competitor A | Competitor B | Competitor C | Competitor D | Competitor E | Candidate | Priority | Evidence |
|---|---|---|---|---|---|---|---|---|
| PDF export | `YES` | `YES` | `MISSING` | `NO` | `PARTIAL` | `PLANNED` | `P0` | `USER_SUPPLIED_THIRD_PARTY`: supplied competitor evidence |

## SERP Coverage Map
| Cluster | Primary Keyword | Intent | Evidence | SERP Strength | Gap | Reuse Potential | Proposed Page | Priority |
|---|---|---|---|---|---|---|---|---|
| md-pdf | markdown to pdf | tool | `MISSING` | `MISSING` | `MISSING` | `HIGH` | /markdown-to-pdf | `P0` |
| md-docx | markdown to word | tool | `MISSING` | `MISSING` | `MISSING` | `HIGH` | /markdown-to-word | `P0` |

## SEO Page Map
| Page Decision | Proposed URL | Canonical Parent | Target Cluster | Primary Keyword | Search Intent | Shared Core | Priority | Reason |
|---|---|---|---|---|---|---|---|---|
| `NEW_TOOL_PAGE` | /markdown-to-pdf | | md-pdf | markdown to pdf | tool | markdown parse/export core | `P0` | strongest export-proven task |
| `NEW_TOOL_PAGE` | /markdown-to-word | | md-docx | markdown to word | tool | markdown parse/export core | `P0` | repeated export proof |

## Page Family Map
| Family | Type | URL Pattern | Bound Clusters | Representative Instances | Initial Instances | Shared Core | Priority | Evidence |
|---|---|---|---|---|---|---|---|---|
| markdown-converter | `TEMPLATE` | /markdown-to-{format} | md-pdf; md-docx | pdf; word | 2 | markdown parse/export core | `P0` | `USER_SUPPLIED_THIRD_PARTY`: export-proven formats |

## First Batch
| Item or URL | Group | Target Cluster | Why Now | Shared Capability | SEO Role |
|---|---|---|---|---|---|
| /markdown-to-pdf | `CORE` | md-pdf | strongest repeated proof | markdown parse/export core | core entry |
| /markdown-to-word | `SUPPORTING` | md-docx | repeated competitor proof | markdown parse/export core | supporting entry |
- **First Batch Deviation:** two-page fixture intentionally tests V2 strong-demand gating.

## Product Roadmap
### MVP / P0
| Item | Shared Core | Required Workflow | Reason |
|---|---|---|---|
| converter template | markdown parse/export core | paste/upload, convert, download | serves both export-proven P0 clusters |

### P1
| Item | Demand Evidence | Core Reuse | Reason |
|---|---|---|---|
| `NONE` | | | no extra fixture scope |

### P2
| Item | Uncertainty or Cost | Revisit Evidence |
|---|---|---|
| `NONE` | | |

## Do Not Build Yet
| Idea | Status | Reason to Hold or Reject | Revisit Trigger |
|---|---|---|---|
| markdown to obscure format | `HOLD` | no export proof | new competitor/query evidence |

## Execution Constraints & Missing Evidence
| Constraint or Unknown | Affected Scope | Recommended Adjustment | Evidence Type | Confidence | Prerequisite or Next Evidence |
|---|---|---|---|---|---|
| live SERP gap not refreshed | supporting pages | do not claim weak SERP | `MISSING` | `LOW` | optional SERP refresh before scale-up |

## Next Execution
- **First action:** implement the shared converter template.
- **Required evidence or prerequisite:** preserve export provenance.
- **Success condition:** both P0 pages complete the same conversion workflow.
- **If it fails:** narrow to the core export path.
- **First Batch re-evaluation trigger:** new export or first-party query evidence.
