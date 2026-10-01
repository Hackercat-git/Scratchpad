# Infrared

IR signal files for the Flipper Zero.

## File format

Flipper `.ir` files contain named signals in two formats:

```
Filetype: IR signals file
Version: 1
#
name: Power
type: parsed
protocol: NEC
address: 20 00 00 00
command: 08 00 00 00
#
name: VolUp
type: raw
frequency: 38000
duty_cycle: 0.330000
data: 9024 4512 564 564 564 ...
```

- **parsed**: Flipper decoded the protocol (NEC, Samsung36, RC6, etc.) — more reliable for re-transmission
- **raw**: raw timing data — works for any signal, even unknown protocols

## Files

| File | Description |
|------|-------------|
| `samsung_tv.ir` | Power, volume and source for common Samsung TVs (NEC protocol) |

## Tips

- Use **Infrared → Learn New Remote** to capture your own signals
- Parsed signals are more reliable than raw — try to capture multiple times and pick the cleanest
- The Flipper has a built-in universal remote under **Infrared → Universal Remotes**
