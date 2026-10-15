import os
import subprocess
import threading
import time
import ctypes
from collections import deque
from pynput import keyboard
from pynput.keyboard import _win32, Key
from core.sound_service import sound_service
from core.screen_glow_service import screen_glow_service
from core.mouse_service import mouse_service

user32 = ctypes.windll.user32

# Win32 Virtual Keys
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3
VK_CAPITAL = 0x14
VK_NUMLOCK = 0x90
VK_SCROLL = 0x91
KEYEVENTF_KEYUP = 0x0002

def send_win32_vk(vk_code: int):
    user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.01)
    user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)

class CustomKeyListener(_win32.Listener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.win_lock = False

    def _handler(self, code, msg, lpdata):
        super()._handler(code, msg, lpdata)
        if self.win_lock:
            struct = ctypes.cast(lpdata, _win32.Listener._LPKBDLLHOOKSTRUCT).contents
            if struct.vkCode in (0x5B, 0x5C):  # Left / Right Windows Key
                self.suppress_event()

class KeyboardService:
    def __init__(self):
        self.lock = threading.Lock()
        self.listener = None
        self.controller = keyboard.Controller()
        
        # Remappings: { "source_key": { "type": "media|launch|text", "value": "..." } }
        self.remaps = {}
        
        # Windows Key Lock (WinLock)
        self.win_lock_enabled = False
        
        # Hotkeys
        self.sniper_hotkey = "F7"
        self.autoclicker_hotkey = "F6"
        self.suppress_remaps = False

        # Turbo Mode (Rapid Trigger repeat for designated key)
        self.turbo_enabled = False
        self.turbo_key = "space"
        self.turbo_rate = 20 # presses per second
        self.turbo_active = False
        self._turbo_thread = None
        self._turbo_stop_event = threading.Event()

        # Telemetry Stats
        self.total_keystrokes = 0
        self.key_timestamps = deque(maxlen=100)
        self.key_press_counts = {}

    def _normalize_key(self, key):
        if hasattr(key, 'char') and key.char:
            return key.char.lower()
        if hasattr(key, 'name') and key.name:
            return key.name.lower()
        return str(key).lower()

    def set_win_lock(self, enabled: bool):
        with self.lock:
            self.win_lock_enabled = bool(enabled)
            if self.listener and isinstance(self.listener, CustomKeyListener):
                self.listener.win_lock = self.win_lock_enabled

    def get_lock_states(self):
        """Returns hardware state of Caps, Num, and Scroll Lock"""
        return {
            "caps": bool(user32.GetKeyState(VK_CAPITAL) & 1),
            "num": bool(user32.GetKeyState(VK_NUMLOCK) & 1),
            "scroll": bool(user32.GetKeyState(VK_SCROLL) & 1),
            "win_lock": self.win_lock_enabled
        }

    # --- TURBO MODE (RAPID FIRE REPEAT) ---
    def set_turbo(self, enabled: bool, key_name: str = "space", rate: int = 20):
        with self.lock:
            self.turbo_enabled = bool(enabled)
            self.turbo_key = str(key_name).strip().lower()
            self.turbo_rate = max(5, min(50, int(rate)))

    def _start_turbo_firing(self):
        if self._turbo_thread and self._turbo_thread.is_alive():
            return
        self._turbo_stop_event.clear()
        self._turbo_thread = threading.Thread(target=self._turbo_loop, daemon=True)
        self._turbo_thread.start()

    def _turbo_loop(self):
        interval = 1.0 / max(1, self.turbo_rate)
        while not self._turbo_stop_event.is_set():
            self.suppress_remaps = True
            try:
                self.controller.tap(self.turbo_key)
            except Exception:
                pass
            self.suppress_remaps = False
            time.sleep(interval)

    def _stop_turbo_firing(self):
        self._turbo_stop_event.set()

    # --- TELEMETRY & HOOK ---
    def _on_press(self, key):
        key_name = self._normalize_key(key)

        # Telemetry tracking
        with self.lock:
            self.total_keystrokes += 1
            now = time.time()
            self.key_timestamps.append(now)
            self.key_press_counts[key_name] = self.key_press_counts.get(key_name, 0) + 1

        # 1. Sound FX trigger (non-blocking)
        sound_service.play_key_sound()

        # 2. Screen Ambient Glow trigger
        screen_glow_service.trigger_pulse()

        # 3. Check Turbo trigger
        if self.turbo_enabled and key_name == self.turbo_key:
            self._start_turbo_firing()

        # 4. Check Auto-Clicker Toggle Hotkey
        if key_name == self.autoclicker_hotkey.lower():
            mouse_service.toggle_autoclicker()
            return

        # 5. Check Sniper Mode Hotkey
        if key_name == self.sniper_hotkey.lower():
            mouse_service.toggle_sniper_mode()
            return

        # 6. Check Custom Remap Rules
        if key_name in self.remaps and not self.suppress_remaps:
            action = self.remaps[key_name]
            act_type = action.get("type")
            act_val = action.get("value")
            threading.Thread(target=self._execute_action, args=(act_type, act_val), daemon=True).start()

    def _on_release(self, key):
        key_name = self._normalize_key(key)
        if self.turbo_enabled and key_name == self.turbo_key:
            self._stop_turbo_firing()

    def get_stats(self):
        """Calculate rolling KPS and stats"""
        now = time.time()
        with self.lock:
            recent = [t for t in self.key_timestamps if now - t <= 1.0]
            kps = len(recent)
            top = sorted(self.key_press_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            return {
                "total": self.total_keystrokes,
                "kps": kps,
                "wpm": int(kps * 12), # standard estimation
                "top": top
            }

    def _execute_action(self, act_type: str, act_val: str):
        try:
            if act_type == "media":
                media_map = {
                    "vol_up": VK_VOLUME_UP,
                    "vol_down": VK_VOLUME_DOWN,
                    "mute": VK_VOLUME_MUTE,
                    "play_pause": VK_MEDIA_PLAY_PAUSE,
                    "next": VK_MEDIA_NEXT_TRACK,
                    "prev": VK_MEDIA_PREV_TRACK
                }
                if act_val in media_map:
                    send_win32_vk(media_map[act_val])

            elif act_type == "launch":
                # Quick launches
                launch_map = {
                    "steam": "start steam://",
                    "discord": "start discord://",
                    "spotify": "start spotify:",
                    "taskmgr": "taskmgr.exe",
                    "calc": "calc.exe",
                    "notepad": "notepad.exe",
                    "browser": "start https://google.com"
                }
                cmd = launch_map.get(act_val.lower(), act_val)
                subprocess.Popen(cmd, shell=True)

            elif act_type == "text":
                self.suppress_remaps = True
                self.controller.type(act_val)
                self.suppress_remaps = False

        except Exception:
            self.suppress_remaps = False

    def start_hook(self):
        with self.lock:
            if self.listener is None or not self.listener.is_alive():
                self.listener = CustomKeyListener(on_press=self._on_press, on_release=self._on_release)
                self.listener.win_lock = self.win_lock_enabled
                self.listener.start()

    def stop_hook(self):
        with self.lock:
            self._stop_turbo_firing()
            if self.listener and self.listener.is_alive():
                self.listener.stop()
                self.listener = None

    def add_remap(self, source_key: str, action_type: str, action_value: str):
        with self.lock:
            self.remaps[source_key.lower()] = {
                "type": action_type,
                "value": action_value
            }

    def remove_remap(self, source_key: str):
        with self.lock:
            self.remaps.pop(source_key.lower(), None)

keyboard_service = KeyboardService()
