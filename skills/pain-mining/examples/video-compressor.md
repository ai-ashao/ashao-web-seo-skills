# Example — Video Compressor (Android)

This example demonstrates the shape of a result, not a canonical market report.

## Intent expansion

- compress video
- video too large
- target file size
- quality loss
- offline / upload
- batch compression
- preserve metadata
- resolution control
- Discord / email / WhatsApp limits

## Observed useful clusters during v0.1 testing

- Target file size
- Quality preservation
- Simple UX vs FFmpeg/Termux complexity
- Batch compression
- On-device/privacy
- Metadata preservation
- Resolution control

## Important learning

A broad query such as a long Boolean tree produced noisy results. Short queries such as:

- `site:reddit.com "compress video" target file size`
- `site:reddit.com "video too large" Discord`
- `site:reddit.com "compress video" offline`

were more reliable.

## Product implication example

`Compress to 10MB / 25MB / 50MB`

Evidence level: DIRECT when users explicitly ask for a maximum target size; otherwise INFERRED.
