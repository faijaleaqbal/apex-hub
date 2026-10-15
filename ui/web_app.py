import os
import sys
import socket
import threading
import webview

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.mouse_service import mouse_service
from core.keyboard_service import keyboard_service
from core.sound_service import sound_service
from core.screen_glow_service import screen_glow_service
from core.config_manager import config_manager
from core.device_detector import device_detector

IPC_PORT = 39842

class ApexApi:
    def __init__(self, window=None):
        self.window = window
        self.allow_exit = False

    def set_window(self, window):
        self.window = window

    def get_initial_state(self):
        cfg = config_manager.config
        return {
            "speed": mouse_service.get_mouse_speed(),
            "acceleration": mouse_service.get_acceleration(),
            "sniper": mouse_service.is_sniper_active,
            "sniper_speed": mouse_service.sniper_speed,
            "dpi_stage": mouse_service.dpi_stage,
            "effective_dpi": mouse_service.get_effective_dpi(),
            "autoclicker_cps": mouse_service.autoclicker_cps,
            "autoclicker_button": mouse_service.autoclicker_button,
            "sound": sound_service.current_sound,
            "sound_enabled": sound_service.enabled,
            "glow_enabled": screen_glow_service.enabled,
            "glow_color": screen_glow_service.color,
            "win_lock": keyboard_service.win_lock_enabled,
            "turbo_enabled": keyboard_service.turbo_enabled,
            "turbo_key": keyboard_service.turbo_key,
            "turbo_rate": keyboard_service.turbo_rate,
            "profile": cfg.get("profile", "Gaming / FPS")
        }

    # --- MOUSE APIS ---
    def set_mouse_speed(self, speed, persistent=True):
        sp = int(speed)
        mouse_service.set_mouse_speed(sp, persistent=bool(persistent))
        # Always update memory and save to permanent AppData config
        cfg = config_manager.config
        if "mouse" not in cfg:
            cfg["mouse"] = {}
        cfg["mouse"]["speed"] = sp
        config_manager.save_config()
        return {
            "speed": sp,
            "effective_dpi": mouse_service.get_effective_dpi(speed=sp)
        }

    def set_dpi_stage(self, stage_dpi):
        stage = int(stage_dpi)
        mouse_service.set_dpi_stage(stage)
        cfg = config_manager.config
        if "mouse" not in cfg:
            cfg["mouse"] = {}
        cfg["mouse"]["dpi_stage"] = stage
        config_manager.save_config()
        return {
            "dpi_stage": stage,
            "effective_dpi": mouse_service.get_effective_dpi(base_dpi=stage)
        }

    def set_sniper_speed(self, speed):
        sp = max(1, min(10, int(speed)))
        mouse_service.set_sniper_speed(sp)
        cfg = config_manager.config
        if "mouse" not in cfg:
            cfg["mouse"] = {}
        cfg["mouse"]["sniper_speed"] = sp
        config_manager.save_config()
        return sp

    def set_acceleration(self, enabled):
        mouse_service.set_acceleration(bool(enabled))
        cfg = config_manager.config
        if "mouse" not in cfg:
            cfg["mouse"] = {}
        cfg["mouse"]["acceleration"] = bool(enabled)
        config_manager.save_config()

    def set_buttons_swapped(self, swapped):
        mouse_service.set_buttons_swapped(bool(swapped))
        cfg = config_manager.config
        if "mouse" not in cfg:
            cfg["mouse"] = {}
        cfg["mouse"]["swap_buttons"] = bool(swapped)
        config_manager.save_config()

    def toggle_sniper(self):
        return mouse_service.toggle_sniper_mode()

    def toggle_autoclicker(self):
        return mouse_service.toggle_autoclicker()

    def set_autoclicker_cps(self, cps):
        mouse_service.autoclicker_cps = max(1, min(100, int(cps)))
        cfg = config_manager.config
        if "mouse" in cfg and "autoclicker" in cfg["mouse"]:
            cfg["mouse"]["autoclicker"]["cps"] = mouse_service.autoclicker_cps
            config_manager.save_config()

    def set_autoclicker_button(self, btn):
        mouse_service.autoclicker_button = str(btn).lower()
        cfg = config_manager.config
        if "mouse" in cfg and "autoclicker" in cfg["mouse"]:
            cfg["mouse"]["autoclicker"]["button"] = mouse_service.autoclicker_button
            config_manager.save_config()

    # --- KEYBOARD APIS ---
    def set_win_lock(self, enabled):
        keyboard_service.set_win_lock(bool(enabled))
        cfg = config_manager.config
        if "keyboard" not in cfg:
            cfg["keyboard"] = {}
        cfg["keyboard"]["win_lock"] = bool(enabled)
        config_manager.save_config()
        return keyboard_service.win_lock_enabled

    def set_turbo(self, enabled, key_name="space", rate=20):
        keyboard_service.set_turbo(bool(enabled), key_name, int(rate))
        cfg = config_manager.config
        if "keyboard" not in cfg:
            cfg["keyboard"] = {}
        cfg["keyboard"]["turbo"] = {
            "enabled": bool(enabled),
            "key": str(key_name),
            "rate": int(rate)
        }
        config_manager.save_config()
        return {
            "enabled": keyboard_service.turbo_enabled,
            "key": keyboard_service.turbo_key,
            "rate": keyboard_service.turbo_rate
        }

    def get_keyboard_stats(self):
        return keyboard_service.get_stats()

    def get_lock_states(self):
        return keyboard_service.get_lock_states()

    def add_remap(self, key, act_type, act_val):
        key = str(key).strip().lower()
        keyboard_service.add_remap(key, str(act_type), str(act_val))
        cfg = config_manager.config
        if "keyboard" not in cfg:
            cfg["keyboard"] = {"remaps": {}}
        cfg["keyboard"]["remaps"][key] = {"type": str(act_type), "value": str(act_val)}
        config_manager.save_config()
        return True

    def remove_remap(self, key):
        key = str(key).strip().lower()
        keyboard_service.remove_remap(key)
        cfg = config_manager.config
        if "keyboard" in cfg and "remaps" in cfg["keyboard"]:
            cfg["keyboard"]["remaps"].pop(key, None)
            config_manager.save_config()
        return True

    def get_remaps(self):
        return keyboard_service.remaps

    # --- SOUND APIS ---
    def set_sound(self, sound_name):
        sound_service.set_sound(str(sound_name))
        cfg = config_manager.config
        if "sound" not in cfg:
            cfg["sound"] = {}
        cfg["sound"]["current"] = str(sound_name)
        config_manager.save_config()

    def toggle_sound(self, enabled):
        sound_service.set_enabled(bool(enabled))
        cfg = config_manager.config
        if "sound" not in cfg:
            cfg["sound"] = {}
        cfg["sound"]["enabled"] = bool(enabled)
        config_manager.save_config()

    def play_test_sound(self, sound_name=None):
        if sound_name:
            old = sound_service.current_sound
            sound_service.set_sound(str(sound_name))
            old_en = sound_service.enabled
            sound_service.set_enabled(True)
            sound_service.play_key_sound()
            sound_service.set_sound(old)
            sound_service.set_enabled(old_en)
        else:
            sound_service.play_key_sound()

    # --- GLOW APIS ---
    def set_glow_enabled(self, enabled):
        screen_glow_service.set_enabled(bool(enabled))
        cfg = config_manager.config
        if "glow" not in cfg:
            cfg["glow"] = {}
        cfg["glow"]["enabled"] = bool(enabled)
        config_manager.save_config()

    def set_glow_color(self, hex_color):
        screen_glow_service.set_color(str(hex_color))
        cfg = config_manager.config
        if "glow" not in cfg:
            cfg["glow"] = {}
        cfg["glow"]["color"] = str(hex_color)
        config_manager.save_config()

    def trigger_glow_test(self):
        old = screen_glow_service.enabled
        screen_glow_service.set_enabled(True)
        screen_glow_service.trigger_pulse()
        if not old:
            pass

    def apply_preset(self, preset_name):
        return config_manager.apply_preset(str(preset_name))

    def exit_app(self):
        """Completely exit the application"""
        self.allow_exit = True
        config_manager.save_config()
        keyboard_service.stop_hook()
        mouse_service.stop_autoclicker()
        screen_glow_service.stop_overlay()
        if self.window:
            self.window.destroy()
        os._exit(0)

