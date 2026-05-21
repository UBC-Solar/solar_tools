# PCAN-View (Py) — Launcher and UI

This folder adds a Bash launcher and a minimal PCAN-View style GUI for SocketCAN-based CAN debugging.

Files added:
- `pcan_launcher.sh` — interactive setup and launcher script
- `ui/pcan_view.py` — PySide6 GUI using `python-can` (SocketCAN)
- `requirements.txt` — Python deps

Quick start

1. Ensure SocketCAN tools are installed: `iproute2`, `can-utils` (for `cansend`, `candump`).
2. Create or activate a Python environment and install requirements:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the launcher:

```bash
chmod +x pcan_launcher.sh
./pcan_launcher.sh
```

Or run the GUI directly:

```bash
python3 ui/pcan_view.py
```

Notes and assumptions
- Uses SocketCAN via `python-can` (bustype `socketcan`).
- Requires Linux with SocketCAN support.
- The UI is intentionally lightweight and focuses on core features: live monitor, filtering, send panel, logging.

Suggested next steps
- Add DBC decoding (python-can supports dbc via cantools)
- Add graphs and bus load visualization
- Add presets persistence
