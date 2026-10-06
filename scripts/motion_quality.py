#!/usr/bin/env python3
"""Lightweight deterministic motion QA for Tesseract Lab video renders.

Measures technical validity plus low-motion runs and final hold from sampled frames.
It intentionally does not judge taste: M1/M4/M5/M6 remain visual/manual gates.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import subprocess
from pathlib import Path


def run(cmd: list[str], *, binary: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=not binary,
    )


def probe(path: str) -> dict:
    p = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path])
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "ffprobe failed")
    return json.loads(p.stdout)


def video_meta(meta: dict) -> dict:
    streams = meta.get("streams") or []
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    if not video:
        return {}
    fmt = meta.get("format") or {}
    try:
        duration = float(fmt.get("duration") or video.get("duration") or 0)
    except (TypeError, ValueError):
        duration = 0.0
    return {
        "codec": video.get("codec_name"),
        "width": int(video.get("width") or 0),
        "height": int(video.get("height") or 0),
        "pix_fmt": video.get("pix_fmt"),
        "duration": duration,
        "avg_frame_rate": video.get("avg_frame_rate") or video.get("r_frame_rate"),
    }


def sample_gray(path: str, fps: float, width: int, height: int) -> list[bytes]:
    vf = f"fps={fps:g},scale={width}:{height}:flags=area,format=gray"
    p = run([
        "ffmpeg", "-v", "error", "-i", path, "-an", "-vf", vf,
        "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1"
    ], binary=True)
    if p.returncode != 0:
        err = p.stderr.decode("utf-8", "replace") if isinstance(p.stderr, bytes) else p.stderr
        raise RuntimeError((err or "ffmpeg sampling failed").strip())
    frame_size = width * height
    data = p.stdout
    return [data[i:i + frame_size] for i in range(0, len(data) - frame_size + 1, frame_size)]


def mean_abs_diff(a: bytes, b: bytes) -> float:
    if not a or len(a) != len(b):
        return 1.0
    return sum(abs(x - y) for x, y in zip(a, b)) / (len(a) * 255.0)


def stddev_norm(frame: bytes) -> float:
    if not frame:
        return 0.0
    mean = sum(frame) / len(frame)
    var = sum((x - mean) ** 2 for x in frame) / len(frame)
    return math.sqrt(var) / 255.0


def longest_low_motion_run(diffs: list[float], threshold: float) -> tuple[int, int]:
    best = cur = 0
    end = -1
    for i, d in enumerate(diffs):
        if d <= threshold:
            cur += 1
            if cur > best:
                best = cur
                end = i
        else:
            cur = 0
    return best, end


def trailing_low_motion_run(diffs: list[float], threshold: float) -> int:
    n = 0
    for d in reversed(diffs):
        if d <= threshold:
            n += 1
        else:
            break
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--sample-fps", type=float, default=8.0)
    ap.add_argument("--sample-width", type=int, default=96)
    ap.add_argument("--sample-height", type=int, default=54)
    ap.add_argument("--flat-threshold", type=float, default=0.005,
                    help="mean normalized luma delta considered nearly static")
    ap.add_argument("--max-flat-seconds", type=float, default=0.75)
    ap.add_argument("--max-end-hold-seconds", type=float, default=1.40)
    ap.add_argument("--json-out")
    args = ap.parse_args()

    src = Path(args.input)
    result = {
        "input": str(src),
        "status": "block",
        "gates": {},
        "metrics": {},
        "notes": [
            "Automatic gates are signals, not taste judgements.",
            "Intentional stillness may override M2/M3 when documented in notes.md."
        ],
    }

    if not src.is_file() or src.stat().st_size == 0:
        result["gates"]["M0"] = {"status": "block", "reason": "file missing or empty"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    try:
        meta = video_meta(probe(str(src)))
        if not meta or meta["duration"] <= 0 or meta["width"] <= 0 or meta["height"] <= 0:
            raise RuntimeError("no valid video stream")
        result["gates"]["M0"] = {"status": "pass", "reason": "video decodes and has positive duration"}
        result["metrics"]["video"] = meta

        frames = sample_gray(str(src), args.sample_fps, args.sample_width, args.sample_height)
        if len(frames) < 2:
            raise RuntimeError("too few sampled frames")

        diffs = [mean_abs_diff(frames[i - 1], frames[i]) for i in range(1, len(frames))]
        texture = [stddev_norm(f) for f in frames]
        longest_n, longest_end = longest_low_motion_run(diffs, args.flat_threshold)
        trailing_n = trailing_low_motion_run(diffs, args.flat_threshold)
        longest_s = longest_n / args.sample_fps
        trailing_s = trailing_n / args.sample_fps
        low_fraction = sum(d <= args.flat_threshold for d in diffs) / len(diffs)
        median_diff = statistics.median(diffs) if diffs else 0.0
        median_texture = statistics.median(texture) if texture else 0.0

        result["metrics"].update({
            "sample_fps": args.sample_fps,
            "sample_size": [args.sample_width, args.sample_height],
            "flat_threshold": args.flat_threshold,
            "sampled_frames": len(frames),
            "median_frame_delta": round(median_diff, 6),
            "low_motion_fraction": round(low_fraction, 4),
            "longest_low_motion_seconds": round(longest_s, 3),
            "longest_low_motion_end_seconds": round((longest_end + 1) / args.sample_fps, 3) if longest_end >= 0 else None,
            "final_hold_seconds": round(trailing_s, 3),
            "median_frame_texture": round(median_texture, 6),
        })

        m2 = "review" if longest_s > args.max_flat_seconds else "pass"
        m3 = "review" if trailing_s > args.max_end_hold_seconds else "pass"
        result["gates"]["M2"] = {
            "status": m2,
            "reason": f"longest near-static run {longest_s:.2f}s; review above {args.max_flat_seconds:.2f}s"
        }
        result["gates"]["M3"] = {
            "status": m3,
            "reason": f"final near-static hold {trailing_s:.2f}s; review above {args.max_end_hold_seconds:.2f}s"
        }
        result["gates"]["M1"] = {"status": "manual", "reason": "product/proof readability requires visual inspection"}
        result["gates"]["M4"] = {"status": "manual", "reason": "one-hero hierarchy requires visual inspection"}
        result["gates"]["M5"] = {"status": "manual", "reason": "anti-page-chrome requires source/contact-sheet review"}
        result["gates"]["M6"] = {"status": "manual", "reason": "brand world/coherence requires visual inspection"}
        result["gates"]["M7"] = {"status": "manual", "reason": "beat buys are checked in storyboard"}

        result["status"] = "review" if "review" in (m2, m3) else "pass"
    except Exception as exc:
        result["gates"]["M0"] = {"status": "block", "reason": str(exc)}
        result["status"] = "block"

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        Path(args.json_out).write_text(payload + "\n", encoding="utf-8")
    return 2 if result["status"] == "block" else 0


if __name__ == "__main__":
    raise SystemExit(main())
