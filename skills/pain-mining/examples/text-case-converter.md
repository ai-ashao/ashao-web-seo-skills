# Example — Text Case Converter (Negative Control)

This example exists to prevent Pain Mining from overfitting toward finding pain everywhere.

## Search behavior

Relevant results can be easy to find:

- uppercase/lowercase conversion
- sentence/title case
- shortcuts in Word/editors
- developer-built case-converter tools

But relevance is not the same as user pain.

## Observed evidence shape

**SPARSE**

Why:

- many tasks are already solved by built-in shortcuts
- developer promotions are common
- most user questions are one-off how-to requests
- recurring multi-thread pain clusters were not found in the benchmark sample

## Weak branches

Potential narrow edge cases:

- title-case exceptions
- sentence/title case not supported by a particular editor
- bulk replacement of specific words with changed case

These are useful hypotheses, but they did not justify a broad Pain Graph.

## Key lesson

If query yield is good but pain density is low:

1. do not keep searching merely to find pain;
2. do not invent subscription/privacy/batch problems;
3. classify the corpus SPARSE;
4. hand any plausible SEO intent to downstream keyword/SERP validation if the user still wants to evaluate it.

Pain Mining is allowed to conclude that a tool is simply low-friction.
