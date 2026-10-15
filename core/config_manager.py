import os
import json
import shutil

APPDATA_DIR = os.getenv('APPDATA')
if not APPDATA_DIR:
    APPDATA_DIR = os.path.expanduser('~')

CONFIG_DIR = os.path.join(APPDATA_DIR, 'ApexHub')
os.makedirs(CONFIG_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

DEFAULT_CONFIG = {
    "profile": "Default",
    "close_to_tray": True,
    "mouse": {
        "speed": 10,
        "acceleration": True,
        "swap_buttons": False,
        "sniper_speed": 3,
        "sniper_hotkey": "F7",
        "dpi_stage": 1600,
        "autoclicker": {
            "cps": 12,
            "button": "left",
            "type": "single",
            "hotkey": "F6"
        }
    },
    "keyboard": {
        "win_lock": False,
        "turbo": {
            "enabled": False,
            "key": "space",
            "rate": 20
        },
        "remaps": {
            "f8": {"type": "launch", "value": "steam"},
            "f9": {"type": "media", "value": "mute"},
            "f10": {"type": "media", "value": "vol_down"},
            "f11": {"type": "media", "value": "vol_up"},
            "f12": {"type": "media", "value": "play_pause"}
        }
    },
    "sound": {
        "enabled": False,
        "current": "thock"
    },
    "glow": {
        "enabled": False,
        "color": "#00D2B4"
    }
}

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self) -> dict:
        # 1. Check permanent user AppData location
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    merged = DEFAULT_CONFIG.copy()
                    # Deep merge mouse
                    if "mouse" in data:
                        merged["mouse"].update(data["mouse"])
                    # Deep merge keyboard
                    if "keyboard" in data:
                        merged["keyboard"].update(data["keyboard"])
                    if "sound" in data:
                        merged["sound"].update(data["sound"])
                    if "glow" in data:
                        merged["glow"].update(data["glow"])
                    if "profile" in data:
                        merged["profile"] = data["profile"]
                    return merged
            except Exception:
                pass

        # 2. Check local fallback in current directory
        local_cfg = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        if os.path.exists(local_cfg):
            try:
                with open(local_cfg, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    merged = DEFAULT_CONFIG.copy()
                    merged.update(data)
                    self.save_config(merged)
                    return merged
            except Exception:
                pass

        # Save default to AppData
        self.save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    def save_config(self, new_config: dict = None):
        if new_config:
            self.config = new_config
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception:
            pass

    def apply_preset(self, preset_name: str):
        if preset_name == "Gaming / FPS":
            self.config["mouse"]["speed"] = 8
            self.config["mouse"]["dpi_stage"] = 1600
            self.config["mouse"]["acceleration"] = False
            self.config["mouse"]["sniper_speed"] = 2
            self.config["mouse"]["autoclicker"]["cps"] = 20
            self.config["keyboard"]["win_lock"] = True
            self.config["sound"]["enabled"] = False
            self.config["sound"]["current"] = "clicky"
            self.config["glow"]["enabled"] = True
            self.config["glow"]["color"] = "#FF0055"
        elif preset_name == "Productivity / Office":
            self.config["mouse"]["speed"] = 10
            self.config["mouse"]["dpi_stage"] = 1200
            self.config["mouse"]["acceleration"] = True
            self.config["keyboard"]["win_lock"] = False
            self.config["sound"]["enabled"] = False
            self.config["sound"]["current"] = "creamy"
            self.config["glow"]["enabled"] = False
        else: # Default
            self.config = DEFAULT_CONFIG.copy()

        self.save_config()
        return self.config

config_manager = ConfigManager()
