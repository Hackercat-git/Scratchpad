#!/usr/bin/env python3
"""
sub_analyze.py — Analyze Flipper .sub files and show signal statistics

Usage:
  python sub_analyze.py signal.sub
  python sub_analyze.py signal.sub --raw
  python sub_analyze.py signal.sub --detect
"""

import argparse
import sys
from pathlib import Path


def parse_sub(path):
    meta = {}
    raw_rows = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("RAW_Data:"):
                values = list(map(int, line.split(":", 1)[1].split()))
                raw_rows.append(values)
            else:
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip()

    return meta, raw_rows


def analyze(raw_rows):
    all_pulses = []
    for row in raw_rows:
        all_pulses.extend(row)

    if not all_pulses:
        return None

    on_times = [v for v in all_pulses if v > 0]
    off_times = [abs(v) for v in all_pulses if v < 0]

    total_us = sum(abs(v) for v in all_pulses)

    return {
        "total_samples": len(all_pulses),
        "on_pulses": len(on_times),
        "off_pulses": len(off_times),
        "total_duration_ms": total_us / 1000,
        "on_min": min(on_times) if on_times else 0,
        "on_max": max(on_times) if on_times else 0,
        "on_avg": sum(on_times) // len(on_times) if on_times else 0,
        "off_min": min(off_times) if off_times else 0,
        "off_max": max(off_times) if off_times else 0,
        "off_avg": sum(off_times) // len(off_times) if off_times else 0,
        "raw_rows": len(raw_rows),
    }


def detect_encoding(stats):
    """Heuristic: try to guess encoding from pulse widths."""
    hints = []

    on_avg = stats["on_avg"]
    off_avg = stats["off_avg"]

    if 200 <= on_avg <= 600 and 200 <= off_avg <= 600:
        hints.append("Possible: NRZ / short OOK (garage, keyfob)")
    if 300 <= on_avg <= 700 and 500 <= off_avg <= 2000:
        hints.append("Possible: Manchester encoding")
    if stats["off_max"] > 5000:
        hints.append("Long gaps detected — likely repeated transmissions")
    if stats["on_avg"] < 300:
        hints.append("Very short pulses — check if signal is noise")

    return hints or ["No strong pattern detected"]


def main():
    parser = argparse.ArgumentParser(description="Analyze Flipper .sub signal files")
    parser.add_argument("file", help="Path to .sub file")
    parser.add_argument("--raw", action="store_true",
                        help="Print first 20 raw values per row")
    parser.add_argument("--detect", action="store_true",
                        help="Try to detect encoding heuristically")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    meta, raw_rows = parse_sub(path)
    stats = analyze(raw_rows)

    print(f"=== {path.name} ===")
    print()
    print("Metadata:")
    for k, v in meta.items():
        print(f"  {k}: {v}")
    print()

    if not stats:
        print("No RAW_Data found.")
        return

    print("Signal stats:")
    print(f"  RAW_Data rows : {stats['raw_rows']}")
    print(f"  Total samples : {stats['total_samples']}")
    print(f"  Duration      : {stats['total_duration_ms']:.1f} ms")
    print(f"  ON  pulses    : {stats['on_pulses']}  (min={stats['on_min']}µs  avg={stats['on_avg']}µs  max={stats['on_max']}µs)")
    print(f"  OFF pulses    : {stats['off_pulses']}  (min={stats['off_min']}µs  avg={stats['off_avg']}µs  max={stats['off_max']}µs)")

    if args.detect:
        print()
        print("Encoding hints:")
        for h in detect_encoding(stats):
            print(f"  • {h}")

    if args.raw:
        print()
        print("Raw values (first 20 per row):")
        for i, row in enumerate(raw_rows):
            preview = " ".join(str(v) for v in row[:20])
            suffix = "..." if len(row) > 20 else ""
            print(f"  Row {i+1}: {preview}{suffix}")


if __name__ == "__main__":
    main()
