import tkinter as tk
import ctypes
import threading
import time

user32 = ctypes.windll.user32
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

class ScreenGlowService:
    def __init__(self):
        self.enabled = False
        self.color = "#00F0FF" # Cyberpunk Neon Cyan
        self.glow_window = None
        self.canvas = None
        self._thread = None
        self.lock = threading.Lock()
        self._flash_trigger = threading.Event()
        self._stop_event = threading.Event()

    def _create_overlay(self):
        try:
            root = tk.Tk()
            self.glow_window = root
            root.title("ApexGlowOverlay")
            root.attributes("-topmost", True)
            root.attributes("-alpha", 0.0) # start invisible
            root.overrideredirect(True)

            w = root.winfo_screenwidth()
            h = root.winfo_screenheight()
            root.geometry(f"{w}x{h}+0+0")
            root.config(bg="black")

            # Make window click-through using Win32 API
            hwnd = user32.GetParent(root.winfo_id())
            if not hwnd:
                hwnd = root.winfo_id()
            style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT)

            # Canvas for glowing borders
            canvas = tk.Canvas(root, width=w, height=h, bg="black", highlightthickness=0)
            canvas.pack(fill="both", expand=True)
            self.canvas = canvas

            # Border rectangles
            border_thickness = 8
            self.borders = [
                canvas.create_rectangle(0, 0, w, border_thickness, fill=self.color, outline=""), # top
                canvas.create_rectangle(0, h-border_thickness, w, h, fill=self.color, outline=""), # bottom
                canvas.create_rectangle(0, 0, border_thickness, h, fill=self.color, outline=""), # left
                canvas.create_rectangle(w-border_thickness, 0, w, h, fill=self.color, outline="") # right
            ]

            # Periodic check for triggers
            def poll_flash():
                if self._stop_event.is_set():
                    root.destroy()
                    return
                if self._flash_trigger.is_set():
                    self._flash_trigger.clear()
                    # Pulse animation
                    for alpha in [0.85, 0.6, 0.4, 0.2, 0.0]:
                        if self._stop_event.is_set():
                            break
                        try:
                            root.attributes("-alpha", alpha)
                            root.update()
                            time.sleep(0.03)
                        except Exception:
                            pass
                root.after(30, poll_flash)

            root.after(30, poll_flash)
            root.mainloop()
        except Exception:
            pass

    def start_overlay(self):
        with self.lock:
            if self._thread and self._thread.is_alive():
                return
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._create_overlay, daemon=True)
            self._thread.start()

    def stop_overlay(self):
        with self.lock:
            self._stop_event.set()

    def trigger_pulse(self):
        if self.enabled:
            self._flash_trigger.set()

    def set_enabled(self, enabled: bool):
        self.enabled = enabled
        if enabled:
            self.start_overlay()
        else:
            self.stop_overlay()

    def set_color(self, hex_color: str):
        self.color = hex_color
        if self.canvas and self.glow_window:
            try:
                for b in self.borders:
                    self.canvas.itemconfig(b, fill=hex_color)
            except Exception:
                pass

screen_glow_service = ScreenGlowService()
