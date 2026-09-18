# helpful-value-audit v2

Page-level quality audit for tool/utility pages.

It answers **whether the page genuinely satisfies the query and what page-level gap remains**. It no longer outputs market-entry verdicts such as ATTACK/SKIP and no longer assigns pseudo-precise ranking-moat scores.

```bash
python3 scripts/calculate_score.py audit.json
python3 -B -m unittest discover -s tests -v
```
