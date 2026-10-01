#!/usr/bin/env python3
"""sub_gen.py — Generate Flipper Zero SubGHz RAW files (.sub) from a bit pattern.

Usage examples:
  # Simple repeating pattern at 433.92 MHz
  python sub_gen.py --bits 10110100 --freq 433920000 --repeat 3 -o signal.sub

  # Custom pulse/gap timings
  python sub_gen.py --bits 10110100 --short 500 --long 1000 --gap 10000 -o signal.sub
"""

import argparse
import sys


PRESETS = {
    433: "FuriHalSubGhzPresetOok650Async",
    315: "FuriHalSubGhzPresetOok650Async",
    868: "FuriHalSubGhzPresetOok650Async",
}


def bits_to_raw(bits: str, short: int, long: int, gap: int) -> list[int]:
    """Convert a binary string to Flipper RAW_Data timings.

    Convention: positive = on, negative = off.
    '1' → long pulse + short gap
    '0' → short pulse + short gap
    End of sequence → long gap (silence)
    """
    raw = []
    for b in bits:
        if b == "1":
            raw.append(long)       # on
            raw.append(-short)     # off
        elif b == "0":
            raw.append(short)      # on
            raw.append(-short)     # off
        else:
            sys.exit(f"Invalid bit character: {b!r} — only '0' and '1' allowed")
    raw.append(-gap)  # trailing silence
    return raw


def write_sub(path: str, freq: int, raw_lines: list[list[int]]) -> None:
    freq_mhz = freq / 1_000_000
    preset = PRESETS.get(int(freq_mhz), "FuriHalSubGhzPresetOok650Async")

    with open(path, "w", encoding="utf-8") as f:
        f.write("Filetype: Flipper SubGhz RAW File\n")
        f.write("Version: 1\n")
        f.write(f"Frequency: {freq}\n")
        f.write(f"Preset: {preset}\n")
        f.write("Protocol: RAW\n")
        for row in raw_lines:
            f.write("RAW_Data: " + " ".join(map(str, row)) + "\n")

    print(f"Written {len(raw_lines)} repetition(s) → {path}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate a Flipper SubGHz .sub file from a bit pattern.")
    parser.add_argument("--bits", required=True, help="Binary string, e.g. 10110100")
    parser.add_argument("--freq", type=int, default=433_920_000, help="Frequency in Hz (default: 433920000)")
    parser.add_argument("--short", type=int, default=500, help="Short pulse duration µs (default: 500)")
    parser.add_argument("--long", type=int, default=1000, help="Long pulse duration µs (default: 1000)")
    parser.add_argument("--gap", type=int, default=10_000, help="Trailing silence µs (default: 10000)")
    parser.add_argument("--repeat", type=int, default=3, help="Number of repetitions (default: 3)")
    parser.add_argument("-o", "--output", default="output.sub", help="Output file path (default: output.sub)")
    args = parser.parse_args(argv)

    raw = bits_to_raw(args.bits, args.short, args.long, args.gap)
    write_sub(args.output, args.freq, [raw] * args.repeat)


if __name__ == "__main__":
    main()
