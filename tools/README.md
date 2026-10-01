# Tools

Python utilities for generating and parsing Flipper Zero files. No dependencies beyond the standard library.

## Scripts

### `sub_gen.py` — SubGHz file generator

Converts a binary bit pattern into a Flipper `.sub` file.

```bash
# Generate a signal at 433.92 MHz, repeated 3 times
python sub_gen.py --bits 10110100 --freq 433920000 --repeat 3 -o my_signal.sub

# Custom timings
python sub_gen.py --bits 10110100 --short 400 --long 900 --gap 12000 -o custom.sub
```

### `ir_parser.py` — IR file inspector

Lists and inspects signals in a Flipper `.ir` file. Can convert parsed NEC signals back to raw timings.

```bash
# List all signals
python ir_parser.py ../Infrared/samsung_tv.ir

# Inspect one signal
python ir_parser.py ../Infrared/samsung_tv.ir --name Power

# Convert NEC to raw
python ir_parser.py ../Infrared/samsung_tv.ir --name Power --to-raw
```

### `badusb_gen.py` — BadUSB payload generator

Generates Ducky Script payloads from named templates.

```bash
# List templates
python badusb_gen.py --list

# Generate a troll payload
python badusb_gen.py troll --message "You got hackercatted 🐾" -o troll.txt

# Generate a sysinfo payload
python badusb_gen.py sysinfo --outpath "C:\\Users\\Public\\info.txt" -o sysinfo.txt
```
