# site-opportunity-scorecard v2

Decides one thing: **where an opportunity should live**.

Outputs exactly one architecture: independent site, existing-site section, existing-site page, or observe/reject.

## Profiles

- `seo_first_utility`
- `product_led`
- `content_site`
- `downloader`
- `generic`

Niche-specific rules belong in profiles, not new Skills. The downloader profile lives at `references/profiles/downloader.md`.

After the architecture decision, hand the evidence to `$serp-siege` for Page Families, SEO Page Map, and First Batch.

```bash
python3 scripts/calculate_score.py assets/assessment-input-template.json --pretty
python3 scripts/validate_report.py --lang auto report.md
python3 -B -m unittest discover -s tests -v
```
