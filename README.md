# 🐾 Scratchpad

Personal Flipper Zero collection by [Hackercat-git](https://github.com/Hackercat-git) — curated BadUSB payloads, SubGHz captures, NFC dumps, IR signals, and Python tools to work with them.

> ⚠️ **For educational and authorized use only.** Only use these on devices and systems you own or have explicit permission to test.

---

## 📁 Structure

| Folder | Contents |
|--------|----------|
| [`BadUSB/`](BadUSB/) | Ducky Script payloads for Windows |
| [`SubGHz/`](SubGHz/) | SubGHz RAW captures (`.sub`) |
| [`NFC/`](NFC/) | NFC card dumps (`.nfc`) |
| [`Infrared/`](Infrared/) | IR signal files (`.ir`) |
| [`tools/`](tools/) | Python CLI tools to generate and parse files |

---

## 🛠️ Tools

Three standalone Python tools (no external dependencies):

```bash
python tools/sub_gen.py --bits 10110100 --freq 433920000 -o out.sub
python tools/ir_parser.py signals.ir --list
python tools/badusb_gen.py --template sysinfo -o payload.txt
```

→ See [`tools/README.md`](tools/README.md) for full usage.

---

## 📋 Requirements

- **Flipper Zero** with latest firmware
- **Python 3.8+** for the tools (no pip installs needed)
- Files go on the SD card under the matching folder (`SD Card/badusb/`, `SD Card/subghz/raw/`, etc.)

---

## 📄 License

MIT — see [LICENSE](LICENSE). Use responsibly.
