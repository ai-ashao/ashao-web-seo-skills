# Example — Photo Cleaner (Android)

This example demonstrates why intent expansion and promotion filtering matter.

## Weak first-pass queries

- `android photo cleaner privacy local on-device`
- `android similar photos cleaner`
- `android accidentally deleted photos`

Several broad combinations produced irrelevant results.

## Better intent-driven queries

- `site:reddit.com/r/androidapps screenshot cleanup app`
- `site:reddit.com/r/androidapps gallery cleaner undo delete`
- `site:reddit.com/r/androidapps WhatsApp images clean gallery`
- `site:reddit.com/r/androidapps photos "on device" cleaner`
- `site:reddit.com/r/androidapps "photo cleaner" subscription`

## Pain Graph observed during testing

- Safe deletion
  - fear of accidental deletion
  - review queue
  - confirmation / trash / recovery
- Fast review
  - swipe delete / keep
  - fewer navigation steps
- Junk classification
  - screenshots
  - WhatsApp forwards
  - ads / random downloads
  - blurry images
- Large libraries
  - thousands / 10k+ images
  - impossible to inspect one by one
- Pricing friction
  - core feature behind subscription
  - dislike of monthly payment for simple cleanup
- Privacy / permissions
  - concern about internet access and permissions
  - preference for on-device processing
- Batch management
  - date ranges
  - month/year grouping
  - multi-select
- Duplicate / similar photos
  - evidence existed but was weaker than the clusters above in the Android Reddit sample

## Critical v0.1 learning

Developer self-promotion was common. A developer saying their app solves blurry photos is **not** evidence that users broadly demand blurry-photo detection.

The safest workflow observed in user discussion was:

`Swipe/mark -> Review queue -> Confirm -> System trash/recoverable state`

This is stronger than immediate destructive deletion because the corpus contained explicit fear and reports of accidental loss.
