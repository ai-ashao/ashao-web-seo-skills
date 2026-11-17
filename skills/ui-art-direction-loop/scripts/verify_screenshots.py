#!/usr/bin/env python3
"""Check local screenshot evidence without a browser or third-party packages."""

import argparse
import hashlib
import json
import math
import struct
import sys
from pathlib import Path


def dimensions(data):
    if data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        return "png", *struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        pos = 2
        frames = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                  0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
        while pos < len(data):
            if data[pos] != 0xFF:
                raise ValueError("invalid JPEG marker")
            while pos < len(data) and data[pos] == 0xFF:
                pos += 1
            marker = data[pos]
            pos += 1
            if marker in {0xD9, 0xDA}:
                break
            if marker == 0x01 or 0xD0 <= marker <= 0xD8:
                continue
            length = int.from_bytes(data[pos:pos + 2], "big")
            if length < 2 or pos + length > len(data):
                raise ValueError("truncated JPEG segment")
            if marker in frames:
                height, width = struct.unpack(">HH", data[pos + 3:pos + 7])
                return "jpeg", width, height
            pos += length
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        pos = 12
        while pos + 8 <= len(data):
            tag = data[pos:pos + 4]
            size = int.from_bytes(data[pos + 4:pos + 8], "little")
            chunk = data[pos + 8:pos + 8 + size]
            if len(chunk) != size:
                raise ValueError("truncated WebP chunk")
            if tag == b"VP8X" and len(chunk) >= 10:
                return "webp", 1 + int.from_bytes(chunk[4:7], "little"), 1 + int.from_bytes(chunk[7:10], "little")
            if tag == b"VP8L" and len(chunk) >= 5 and chunk[0] == 0x2F:
                bits = int.from_bytes(chunk[1:5], "little")
                return "webp", (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
            if tag == b"VP8 " and len(chunk) >= 10 and chunk[3:6] == b"\x9d\x01\x2a":
                width, height = struct.unpack("<HH", chunk[6:10])
                return "webp", width & 0x3FFF, height & 0x3FFF
            pos += 8 + size + size % 2
    raise ValueError("unsupported or malformed PNG/JPEG/WebP")


def verify(manifest, tolerance):
    spec = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(spec, dict) or type(spec.get("schema_version")) is not int or spec["schema_version"] != 1:
        raise ValueError("schema_version must be 1")
    shots = spec.get("screenshots")
    if not isinstance(shots, list) or not shots:
        raise ValueError("screenshots must be a nonempty list")
    results, ids, hashes = [], set(), {}
    for shot in shots:
        row = {"scene_id": shot.get("scene_id") if isinstance(shot, dict) else None,
               "errors": [], "warnings": []}
        results.append(row)
        try:
            if not isinstance(shot, dict):
                raise ValueError("screenshot entry must be an object")
            scene_id = shot.get("scene_id")
            if not isinstance(scene_id, str) or not scene_id.strip():
                raise ValueError("scene_id must be a nonempty string")
            if scene_id in ids:
                row["errors"].append("duplicate scene_id")
            ids.add(scene_id)
            viewport = shot.get("viewport")
            if not isinstance(viewport, list) or len(viewport) != 2 or any(type(n) is not int or n <= 0 for n in viewport):
                raise ValueError("viewport must contain two positive integers")
            capture = shot.get("capture", "viewport")
            if capture not in {"viewport", "full-page"}:
                raise ValueError("capture must be viewport or full-page")
            file = shot.get("file")
            if not isinstance(file, str) or not file.strip() or "://" in file:
                raise ValueError("file must be a local path")
            path = (manifest.parent / file).resolve()
            data = path.read_bytes()
            kind, width, height = dimensions(data)
            if width <= 0 or height <= 0:
                raise ValueError("image dimensions must be positive")
            digest = hashlib.sha256(data).hexdigest()
            row.update(file=file, format=kind, pixels=[width, height], viewport=viewport,
                       capture=capture, sha256=digest)
            if capture == "viewport":
                error = abs((width / height) / (viewport[0] / viewport[1]) - 1)
                row["ratio_error"] = round(error, 6)
                if error > tolerance:
                    row["errors"].append("aspect ratio differs from viewport; check capture/resize state")
            if digest in hashes:
                row["warnings"].append(f"identical image bytes also used by {hashes[digest]}; verify scene identity")
            else:
                hashes[digest] = scene_id
        except (OSError, ValueError, TypeError, IndexError, struct.error) as error:
            row["errors"].append(str(error))
    return {"schema_version": 1, "round": spec.get("round"), "screenshots": results,
            "passed": sum(not row["errors"] for row in results),
            "failed": sum(bool(row["errors"]) for row in results),
            "warning_count": sum(len(row["warnings"]) for row in results)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--ratio-tolerance", type=float, default=0.03)
    args = parser.parse_args()
    try:
        if not math.isfinite(args.ratio_tolerance) or not 0 <= args.ratio_tolerance <= 1:
            raise ValueError("ratio-tolerance must be between 0 and 1")
        manifest = args.manifest.resolve()
        if args.output and args.output.resolve() == manifest:
            raise ValueError("output must not overwrite the manifest")
        result = verify(manifest, args.ratio_tolerance)
        if args.output:
            for shot in json.loads(manifest.read_text(encoding="utf-8"))["screenshots"]:
                if isinstance(shot, dict) and isinstance(shot.get("file"), str) and args.output.resolve() == (manifest.parent / shot["file"]).resolve():
                    raise ValueError("output must not overwrite a screenshot")
        output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
        print(output, end="")
        return int(result["failed"] > 0)
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