def check_single_instance():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('127.0.0.1', IPC_PORT))
        return s, True
    except Exception:
        # Already running: signal existing instance to show its window
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', IPC_PORT))
            client.sendall(b'SHOW')
            client.close()
        except Exception:
            pass
        return None, False

def start_ipc_server(sock, window):
    sock.listen(5)
    def loop():
        while True:
            try:
                conn, _ = sock.accept()
                data = conn.recv(1024)
                if data == b'SHOW':
                    window.show()
                    window.restore()
                conn.close()
            except Exception:
                break
    t = threading.Thread(target=loop, daemon=True)
    t.start()

def launch_web_gui():
    # 1. Single Instance Check
    ipc_sock, is_primary = check_single_instance()
    if not is_primary:
        # Already running and pinged; exit this second process
        sys.exit(0)

    # 2. Start global low-level hooks
    keyboard_service.start_hook()

    # 3. Load & Apply Saved Settings from %APPDATA%/ApexHub/config.json
    cfg = config_manager.config
    m_cfg = cfg.get("mouse", {})
    if "speed" in m_cfg:
        mouse_service.set_mouse_speed(m_cfg["speed"], persistent=True)
    if "dpi_stage" in m_cfg:
        mouse_service.set_dpi_stage(m_cfg["dpi_stage"])
    if "sniper_speed" in m_cfg:
        mouse_service.set_sniper_speed(m_cfg["sniper_speed"])
    if "acceleration" in m_cfg:
        mouse_service.set_acceleration(m_cfg["acceleration"])
    if "swap_buttons" in m_cfg:
        mouse_service.set_buttons_swapped(m_cfg["swap_buttons"])
    if "autoclicker" in m_cfg:
        ac = m_cfg["autoclicker"]
        mouse_service.autoclicker_cps = ac.get("cps", 12)
        mouse_service.autoclicker_button = ac.get("button", "left")

    kb_cfg = cfg.get("keyboard", {})
    if "win_lock" in kb_cfg:
        keyboard_service.set_win_lock(kb_cfg["win_lock"])
    if "turbo" in kb_cfg:
        t = kb_cfg["turbo"]
        keyboard_service.set_turbo(t.get("enabled", False), t.get("key", "space"), t.get("rate", 20))
    for k, act in kb_cfg.get("remaps", {}).items():
        keyboard_service.add_remap(k, act.get("type"), act.get("value"))

    s_cfg = cfg.get("sound", {})
    sound_service.set_enabled(s_cfg.get("enabled", False))
    sound_service.set_sound(s_cfg.get("current", "thock"))

    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

    api = ApexApi()
    window = webview.create_window(
        title="Apex Hub - Gaming Peripheral Suite",
        url=html_path,
        js_api=api,
        width=1240,
        height=830,
        min_size=(1050, 700),
        background_color="#121316"
    )
    api.set_window(window)

    # Start IPC server so secondary launches bring this window forward
    start_ipc_server(ipc_sock, window)

    def on_closing():
        config_manager.save_config()
        if api.allow_exit:
            return True
        # Keep hooks, WinLock, and auto-clicker running in background!
        window.hide()
        return False

    def on_closed():
        config_manager.save_config()
        keyboard_service.stop_hook()
        mouse_service.stop_autoclicker()
        screen_glow_service.stop_overlay()
        os._exit(0)

    window.events.closing += on_closing
    window.events.closed += on_closed
    webview.start(debug=False)

if __name__ == "__main__":
    launch_web_gui()
