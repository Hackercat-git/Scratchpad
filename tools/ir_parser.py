#!/usr/bin/env python3
"""ir_parser.py — Parse and inspect Flipper Zero IR signal files (.ir).

Usage examples:
  # List all signals in a file
  python ir_parser.py samsung_tv.ir

  # Show raw timing data for a specific signal
  python ir_parser.py samsung_tv.ir --name Power

  # Convert a parsed NEC signal back to raw timings and print them
  python ir_parser.py samsung_tv.ir --name Power --to-raw
"""

import argparse
import sys
from pathlib import Path


def parse_ir_file(path: str) -> list[dict]:
    """Parse a .ir file into a list of signal dicts."""
    signals = []
    current = {}

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                if current:
                    signals.append(current)
                    current = {}
                continue
            if line.startswith("Filetype:") or line.startswith("Version:"):
                continue
            if ":" in line:
                key, _, value = line.partition(":")
                current[key.strip()] = value.strip()

    if current:
        signals.append(current)

    return signals


def nec_to_raw(address: str, command: str, freq: int = 38_000) -> list[int]:
    """Approximate NEC protocol timing from parsed address/command bytes."""
    addr_bytes = [int(b, 16) for b in address.split()]
    cmd_bytes = [int(b, 16) for b in command.split()]

    bits = []
    for byte in addr_bytes[:1] + cmd_bytes[:1]:
        for i in range(8):
            bits.append((byte >> i) & 1)

    LEADER_ON  = 9000
    LEADER_OFF = 4500
    BIT_ON     = 560
    BIT_ONE_OFF = 1690
    BIT_ZERO_OFF = 560
    TRAIL = 560

    raw = [LEADER_ON, -LEADER_OFF]
    for bit in bits:
        raw.append(BIT_ON)
        raw.append(-(BIT_ONE_OFF if bit else BIT_ZERO_OFF))
    raw.append(TRAIL)
    return raw


def main(argv=None):
    parser = argparse.ArgumentParser(description="Parse and inspect Flipper IR files.")
    parser.add_argument("file", help="Path to the .ir file")
    parser.add_argument("--name", help="Signal name to inspect")
    parser.add_argument("--to-raw", action="store_true", help="Convert parsed NEC signal to raw timings")
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.exists():
        sys.exit(f"File not found: {path}")

    signals = parse_ir_file(str(path))

    if not args.name:
        print(f"{'Name':<20} {'Type':<10} {'Protocol':<15} {'Address'}")
        print("-" * 60)
        for s in signals:
            print(f"{s.get('name','?'):<20} {s.get('type','?'):<10} {s.get('protocol','—'):<15} {s.get('address','—')}")
        return

    match = next((s for s in signals if s.get("name") == args.name), None)
    if not match:
        sys.exit(f"Signal '{args.name}' not found. Available: {[s.get('name') for s in signals]}")

    print(f"Signal: {match.get('name')}")
    for k, v in match.items():
        if k != "name":
            print(f"  {k}: {v}")

    if args.to_raw and match.get("type") == "parsed" and "NEC" in match.get("protocol", ""):
        raw = nec_to_raw(match["address"], match["command"])
        print(f"\nApproximate RAW_Data:\n  {' '.join(map(str, raw))}")


if __name__ == "__main__":
    main()
