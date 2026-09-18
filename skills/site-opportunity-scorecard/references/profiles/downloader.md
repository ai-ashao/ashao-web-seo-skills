# Downloader Decision Profile

Use this profile inside `site-opportunity-scorecard` for downloader/save/export/extractor utilities. It preserves the genuinely niche-specific evidence rules without keeping a separate downloader Skill.

## 1. Build the core intent universe before sizing demand

Do not size a downloader niche from one head term.

For a platform and plausible asset, inspect natural variants such as:

- `{platform} downloader`
- `{platform} download`
- `download {platform}`
- `{platform} {asset} downloader`
- `{platform} {asset} download`
- `download {platform} {asset}`

Add real synonyms only when evidence supports them. Keep secondary modifiers such as `free`, `online`, `HD`, `no watermark`, device names, and browser names out of core demand unless they have distinct SERPs or material volume.

## 2. Attribute traffic to the downloader cluster

Keep these separate:

- total domain visits;
- search share;
- organic traffic estimate;
- target-cluster page/keyword traffic.

A domain with high total visits does not prove a large downloader niche. Prefer Top Pages and Organic Keywords that can be tied directly to the target downloader cluster.

Flag conflicting traffic estimates rather than averaging them into false precision.

## 3. Young-domain proof is useful, but missing age evidence is not negative evidence

Age bands may be used as supporting evidence:

- `STRONG_FRESH`: <=6 months
- `FRESH`: >6 and <=12 months
- `WEAK_FRESH`: >12 and <=18 months
- `OLD`: >18 months
- `MISSING`: creation/launch evidence unavailable

`OLD` is negative fresh-site evidence. `MISSING` only lowers confidence and requires validation; it must not be treated as `OLD`.

Prefer RDAP/WHOIS/registrar creation data, then reliable launch/history evidence. A new page on an old domain is not young-domain proof.

## 4. Validate cluster-level rankability

For serious candidates, inspect more than one query. Prefer:

- head query;
- strongest alternate action/word-order query;
- strongest asset-specific query.

One young domain on one query is weak evidence. Repeated appearance across the core intent family is stronger evidence.

## 5. Check implementation durability

Assess:

- public URL/CDN accessibility;
- API dependence;
- anti-bot/signature churn;
- proxy/backend requirement;
- remux/transcoding needs;
- bandwidth/storage cost;
- support burden;
- platform breakage risk.

If extraction stability is uncertain, recommend a bounded extractor spike before a full build.

## 6. Apply policy durability as a product gate

Do not recommend products that fundamentally depend on unauthorized access, credential/token extraction, DRM/access-control circumvention, paywall bypass, or private/authenticated content acquisition without authorization.

A platform restriction that increases search demand may simultaneously reduce product durability. Treat both effects explicitly.

## 7. Handoff

Do not design the final 10–30 page cluster here.

If the architecture decision is to proceed, pass the normalized downloader intent evidence, Top Pages/keyword exports, platform constraints, and validated exclusions to `serp-siege`, which owns Page Families and the SEO MVP First Batch.
