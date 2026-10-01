# BadUSB Payloads

Ducky Script payloads for the Flipper Zero BadUSB module.

> ⚠️ **For educational and authorized use only.**  
> Only run these on devices you own or have explicit permission to test.

---

## Scripts

| File | Target | Description |
|------|--------|-------------|
| `sysinfo_windows.txt` | Windows | Dumps system info to `sysinfo.txt` on the Desktop |
| `wifi_passwords_windows.txt` | Windows | Exports saved Wi-Fi profiles and passwords |
| `lock_troll_windows.txt` | Windows | Opens Notepad with a message, then locks the screen |
| `open_url_windows.txt` | Windows | Opens a URL via the Run dialog |
| `reverse_shell_linux.txt` | Linux | Starts a reverse bash shell (change IP/PORT first!) |
| `add_ssh_key_linux.txt` | Linux | Adds an SSH public key to `~/.ssh/authorized_keys` |

---

## How to use

1. Copy the `.txt` file to `SD Card/badusb/` on your Flipper
2. Go to **BadUSB** on the Flipper menu
3. Select your script and plug in via USB

---

## Notes

- All Windows payloads use `GUI r` (Win+R) to open the Run dialog — works on Win 10 & 11
- Linux payloads use `CTRL-ALT t` for terminal — works on Ubuntu/GNOME; may differ on other DEs
- Adjust `DELAY` values if the target machine is slow
- Always check keyboard layout (`SET LOCALE`) if running on non-US keyboards
