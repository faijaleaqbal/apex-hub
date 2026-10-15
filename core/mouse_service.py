import ctypes
import threading
import time

user32 = ctypes.windll.user32

# Win32 Constants
SPI_GETMOUSESPEED = 0x0070
SPI_SETMOUSESPEED = 0x0071
SPI_GETMOUSE = 0x0003
SPI_SETMOUSE = 0x0004
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040

# Windows 1-20 sensitivity multipliers
SPEED_MULTIPLIERS = {
    1: 0.03125, 2: 0.0625, 3: 0.125, 4: 0.25, 5: 0.375,
    6: 0.5, 7: 0.625, 8: 0.75, 9: 0.875, 10: 1.0,
    11: 1.25, 12: 1.5, 13: 1.75, 14: 2.0, 15: 2.25,
    16: 2.5, 17: 2.75, 18: 3.0, 19: 3.25, 20: 3.5
}

class MouseService:
    def __init__(self):
        self.lock = threading.Lock()
        self.original_speed = self.get_mouse_speed()
        self.is_sniper_active = False
        self.sniper_speed = 3 # Configurable sniper limit (1-10)
        
        # Hardware DPI stages for Arctic Fox (800, 1200, 1600, 2400, 3200)
        self.dpi_stage = 1600
        
        # Auto clicker states
        self.autoclicker_running = False
        self.autoclicker_cps = 12
        self.autoclicker_button = 'left' # 'left', 'right', 'middle'
        self.autoclicker_type = 'single'  # 'single', 'double'
        self.autoclicker_hotkey = 'F6'
        self._autoclicker_thread = None
        self._autoclicker_stop_event = threading.Event()

    # --- POINTER SPEED ---
    def get_mouse_speed(self) -> int:
        speed = ctypes.c_int()
        user32.SystemParametersInfoW(SPI_GETMOUSESPEED, 0, ctypes.byref(speed), 0)
        return speed.value if speed.value > 0 else 10

    def set_mouse_speed(self, speed: int, persistent: bool = True):
        speed = max(1, min(20, int(speed)))
        flags = (SPIF_UPDATEINIFILE | SPIF_SENDCHANGE) if persistent else SPIF_UPDATEINIFILE
        user32.SystemParametersInfoW(
            SPI_SETMOUSESPEED,
            0,
            ctypes.c_void_p(speed),
            flags
        )

    def get_effective_dpi(self, base_dpi: int = None, speed: int = None) -> int:
        if base_dpi is None:
            base_dpi = self.dpi_stage
        if speed is None:
            speed = self.get_mouse_speed()
        mult = SPEED_MULTIPLIERS.get(speed, 1.0)
        return int(round(base_dpi * mult))

    def set_dpi_stage(self, stage_dpi: int):
        self.dpi_stage = max(200, min(12000, int(stage_dpi)))

    # --- BUTTON SWAP ---
    def set_buttons_swapped(self, swapped: bool):
        user32.SwapMouseButton(swapped)

    # --- ACCELERATION ---
    def get_acceleration(self) -> bool:
        mouse_params = (ctypes.c_int * 3)()
        user32.SystemParametersInfoW(SPI_GETMOUSE, 0, mouse_params, 0)
        return bool(mouse_params[2])

    def set_acceleration(self, enabled: bool):
        mouse_params = (ctypes.c_int * 3)()
        user32.SystemParametersInfoW(SPI_GETMOUSE, 0, mouse_params, 0)
        mouse_params[2] = 1 if enabled else 0
        user32.SystemParametersInfoW(SPI_SETMOUSE, 0, mouse_params, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

    # --- SNIPER MODE ---
    def set_sniper_speed(self, speed: int):
        self.sniper_speed = max(1, min(10, int(speed)))

    def toggle_sniper_mode(self, active: bool = None):
        with self.lock:
            if active is None:
                self.is_sniper_active = not self.is_sniper_active
            else:
                self.is_sniper_active = active

            if self.is_sniper_active:
                self.original_speed = self.get_mouse_speed()
                self.set_mouse_speed(self.sniper_speed, persistent=False)
            else:
                self.set_mouse_speed(self.original_speed, persistent=False)
        return self.is_sniper_active

    # --- AUTO CLICKER ---
    def _click_once(self):
        btn = self.autoclicker_button.lower()
        if btn == 'left':
            down, up = MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
        elif btn == 'right':
            down, up = MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
        else:
            down, up = MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP

        user32.mouse_event(down, 0, 0, 0, 0)
        time.sleep(0.002)
        user32.mouse_event(up, 0, 0, 0, 0)

        if self.autoclicker_type == 'double':
            time.sleep(0.02)
            user32.mouse_event(down, 0, 0, 0, 0)
            time.sleep(0.002)
            user32.mouse_event(up, 0, 0, 0, 0)

    def _autoclicker_loop(self):
        while not self._autoclicker_stop_event.is_set():
            self._click_once()
            interval = 1.0 / max(1, self.autoclicker_cps)
            end_time = time.time() + interval
            while time.time() < end_time:
                if self._autoclicker_stop_event.is_set():
                    break
                time.sleep(0.002)

    def start_autoclicker(self):
        with self.lock:
            if self.autoclicker_running:
                return
            self.autoclicker_running = True
            self._autoclicker_stop_event.clear()
            self._autoclicker_thread = threading.Thread(target=self._autoclicker_loop, daemon=True)
            self._autoclicker_thread.start()

    def stop_autoclicker(self):
        with self.lock:
            if not self.autoclicker_running:
                return
            self.autoclicker_running = False
            self._autoclicker_stop_event.set()

    def toggle_autoclicker(self):
        if self.autoclicker_running:
            self.stop_autoclicker()
            return False
        else:
            self.start_autoclicker()
            return True

mouse_service = MouseService()
