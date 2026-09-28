#!/usr/bin/env python3
"""Visual reference QA for rendered creatives.

Compares a candidate MP4 against an approved visual reference. The goal is not
to prove pixel identity; it is to catch macro drift in composition, timing and
art direction before a render is called "approved".
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=True)


def probe(path: Path) -> dict:
    out = run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration:stream=width,height,r_frame_rate",
        "-of", "json", str(path),
    ]).stdout
    return json.loads(out)


def ssim(reference: Path, candidate: Path) -> float | None:
    # Normalize dimensions and timeline before measuring. SSIM is advisory:
    # copy or asset changes can lower it even when geometry is intentionally locked.
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(candidate), "-i", str(reference),
        "-lavfi",
        "[0:v]scale=540:960:flags=lanczos,setpts=PTS-STARTPTS[c];"
        "[1:v]scale=540:960:flags=lanczos,setpts=PTS-STARTPTS[r];"
        "[c][r]ssim",
        "-f", "null", "-"
    ]
    p = subprocess.run(cmd, text=True, capture_output=True)
    m = re.findall(r"All:([0-9.]+)", p.stderr)
    return float(m[-1]) if m else None


def frame(video: Path, t: float, dest: Path) -> None:
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(video),
        "-frames:v", "1", "-vf", "scale=360:-2", str(dest)
    ])


def contact_sheet(reference: Path, candidate: Path, times: list[float], out: Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        pairs = []
        for i, t in enumerate(times):
            rp, cp = td / f"r{i}.jpg", td / f"c{i}.jpg"
            frame(reference, t, rp)
            frame(candidate, t, cp)
            pairs.append((Image.open(rp).convert("RGB"), Image.open(cp).convert("RGB"), t))

        w = max(im.width for pair in pairs for im in pair[:2])
        h = max(im.height for pair in pairs for im in pair[:2])
        label_h = 34
        sheet = Image.new("RGB", (w * 2, (h + label_h) * len(pairs)), (18, 18, 18))
        draw = ImageDraw.Draw(sheet)
        for row, (r, c, t) in enumerate(pairs):
            y = row * (h + label_h)
            sheet.paste(r, (0, y))
            sheet.paste(c, (w, y))
            draw.text((8, y + h + 8), f"REFERENCE  {t:.2f}s", fill="white")
            draw.text((w + 8, y + h + 8), f"CANDIDATE  {t:.2f}s", fill="white")
        out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out, quality=92)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference", required=True, type=Path)
    ap.add_argument("--candidate", required=True, type=Path)
    ap.add_argument("--out-dir", type=Path, default=Path(".visual-qa"))
    ap.add_argument("--timestamps", default="0.5,2.5,5,7.5,10,12.5,15,17")
    ap.add_argument("--max-duration-drift", type=float, default=0.35)
    ap.add_argument("--min-ssim", type=float, default=None,
                    help="Optional hard gate. Leave unset for advisory SSIM.")
    args = ap.parse_args()

    ref_meta, cand_meta = probe(args.reference), probe(args.candidate)
    rd = float(ref_meta["format"]["duration"])
    cd = float(cand_meta["format"]["duration"])
    drift = abs(rd - cd)

    times = [float(x.strip()) for x in args.timestamps.split(",") if x.strip()]
    # Never request a frame beyond the shorter render.
    limit = max(0.0, min(rd, cd) - 0.05)
    times = [min(t, limit) for t in times]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    sheet = args.out_dir / "reference-vs-candidate.jpg"
    contact_sheet(args.reference, args.candidate, times, sheet)
    score = ssim(args.reference, args.candidate)

    report = {
        "reference": str(args.reference),
        "candidate": str(args.candidate),
        "reference_duration": rd,
        "candidate_duration": cd,
        "duration_drift_seconds": drift,
        "ssim_advisory": score,
        "timestamps_seconds": times,
        "contact_sheet": str(sheet),
        "status": "pass",
        "reasons": [],
    }
    if drift > args.max_duration_drift:
        report["status"] = "block"
        report["reasons"].append(
            f"duration drift {drift:.3f}s exceeds {args.max_duration_drift:.3f}s"
        )
    if args.min_ssim is not None and score is not None and score < args.min_ssim:
        report["status"] = "block"
        report["reasons"].append(
            f"SSIM {score:.4f} is below required {args.min_ssim:.4f}"
        )

    (args.out_dir / "visual-reference-qa.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["status"] == "block":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
