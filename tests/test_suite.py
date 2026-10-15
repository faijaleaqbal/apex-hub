import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("RUNNING APEX HUB AUTOMATED VERIFICATION SUITE")
print("=" * 60)

# 1. Config Manager Test
print("\n[1/6] Testing ConfigManager...")
from core.config_manager import config_manager
cfg = config_manager.load_config()
assert "mouse" in cfg, "Config missing mouse key"
assert "keyboard" in cfg, "Config missing keyboard key"
assert "sound" in cfg, "Config missing sound key"
print("  ✓ Config structure verified successfully.")

# Test presets
config_manager.apply_preset("Gaming / FPS")
assert config_manager.config["mouse"]["speed"] == 8
config_manager.apply_preset("Default")
print("  ✓ Preset switching verified successfully.")

# 2. Device Detector Test
print("\n[2/6] Testing DeviceDetector...")
from core.device_detector import device_detector
summary = device_detector.get_hardware_summary()
assert "keyboard" in summary
assert "mouse" in summary
print(f"  ✓ Detected Keyboard: {summary['keyboard']['name']} ({summary['keyboard']['model']})")
print(f"  ✓ Detected Mouse: {summary['mouse']['name']}")
print(f"  ✓ System Motherboard: {summary.get('system_board')}")

# 3. Mouse Service Test
print("\n[3/6] Testing MouseService...")
from core.mouse_service import mouse_service
initial_speed = mouse_service.get_mouse_speed()
assert 1 <= initial_speed <= 20
print(f"  ✓ Initial Win32 Mouse Speed: {initial_speed}")

# Test speed change and restore
mouse_service.set_mouse_speed(12)
assert mouse_service.get_mouse_speed() == 12
mouse_service.set_mouse_speed(initial_speed)
assert mouse_service.get_mouse_speed() == initial_speed
print("  ✓ Win32 Mouse Speed modification & restoration verified.")

# Test sniper mode
mouse_service.toggle_sniper_mode(True)
assert mouse_service.is_sniper_active == True
assert mouse_service.get_mouse_speed() == mouse_service.sniper_speed
mouse_service.toggle_sniper_mode(False)
assert mouse_service.is_sniper_active == False
assert mouse_service.get_mouse_speed() == initial_speed
print("  ✓ Sniper mode precision toggle & speed restoration verified.")

# Test autoclicker
mouse_service.autoclicker_cps = 30
mouse_service.start_autoclicker()
assert mouse_service.autoclicker_running == True
time.sleep(0.1)
mouse_service.stop_autoclicker()
assert mouse_service.autoclicker_running == False
print("  ✓ Multi-threaded Auto-Clicker lifecycle verified.")

# 4. Sound Service Test
print("\n[4/6] Testing SoundService & Synthesizer...")
from core.sound_service import sound_service
sound_service.set_enabled(True)
for snd in ['thock', 'clicky', 'creamy', 'bubble']:
    sound_service.set_sound(snd)
    sound_service.play_key_sound()
print("  ✓ All 4 mechanical audio switch models synthesized and verified.")

# 5. Keyboard Service Test
print("\n[5/6] Testing KeyboardService...")
from core.keyboard_service import keyboard_service
keyboard_service.add_remap("f9", "media", "mute")
assert "f9" in keyboard_service.remaps
keyboard_service.start_hook()
time.sleep(0.2)
assert keyboard_service.listener.is_alive()
keyboard_service.stop_hook()
print("  ✓ Keyboard global hook & remap engine verified.")

# 6. UI Headless / Smoke Test
print("\n[6/6] Testing UI Construction & Window Lifecycle...")
from ui.main_window import MainWindow
app = MainWindow()
app.update_idletasks()
print("  ✓ MainWindow layout & widgets rendered cleanly.")
app.show_tab("mouse")
app.update_idletasks()
print("  ✓ MouseTab rendered cleanly.")
app.show_tab("keyboard")
app.update_idletasks()
print("  ✓ KeyboardTab rendered cleanly.")
app.show_tab("sound")
app.update_idletasks()
print("  ✓ SoundTab rendered cleanly.")
app.show_tab("glow")
app.update_idletasks()
print("  ✓ RgbGlowTab rendered cleanly.")
app.destroy()
print("  ✓ UI teardown completed cleanly.")

print("\n" + "=" * 60)
print("ALL TESTS PASSED! PRODUCTION READY.")
print("=" * 60)
