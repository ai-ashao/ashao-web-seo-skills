# Codex Skillforge — 精简版

这个仓库只保留**真正需要固定流程、证据契约或确定性脚本**的 Skill。目标不是让 Skill 越多越好，而是让 AI 在关键决策上少犯重复错误，同时保留正常推理空间。

## 活跃 Skill（6 个）

| Skill | 只回答什么 | 什么时候用 |
|---|---|---|
| `site-opportunity-scorecard` | **WHERE**：独立站、专区、单页还是不做？ | 架构尚未决定 |
| `serp-siege` | **WHAT**：哪些 Page Families / SEO MVP 页面先做？ | 方向已经决定 |
| `reference-website-builder` | **HOW**：参考页怎么分析、做原型、迁入真实项目？ | UI/交互/参考站任务 |
| `technical-seo-audit` | **CRAWL**：搜索引擎能否正确发现、抓取、索引？ | 上线/迁移/技术 SEO 审计 |
| `helpful-value-audit` | **VALUE**：页面是否真的解决用户任务？ | 工具页质量/竞品页差距 |
| `web-asset-pipeline` | **ASSETS**：视觉素材如何安全、轻量、可追踪地上线？ | 需要处理生产素材时 |

## 已合并/移除的 Skill

- `downloader-opportunity-radar` → 变成 `site-opportunity-scorecard` 的 `downloader` profile。
- `competitive-ui-reverse-engineering` → 合并进 `reference-website-builder` 的 `analyze` mode。
- `adapt-reference-site` → 合并进 `reference-website-builder` 的 `adapt` mode。
- `website-audit-scorecard` → 移除；综合判断由 AI 基于 specialist audits 完成，不再制造额外总分。
- `ai-citation-research` → 移出核心 Skill 集；需要时作为普通研究任务执行，避免过早流程化。

## 推荐工作流

```text
Idea / competitor
       ↓
site-opportunity-scorecard
WHERE should it live?
       ↓
serp-siege
WHAT should we build?
       ↓
reference-website-builder
HOW should important pages work?
       ↓
technical-seo-audit
Can search engines crawl/index it?
       ↓
helpful-value-audit
Does the page genuinely satisfy the task?
       ↓
Launch / iterate from GSC and product data
```

`web-asset-pipeline` 在任何需要生产素材的阶段按需调用。

## 新建 Skill 的门槛

新 Skill 至少应满足下面三条中的两条：

1. 不用 Skill 时，AI 会反复犯同一种高影响错误；
2. 存在值得固定的 deterministic script / validator / evidence contract；
3. 它是一个真正独立的决策阶段，而不是现有 Skill 的行业 profile/reference。

如果只满足一条，优先写成现有 Skill 的 reference/profile，或者直接让 AI 正常推理。

## 验证

```bash
python3 -B -m unittest discover -s skills/site-opportunity-scorecard/tests -v
python3 -B -m unittest discover -s skills/serp-siege/tests -v
python3 -B skills/reference-website-builder/scripts/validate_skill.py skills/reference-website-builder
python3 -B -m unittest discover -s skills/helpful-value-audit/tests -v
python3 -B -m unittest discover -s skills/technical-seo-audit/tests -v
python3 -B -m unittest discover -s skills/web-asset-pipeline/tests -v
```
