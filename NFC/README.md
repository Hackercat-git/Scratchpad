# NFC

NFC card dumps and handcrafted tag files for the Flipper Zero.

> ⚠️ **Only dump and emulate cards you own.** Cloning access cards you don't own is illegal.

## File format

Flipper NFC files (`.nfc`) are plain text:

```
Filetype: Flipper NFC device
Version: 4
Device type: NTAG215
UID: 04 AB CD 12 34 56 78
ATQA: 00 44
SAK: 00
Data format version: 2
NTAG215 pages total: 135
NTAG215 pages read: 135
Page 0: 04 AB CD 12
...
```

## Card types supported by Flipper

| Type | Common use |
|------|-----------|
| MIFARE Classic 1K/4K | Old access control, parking |
| MIFARE Ultralight / NTAG | Amiibo, event wristbands |
| EMV (read-only) | Bank cards — Flipper can read UID only |
| FeliCa | Japanese transit cards |

## Files

| File | Type | Description |
|------|------|-------------|
| `blank_ntag215.nfc` | NTAG215 | Blank NTAG215 template — useful as a starting point |

## Tips

- Use `NFC → Read` to dump a card; it gets saved to `SD/nfc/`
- MIFARE Classic needs a dictionary attack for encrypted sectors — use the Flipper's built-in Mfkey32
