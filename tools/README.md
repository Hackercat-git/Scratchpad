# Tools

Standalone Python CLI tools for generating and analyzing Flipper Zero files.  
No external dependencies — Python 3.8+ only.

---

## sub_gen.py — SubGHz file generator

Converts a binary bit string into a Flipper `.sub` RAW file.

```bash
# Basic usage
python tools/sub_gen.py --bits 10110100 -o out.sub

# Custom frequency and timing
python tools/sub_gen.py --bits 1010101010110011 --freq 315000000 --short 300 --long 900 -o out.sub

# Repeat signal 5 times
python tools/sub_gen.py --bits 10110100 --repeat 5 -o out.sub
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--bits` | required | Binary string (e.g. `10110100`) |
| `--freq` | 433920000 | Frequency in Hz |
| `--short` | 500 | Short pulse duration (µs) |
| `--long` | 1000 | Long pulse duration (µs) |
| `--gap` | 10000 | Gap between repeats (µs) |
| `--repeat` | 3 | Number of RAW_Data repetitions |
| `-o` | stdout | Output file path |

---

## sub_analyze.py — SubGHz file analyzer

Reads a `.sub` file and shows signal statistics and encoding hints.

```bash
# Basic stats
python tools/sub_analyze.py SubGHz/test_pattern_433.sub

# Show raw values
python tools/sub_analyze.py signal.sub --raw

# Heuristic encoding detection
python tools/sub_analyze.py signal.sub --detect
```

| Argument | Description |
|----------|-------------|
| `file` | Path to `.sub` file |
| `--raw` | Print first 20 raw values per row |
| `--detect` | Try to guess encoding from pulse widths |

---

## nfc_gen.py — NFC card file generator

Generates blank Flipper `.nfc` files for various card types.

```bash
# List supported card types
python tools/nfc_gen.py --list

# Generate blank NTAG215
python tools/nfc_gen.py --type ntag215 -o blank.nfc

# Generate MIFARE Classic 1K with custom UID
python tools/nfc_gen.py --type mifare1k --uid AA BB CC DD -o card.nfc

# NTAG213 with custom 7-byte UID
python tools/nfc_gen.py --type ntag213 --uid 04 AB CD EF 01 02 03 -o tag.nfc
```

Supported types: `ntag213`, `ntag215`, `ntag216`, `mifare1k`, `mifare4k`

---

## ir_parser.py — IR signal file parser

Reads `.ir` files, lists signals, and can convert parsed NEC signals to raw timing.

```bash
# List all signals in a file
python tools/ir_parser.py Infrared/samsung_tv.ir --list

# Convert parsed signal to raw timing data
python tools/ir_parser.py Infrared/samsung_tv.ir --to-raw Power
```

---

## badusb_gen.py — BadUSB script generator

Generates Ducky Script from built-in templates.

```bash
# Generate sysinfo payload
python tools/badusb_gen.py --template sysinfo -o payload.txt

# Generate troll payload
python tools/badusb_gen.py --template troll -o troll.txt

# Open a URL
python tools/badusb_gen.py --template open_url --url https://example.com -o open.txt
```

Templates: `troll`, `sysinfo`, `open_url`
