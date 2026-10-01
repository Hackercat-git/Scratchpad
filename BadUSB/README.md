# BadUSB

Ducky Script payloads for the Flipper Zero BadUSB module.

> ⚠️ **For educational and authorised testing only.** Only run these on devices you own or have explicit permission to test.

## Scripts

| File | Target | Description |
|------|--------|-------------|
| `sysinfo_windows.txt` | Windows 10/11 | Dumps system info, network config and local users to Desktop |
| `wifi_passwords_windows.txt` | Windows 10/11 | Exports saved WiFi profiles + cleartext keys to Desktop |
| `lock_troll_windows.txt` | Windows 10/11 | Opens Notepad with a message, then locks the screen |

## How to use

1. Copy the `.txt` file to `SD/badusb/` on your Flipper Zero
2. In the Flipper menu: **Bad USB → [file] → Run**
3. Make sure the target machine's keyboard layout matches (default: US)

## Keyboard layout note

Scripts are written for **US QWERTY**. If the target uses a different layout (e.g. Dutch/Belgian), some symbols may come out wrong. Either switch the target layout temporarily or adjust the script.
