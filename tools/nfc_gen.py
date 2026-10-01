#!/usr/bin/env python3
"""
nfc_gen.py — Generate blank Flipper NFC card files

Usage:
  python nfc_gen.py --type ntag215 -o blank.nfc
  python nfc_gen.py --type mifare1k --uid AA BB CC DD -o card.nfc
  python nfc_gen.py --list
"""

import argparse
import sys

CARD_TYPES = {
    "ntag213": {
        "Device type": "NTAG213",
        "ATQA": "00 44",
        "SAK": "00",
        "uid_len": 7,
        "pages": 45,
        "page_size": 4,
    },
    "ntag215": {
        "Device type": "NTAG215",
        "ATQA": "00 44",
        "SAK": "00",
        "uid_len": 7,
        "pages": 135,
        "page_size": 4,
    },
    "ntag216": {
        "Device type": "NTAG216",
        "ATQA": "00 44",
        "SAK": "00",
        "uid_len": 7,
        "pages": 231,
        "page_size": 4,
    },
    "mifare1k": {
        "Device type": "Mifare Classic 1K",
        "ATQA": "00 04",
        "SAK": "08",
        "uid_len": 4,
        "sectors": 16,
        "blocks_per_sector": 4,
    },
    "mifare4k": {
        "Device type": "Mifare Classic 4K",
        "ATQA": "00 02",
        "SAK": "18",
        "uid_len": 4,
        "sectors": 40,
        "blocks_per_sector": 4,
    },
}


def format_uid(uid_bytes):
    return " ".join(f"{b:02X}" for b in uid_bytes)


def make_ntag(card, uid):
    uid_str = format_uid(uid)
    pages = card["pages"]
    page_size = card["page_size"]

    lines = [
        "Filetype: Flipper NFC device",
        "Version: 4",
        f"Device type: {card['Device type']}",
        f"UID: {uid_str}",
        f"ATQA: {card['ATQA']}",
        f"SAK: {card['SAK']}",
        "Pages total: " + str(pages),
        "Pages read: " + str(pages),
    ]

    for i in range(pages):
        data = "00 " * page_size
        lines.append(f"Page {i}: {data.strip()}")

    return "\n".join(lines) + "\n"


def make_mifare(card, uid):
    uid_str = format_uid(uid)
    sectors = card["sectors"]
    bps = card["blocks_per_sector"]
    total_blocks = sectors * bps

    lines = [
        "Filetype: Flipper NFC device",
        "Version: 4",
        f"Device type: {card['Device type']}",
        f"UID: {uid_str}",
        f"ATQA: {card['ATQA']}",
        f"SAK: {card['SAK']}",
    ]

    for b in range(total_blocks):
        # Sector trailer blocks get default keys
        if (b + 1) % bps == 0:
            lines.append(f"Block {b}: FF FF FF FF FF FF FF 07 80 69 FF FF FF FF FF FF")
        else:
            lines.append(f"Block {b}: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

    return "\n".join(lines) + "\n"


def parse_uid(uid_str, expected_len):
    parts = uid_str.upper().split()
    if len(parts) != expected_len:
        raise ValueError(f"Expected {expected_len} UID bytes, got {len(parts)}")
    return [int(x, 16) for x in parts]


def main():
    parser = argparse.ArgumentParser(description="Generate blank Flipper NFC card files")
    parser.add_argument("--type", "-t", default="ntag215",
                        choices=list(CARD_TYPES.keys()),
                        help="Card type (default: ntag215)")
    parser.add_argument("--uid", nargs="+", metavar="HH",
                        help="UID bytes in hex (e.g. 04 AB CD EF 01 02 03)")
    parser.add_argument("-o", "--output", default=None,
                        help="Output file (default: stdout)")
    parser.add_argument("--list", action="store_true",
                        help="List supported card types")
    args = parser.parse_args()

    if args.list:
        print(f"{'Type':<12} {'Device name':<26} {'UID len'}")
        print("-" * 50)
        for k, v in CARD_TYPES.items():
            print(f"{k:<12} {v['Device type']:<26} {v['uid_len']}")
        return

    card = CARD_TYPES[args.type]
    uid_len = card["uid_len"]

    if args.uid:
        uid = parse_uid(" ".join(args.uid), uid_len)
    else:
        uid = [0x04] + [0x00] * (uid_len - 1)

    if "pages" in card:
        content = make_ntag(card, uid)
    else:
        content = make_mifare(card, uid)

    if args.output:
        with open(args.output, "w") as f:
            f.write(content)
        print(f"Wrote {args.output}")
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
