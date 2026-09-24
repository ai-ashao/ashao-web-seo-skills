---
name: reddit-subreddit-scan
description: Perform a bounded, chronological, read-only scan of one public subreddit over a defined time window using Reddit listing JSON and optional thread JSON. Use when the user needs recent feed coverage from a known subreddit, such as a weekly opportunity scan, entity watch, or unresolved-question sweep. Do not use for broad cross-Reddit pain research, posting, voting, messaging, account automation, or high-frequency monitoring.
---

# Reddit Subreddit Scan

Version: 0.1

## Purpose

Collect a recent, time-bounded corpus from **one known public subreddit** in chronological order.

This skill is for questions such as:

- What appeared in r/identifythisfont during the last 7 days?
- Which recent posts mention entities in my catalog?
- Which unresolved questions are worth reviewing manually?
- Which identified entities are missing from my catalog?
- Give me a weekly subreddit opportunity scan without setting up a crawler.

Use `pain-mining` instead when the task is broad discovery across Reddit or multiple communities.

## Core rules

1. **Chronological feed, not search.** Start from the subreddit's `new` listing and paginate backward.
2. **Bounded window.** Stop when the oldest fetched post crosses the requested cutoff.
3. **Coverage must be explicit.** Report pages fetched, posts seen, oldest timestamp, and whether the time boundary was reached.
4. **Read-only only.** Never post, comment, vote, message, follow, or log in through this skill.
5. **Minimize requests.** Fetch thread comments only when they are needed for the user's task.
6. **No rate-limit evasion.** On 403/429/challenge responses, stop or back off; do not rotate identities, proxies, cookies, or endpoints to bypass controls.
7. **No account cookies.** Public scans should not use a user's Reddit login session.
8. **Do not overclaim completeness.** If pagination fails before the cutoff, label the corpus `PARTIAL`.
9. **Exact match and inference are different.** A catalog/entity string match is evidence; a visual or semantic identification is a separate model judgment and must be labeled.
10. **This is not search-demand validation.** Reddit occurrence does not equal keyword volume, SERP opportunity, or commercial demand.

## Inputs

Required:

- `subreddit`: subreddit name without `r/`.

Optional:

- `time_window`: default `7d`.
- `cutoff_utc`: explicit timestamp; overrides `time_window`.
- `max_pages`: safety cap, default 10 listing pages.
- `include_comments`: `none`, `candidates`, or `all_nonzero`; default `candidates`.
- `candidate_rule`: what makes a post worth deeper inspection.
- `entity_catalog`: optional list of names/slugs to exact-match against post/comment text.
- `status_filter`: optional flair/status filter.
- `output_goal`: e.g. `opportunity_scan`, `gap_scan`, `unresolved_scan`, `corpus_only`.

If the user gives only a subreddit and a period, proceed with a feed scan and summarize the corpus.

## Data acquisition

### 1. Fetch the listing

Use the public chronological listing:

```text
https://www.reddit.com/r/{subreddit}/new.json?limit=100&raw_json=1
```

Read:

- `data.children[].data`
- `data.after`

Useful post fields:

- `id`
- `name`
- `title`
- `selftext`
- `author`
- `created_utc`
- `link_flair_text`
- `num_comments`
- `score`
- `permalink`
- `url`
- `url_overridden_by_dest`
- `is_gallery`
- `gallery_data`
- `media_metadata`
- `preview`

Do not treat score/upvotes as proof of demand.

### 2. Paginate with `after`

For the next page:

```text
https://www.reddit.com/r/{subreddit}/new.json?limit=100&raw_json=1&after={data.after}
```

Continue until one of these stop conditions is met:

- the oldest fetched `created_utc` is older than the cutoff;
- `data.after` is null;
- `max_pages` is reached;
- access is blocked or rate-limited.

Deduplicate by Reddit post `id`.

### 3. Apply the cutoff

Keep posts whose `created_utc >= cutoff_utc`.

Record the first post older than the cutoff as boundary evidence when available.

### 4. Fetch comments only when needed

