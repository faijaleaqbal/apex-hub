# ⚡ Apex Hub - Gaming Peripheral Control Suite

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6.svg)](https://www.microsoft.com/windows)
[![UI Engine](https://img.shields.io/badge/UI-WebView2%20%28Chromium%29-00D2B4.svg)](https://developer.microsoft.com/microsoft-edge/webview2/)
[![Design](https://img.shields.io/badge/Theme-Obsidian%20Telemetry-121316.svg)](https://stitch.design)

**Apex Hub** is a lightweight, low-latency, commercial-grade Windows desktop control suite designed for gaming peripherals:
- **Keyboard:** Tailored for **Karnage Visage Tri-Mode Gaming Keyboard (`WLKM-054`)** and all Windows keyboards.
- **Mouse:** Tailored for **Arctic Fox 2.4GHz Wireless Gaming Mouse** and all Windows mice.
- **Universal Support:** Compatible with **any** keyboard, mouse, and motherboard on Windows 10 & 11.

Designed with **Obsidian Telemetry** styling (inspired by Logitech G HUB & Nothing OS) powered by native Windows WebView2 (Chromium engine) for 60+ FPS glassmorphism with zero Tkinter clipping artifacts.

---

## 🎮 Core Features

### 🖱️ Mouse & DPI Tuning
- **5-Stage Optical DPI Selector:** Direct 1-click stage switching (`800`, `1200`, `1600`, `2400`, `3200 DPI`) matching physical mouse sensor presets.
- **Custom DPI Input:** Enter arbitrary target DPI values (from 200 up to 12,000 DPI).
- **Lag-Free Sensitivity Scaling:** Non-stuttering memory scaling (1–20 multiplier, 0.03x to 3.50x).
- **Effective Calculated eDPI:** Live formula telemetry: `Base DPI × Multiplier = Effective eDPI`.
- **🔭 Sniper Aim Precision (`F7`):** Instantly cuts cursor speed to configurable sniper precision (default `3/20`) for steady scope aiming; press `F7` again to restore normal speed.
- **⚡ High-Speed Auto-Clicker (`F6`):** Multi-threaded burst clicker (1 to 50 CPS) with Left, Right, or Middle click selection.
- **Pointer Precision & Button Swap:** Direct Win32 acceleration toggle and left-handed mouse button swapping.

### ⌨️ Keyboard Engine
- **🛡️ Gaming WinLock:** Intercepts and suppresses the Windows Meta/Start key at the kernel hook level to prevent accidental desktop tab-outs during competitive matches.
- **⚡ Turbo Rapid Trigger:** Configurable rapid-fire key repeater (5 to 50 presses/sec) while holding designated keys (e.g., `Space` for bunnyhopping, `E`/`F` for fast looting).
- **🔒 Lock Keys HUD:** Live status badges in the navigation bar for `CAPS`, `NUM`, and `WINLOCK`.
- **📊 Real-Time Typing Telemetry:** Live Session Keystroke Counter, KPS (Keys per second), and estimated WPM gauge.
- **🚀 1-Click Game & App Binds:** Quick function key mappings for Steam, Discord, Spotify, Task Manager, and Calculator.
- **🔀 Custom Remap Rules:** Map physical keys to multimedia audio controls, custom app launchers, or automated text expansion macros.

### 🎧 Switch Acoustics & Screen Aura
- **Mechanical Switch Audio Simulator:** Synthesized tactile feedback on physical keystrokes with 4 switch profiles (Thocky Tactile, Crisp Clicky, Creamy Linear, Bubble Pop). *Muted by default.*
- **Screen Border Ambient RGB:** Layered, click-through desktop screen border glow that reacts to typing without capturing mouse focus.

### 🔒 Reliability & Architecture
- **Single-Instance IPC:** Running the app or clicking its shortcut while it's already active brings the existing window to the foreground instead of launching duplicate processes.
- **Background Persistence:** Closing the window with `✕` hides it to the background so your **WinLock**, **Auto-Clicker (F6)**, **Sniper Mode (F7)**, and **Key Remaps** continue running during gameplay.
- **Permanent Storage:** All configuration is automatically persisted to `%APPDATA%\ApexHub\config.json`, and mouse sensitivity is written directly to the Windows Registry (`HKCU\Control Panel\Mouse\MouseSensitivity`) via `SPIF_UPDATEINIFILE` so settings survive reboots.

---

## ⌨️ Karnage Visage Tri-Mode Hardware Lighting Matrix

Since the WLKM-054 uses an onboard hardware lighting microcontroller, color modes are driven directly via physical key shortcuts:

| Shortcut | Function | Description |
| :--- | :--- | :--- |
| **`Fn + Enter`** | **Cycle 15 RGB Modes** | Breathing, Static, RGB Wave, Color Shift, Reactive, Ripple, etc. |
| **`Fn + \`** | **Solid Color Select** | Cycles 8 solid static colors (Red, Blue, Green, Cyan, Purple, Yellow, White, Orange) |
| **`Fn + Backspace`** | **LED Power Toggle** | Turns LED backlighting completely ON or OFF |
| **`Fn + Up / Down`** | **Brightness Tuning** | Adjusts backlighting brightness levels (4-stage) |
| **`Fn + Left / Right`**| **Animation Speed** | Increases or decreases dynamic lighting wave speed |
| **Rotary Dial Knob** | **Multifunction Dial** | Turn for master volume; press to switch to RGB brightness dial |

---

## 📂 Project Structure

```
ApexHub/
├── assets/
│   ├── icon.ico                # Desktop and window application icon
│   └── sounds/                 # Switch acoustics (Thock, Clicky, Creamy, Bubble)
├── core/
│   ├── config_manager.py       # Persistence in %APPDATA%/ApexHub/config.json
│   ├── device_detector.py      # PnP Hardware identifier for Karnage & Arctic Fox
│   ├── mouse_service.py        # Win32 pointer speed, DPI stages, sniper aim, auto-clicker
│   ├── keyboard_service.py     # WinLock, turbo rapid trigger, global hooks, key remapper
│   ├── sound_service.py        # Switch acoustic synthesizer
│   └── screen_glow_service.py  # Layered click-through neon screen aura
├── ui/
│   ├── index.html              # Obsidian Telemetry UI (Geist, Space Grotesk, micro-sliders)
│   └── web_app.py              # Native pywebview window & bidirectional JS API bridge
├── tests/
│   └── test_suite.py           # Automated 6-phase verification test suite
├── install.ps1                 # Automated Windows installer & shortcut creator
├── launch.bat                  # 1-Click launcher
├── requirements.txt            # Python dependencies
└── run_app.py                  # Python entrypoint
```

---

## 🚀 Installation & Running

### Prerequisites
- Windows 10 or 11 (64-bit)
- Python 3.10+
- Microsoft Edge WebView2 Runtime (pre-installed on modern Windows 10/11)

### Setup
```powershell
# 1. Clone repository
git clone https://github.com/faijaleaqbal/apex-hub.git
cd apex-hub

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch application
python run_app.py
# or double click launch.bat
```

### Build Standalone Executable (.exe)
```powershell
pyinstaller -y --noconsole --onedir --name "ApexHub" --icon="assets\icon.ico" --add-data "assets;assets" --add-data "ui;ui" --collect-all webview run_app.py
```

Deploy locally and create Desktop/Start Menu shortcuts:
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

---

## 📜 License
MIT License. Built for pro gamers and productivity enthusiasts.
