# Reddit Subreddit Scan Skill v0.1

A lightweight, read-only Skill for scanning one public subreddit chronologically over a bounded time window.

## Typical prompts

- `Scan r/identifythisfont for the last 7 days and show unresolved posts that match my font catalog.`
- `Run a weekly gap scan on r/identifythisfont and list identified fonts missing from FontOdyssey.`
- `Scan r/webdev/new for the last 3 days and return only posts matching this entity list.`
- `Collect the last 24 hours of r/SomeSubreddit as a bounded corpus; do not search Reddit globally.`

## Method

The Skill uses Reddit's public chronological JSON listing:

```text
/r/{subreddit}/new.json?limit=100
```

and paginates with `data.after` until the requested cutoff is crossed.

Thread JSON is fetched only when comments are needed:

```text
/comments/{post_id}.json?limit=100
```

## Why this is separate from pain-mining

`pain-mining` is search-led and cross-thread: it asks what recurring pain exists.

`reddit-subreddit-scan` is feed-led and bounded: it asks what appeared recently in one known subreddit.

## Safety / access boundary

- public, read-only collection only;
- no login cookies;
- no posting/voting/messaging;
- no rate-limit or access-control bypass;
- stop/back off on 403/429/challenges;
- label coverage partial if pagination fails;
- use Reddit's current approved API/access method for high-frequency, authenticated, or production-scale collection.

## FontOdyssey example

A weekly scan of `r/identifythisfont` can produce two small outputs:

1. current open threads where an existing FontOdyssey font is a credible match;
2. newly identified fonts missing from the catalog, for later license/SEO/reference-page validation.

It never auto-replies on Reddit.