Thread JSON:

```text
https://www.reddit.com/comments/{post_id}.json?limit=100&raw_json=1
```

Default behavior is `include_comments=candidates`.

Fetch comments when they materially help with:

- extracting an identified answer;
- checking whether an open question is actually resolved in comments;
- matching a supplied entity catalog;
- verifying a workaround/source link;
- measuring response timing.

Do not fetch every thread by default just because comments exist.

### 5. Handle failures conservatively

If Reddit returns a block, challenge, 403, or 429:

- do not bypass it;
- record the affected page/thread;
- stop aggressive retries;
- continue only through an allowed browser/search path if the task still makes sense;
- downgrade coverage to `PARTIAL`.

For production, high-frequency, authenticated, or commercial-scale collection, use Reddit's current approved API/access method rather than treating public `.json` endpoints as a guaranteed long-term interface.

## Candidate filtering

The skill may run a cheap first pass before fetching comments.

Examples:

### Entity watch

When `entity_catalog` is supplied:

1. normalize case and whitespace;
2. exact-match full entity names in title/selftext;
3. keep aliases only if the user supplied them;
4. do not count substring collisions such as `Inter` inside `interesting`;
5. report fuzzy/visual candidates separately.

### Unresolved-question scan

Prefer posts that are:

- in an open/unresolved flair;
- recent enough to still be useful;
- low-comment or unanswered;
- relevant to the user's catalog/topic.

Do not equate `0 comments` with a good opportunity; the sample may be poor or irrelevant.

### Gap scan

For posts explicitly marked resolved/identified:

1. fetch comments only when needed;
2. extract the identified entity from source text;
3. compare with the supplied catalog;
4. classify:
   - `IN_CATALOG`
   - `CATALOG_GAP`
   - `AMBIGUOUS`
5. preserve the source thread URL.

## Output contract

Always begin with coverage:

```yaml
coverage:
  subreddit: identifythisfont
  requested_window: 7d
  listing_pages_fetched: 4
  posts_seen: 327
  posts_in_window: 301
  oldest_seen_utc: ...
  cutoff_utc: ...
  boundary_reached: true
  coverage_status: COMPLETE | PARTIAL
  partial_reason: null
```

Then return only sections relevant to the user's goal.

For an opportunity scan:

```yaml
reply_candidates:
  - post_id: ...
    title: ...
    status: ...
    permalink: ...
    evidence_type: EXACT_TEXT_MATCH | VISUAL_REVIEW
    matched_entity: ...
    comments: 0
    confidence: HIGH | MEDIUM | LOW
    note: ...

catalog_gaps:
  - entity: ...
    supporting_threads: 2
    source_urls:
      - ...
    note: ...
```

For corpus-only work, return a compact table or JSON-like structure instead.

## FontOdyssey weekly pattern

For a weekly `r/identifythisfont` run:

1. Scan `new.json` backward until 7 days are covered.
2. Compare post text against the current FontOdyssey catalog.
3. Fetch comments for `Identified*` posts to extract possible catalog gaps.
4. Prioritize still-open posts for manual visual review.
5. Separate:
   - `reply_candidates`: FontOdyssey already has the exact font and the thread is still meaningfully open;
   - `catalog_gaps`: identified fonts absent from FontOdyssey;
   - `reference_page_candidates`: gaps that may justify a non-download reference page, subject to downstream SERP/search-demand validation.
6. Never auto-post a Reddit reply.

## Relationship to other Skills

Use this skill for:

> **WHAT appeared recently in this one subreddit?**

Use `pain-mining` for:

> **WHAT recurring user pains exist across Reddit/public discussions?**

Use `serp-siege` only after a candidate page or entity has separate SEO evidence.

## Final boundary

This skill produces a **bounded recent subreddit corpus and opportunity shortlist**.

It does not:

- post to Reddit;
- automate a Reddit account;
- infer keyword volume;
- decide that a page should be built from one Reddit mention;
- guarantee complete historical coverage;
- bypass Reddit access controls.
