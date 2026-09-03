# v3 Scoring Model — 100 points

## Domain-age bands

Measured from creation date to SERP observation date:

- `STRONG_FRESH`: <=6 months.
- `FRESH`: >6 and <=12 months.
- `WEAK_FRESH`: >12 and <=18 months.
- `OLD`: >18 months.

## 1. Young-domain SERP proof — 25

Score the strongest **cluster-level** credible pattern:

- 25: 2+ STRONG_FRESH domains rank across the core cluster, with at least one Top 5.
- 23: 1 STRONG_FRESH domain Top 5 on >=2 material core permutations.
- 21: 1 STRONG_FRESH domain Top 5 on one core query and neighboring SERPs are fragmented.
- 19: 1 STRONG_FRESH domain positions 6–10 with weak/fragmented SERP.
- 17: 2+ FRESH domains Top 10, at least one Top 5.
- 15: 1 FRESH domain Top 5.
- 11: 1 FRESH domain positions 6–10.
- 5: only WEAK_FRESH evidence.
- 2: fresh product/page but old/unconfirmed domain.
- 0: no <=18-month proof.

Do not award fresh-site points for >18-month domains.

## 2. SERP weakness — 12

- 11–12: fragmented, weak niche microsites, poor tools, few dominant brands.
- 8–10: mixed SERP, several beatable incumbents.
- 4–7: multiple strong incumbents.
- 0–3: locked by official/giant/high-authority domains.

Evaluate across >=3 core permutations for serious candidates.

## 3. Demand & attributable traffic proof — 18

Use **target-cluster evidence**, not headline domain traffic.

- 18: BREAKOUT — >=100K attributable monthly target-cluster search/organic traffic, or equivalent multi-region proof; attribution consistent.
- 17: BREAKOUT — 50K–100K attributable target-cluster traffic.
- 16: BREAKOUT — 10K–50K attributable target-cluster traffic with >=3 material core keywords/pages.
- 13–15: STRONG — 3K–10K attributable target traffic or several large core queries with strong ranking evidence.
- 10–12: MODERATE — 1K–3K attributable traffic plus multi-keyword proof.
- 7–9: credible cluster volume but weak traffic attribution.
- 4–6: one meaningful query, incomplete cluster data.
- 1–3: indirect/weak demand signals only.
- 0: no demand evidence.

If `TRAFFIC_ESTIMATE_CONFLICT` is unresolved, maximum for this dimension is 9 unless the conflict is irrelevant to the target-cluster evidence.

## 4. Keyword/page cluster depth — 12

Score distinct useful intents, not permutations alone.

- 11–12: 20+ useful page intents.
- 9–10: 12–19 intents.
- 6–8: 7–11 intents.
- 0–5: shallow or doorway-dependent.

Word-order variants normally map to the same page; they increase demand evidence, not page count.

## 5. Product feasibility — 12

- 11–12: client-side or deterministic public URL/API.
- 9–10: light stateless backend.
- 6–8: parser/proxy required but manageable.
- 3–5: recurring reverse engineering/remuxing.
- 0–2: technically fragile/access-control dependent.

## 6. Maintenance burden — 8

- 8: near-zero churn.
- 6–7: occasional fixes.
- 4–5: recurring parser/API changes.
- 1–3: frequent signature/anti-bot breakage.
- 0: operationally impractical.

## 7. Monetization — 5

Consider ad RPM, global traffic scale, repeat use, commercial audience, affiliate/API upside.

## 8. Platform growth/timing — 4

Reward growing platforms, fresh user behavior, recent asset formats, and emerging SERP windows.

## 9. Legal/policy durability — 4

- 4: public/user-owned assets, low controversy.
- 3: ordinary platform-content risk.
- 1–2: substantial ToS/DMCA fragility.
- 0: core product depends on private/DRM/paywall/access-control bypass => hard reject.

# Decision gates

## TEST NOW age gate

A total score is insufficient.

TEST NOW requires one:

1. >=1 STRONG_FRESH <=6-month domain currently Top 10; or
2. FRESH 6–12 month proof with >=1 Top 5, or >=2 Top 10 plus weak/fragmented SERP.

WEAK_FRESH 12–18 month evidence can only support WATCH.

## PROVEN BREAKOUT gate

`PROVEN BREAKOUT` is an upgrade label on TEST NOW, not a separate score range.

Requires all:

- base score >=78 and TEST NOW age gate passed;
- demand grade = BREAKOUT;
- >=10K attributable target-cluster monthly search/organic traffic or equivalent strong multi-region proof;
- target-cluster evidence spans >=3 material core keywords OR >=2 top pages;
- attribution confidence medium/high;
- no unresolved TRAFFIC_ESTIMATE_CONFLICT;
- no policy hard reject.

# Hard caps

- No <=18-month domain in current Top 10 => max 59.
- Best evidence only WEAK_FRESH 12–18 months => max 77, WATCH ceiling.
- FRESH 6–12 month evidence that does not satisfy age gate => WATCH ceiling.
- Shallow single-page niche => max 64.
- High reverse-engineering churn => max 64 unless unusually strong, well-attributed demand proof justifies WATCH for further spike testing.
- Unresolved traffic conflict that is central to the opportunity thesis => cannot receive PROVEN BREAKOUT.
- DRM/paywall/private/access-control circumvention => REJECT.
- `POLICY_SHOCK` where the only viable product path is explicitly prohibited => REJECT.

# Decision bands

- `TEST NOW`: 78–100 + age gate + confidence >= medium + no hard reject.
- `WATCH`: 65–77, weak/incomplete age evidence, unresolved important traffic conflict, or technical/policy uncertainty requiring a spike.
- `REJECT`: <65 or hard reject.
