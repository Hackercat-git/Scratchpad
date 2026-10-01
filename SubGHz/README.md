# SubGHz

Raw SubGHz captures and handcrafted signal files for the Flipper Zero.

> ⚠️ **Transmitting captured signals at unauthorised frequencies or to systems you don't own is illegal in most countries.** These files are for study, testing on your own devices, and understanding signal structures.

## File format

Flipper SubGHz files use a plain-text format:

```
Filetype: Flipper SubGhz RAW File
Version: 1
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: -100 200 -300 400 ...
```

- **Frequency**: in Hz (433.92 MHz is the most common unlicensed band in EU)
- **Preset**: modulation — `OOK` (on-off keying) is typical for remote controls
- **RAW_Data**: alternating on/off durations in microseconds (negative = off)

## Files

| File | Frequency | Description |
|------|-----------|-------------|
| `test_pattern_433.sub` | 433.92 MHz | Synthetic repeating test pattern — safe to capture and compare |

## Tips

- Use **Frequency Analyzer** on the Flipper to find what frequency a remote uses
- Capture with **SubGHz → Read RAW** for unknown protocols
- Use `tools/sub_gen.py` to generate `.sub` files programmatically
