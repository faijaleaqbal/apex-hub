import os
import threading
import customtkinter as ctk
from PIL import Image, ImageDraw
import pystray

from core.keyboard_service import keyboard_service
from core.mouse_service import mouse_service
from core.sound_service import sound_service
from core.screen_glow_service import screen_glow_service
from core.config_manager import config_manager

from ui.theme import *
from ui.dashboard_tab import DashboardTab
from ui.mouse_tab import MouseTab
from ui.keyboard_tab import KeyboardTab
from ui.sound_tab import SoundTab
from ui.rgb_glow_tab import RgbGlowTab

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Apex Hub - Peripheral Control Suite (Karnage & Arctic Fox)")
        self.geometry("1100x720")
        self.minsize(980, 640)
        self.configure(fg_color=BG_DARK)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Active Tab Tracking
        self.current_tab = "dashboard"
        self.nav_buttons = {}

        # Build Layout
        self._build_sidebar()
        self._build_content_area()

        # Initialize Background Services from Config
        self._init_services_from_config()

        # System Tray setup
        self.tray_icon = None
        self._setup_tray()

        # Window Close Protocol
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _init_services_from_config(self):
        cfg = config_manager.config
        
        # 1. Mouse speed
        m_cfg = cfg.get("mouse", {})
        if "speed" in m_cfg:
            mouse_service.set_mouse_speed(m_cfg["speed"])
        if "acceleration" in m_cfg:
            mouse_service.set_acceleration(m_cfg["acceleration"])
        if "autoclicker" in m_cfg:
            ac = m_cfg["autoclicker"]
            mouse_service.autoclicker_cps = ac.get("cps", 12)
            mouse_service.autoclicker_button = ac.get("button", "left")
            mouse_service.autoclicker_type = ac.get("type", "single")
            mouse_service.autoclicker_hotkey = ac.get("hotkey", "F6")
            keyboard_service.autoclicker_hotkey = ac.get("hotkey", "F6")

        # 2. Keyboard remaps
        kb_cfg = cfg.get("keyboard", {})
        for k, act in kb_cfg.get("remaps", {}).items():
            keyboard_service.add_remap(k, act.get("type"), act.get("value"))

        # 3. Sound
        s_cfg = cfg.get("sound", {})
        sound_service.set_enabled(s_cfg.get("enabled", True))
        sound_service.set_sound(s_cfg.get("current", "thock"))

        # 4. Glow
        g_cfg = cfg.get("glow", {})
        screen_glow_service.set_enabled(g_cfg.get("enabled", False))
        screen_glow_service.set_color(g_cfg.get("color", "#00F0FF"))

        # 5. Start Global Keyboard Hook
        keyboard_service.start_hook()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=CARD_BG, width=240, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand Logo / Title
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.pack(fill="x", padx=20, pady=(25, 20))

        ctk.CTkLabel(
            brand_frame,
            text="⚡ APEX HUB",
            font=(FONT_FAMILY, 20, "bold"),
            text_color=NEON_CYAN
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand_frame,
            text="Gaming Peripheral Suite v2.0",
            font=(FONT_FAMILY, 11),
            text_color=TEXT_MUTED
        ).pack(anchor="w")

        # Navigation Section
        nav_items = [
            ("dashboard", "⚡ Dashboard"),
            ("mouse", "🖱️ Mouse Controls"),
            ("keyboard", "⌨️ Keyboard Remap"),
            ("sound", "🎧 Mech Sound FX"),
            ("glow", "✨ Screen Ambient RGB")
        ]

        for tab_id, label in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                font=(FONT_FAMILY, 13, "bold"),
                anchor="w",
                fg_color="transparent",
                hover_color=CARD_HOVER,
                text_color=TEXT_SECONDARY,
                height=42,
                corner_radius=8,
                command=lambda t=tab_id: self.show_tab(t)
            )
            btn.pack(fill="x", padx=15, pady=3)
            self.nav_buttons[tab_id] = btn

        # Spacer
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)

        # Footer Card in Sidebar
        footer = ctk.CTkFrame(self.sidebar, fg_color="#0A0E14", corner_radius=8, border_width=1, border_color="#1E2631")
        footer.pack(fill="x", padx=15, pady=15)

        self.profile_badge = ctk.CTkLabel(
            footer,
            text=f"Profile: {config_manager.config.get('profile', 'Default')}",
            font=(FONT_FAMILY, 11, "bold"),
            text_color=NEON_PURPLE
        )
        self.profile_badge.pack(anchor="w", padx=10, pady=(8, 2))

        ctk.CTkLabel(
            footer,
            text="🟢 Engine: Active (Low-Latency)",
            font=(FONT_FAMILY, 10),
            text_color=SUCCESS_GREEN
        ).pack(anchor="w", padx=10, pady=(0, 8))

    def _build_content_area(self):
        self.content_frame = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Initialize Tabs
        self.tabs = {
            "dashboard": DashboardTab(self.content_frame, on_profile_change_cb=self._on_profile_change),
            "mouse": MouseTab(self.content_frame),
            "keyboard": KeyboardTab(self.content_frame),
            "sound": SoundTab(self.content_frame),
            "glow": RgbGlowTab(self.content_frame)
        }

        # Show Dashboard initially
        self.show_tab("dashboard")

    def show_tab(self, tab_id: str):
        self.current_tab = tab_id
        for tid, tab in self.tabs.items():
            if tid == tab_id:
                tab.pack(fill="both", expand=True)
            else:
                tab.pack_forget()

        # Update button highlights
        for tid, btn in self.nav_buttons.items():
            if tid == tab_id:
                btn.configure(fg_color="#1F2937", text_color=NEON_CYAN)
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_SECONDARY)

    def _on_profile_change(self, profile_name: str):
        self.profile_badge.configure(text=f"Profile: {profile_name}")
        # Refresh mouse sliders
        self.tabs["mouse"].refresh_from_system()

    def _setup_tray(self):
        # Generate a small icon for system tray
        img = Image.new('RGB', (64, 64), color=(13, 17, 23))
        draw = ImageDraw.Draw(img)
        draw.ellipse((8, 8, 56, 56), fill=(0, 240, 255))
        draw.ellipse((20, 20, 44, 44), fill=(13, 17, 23))

        menu = pystray.Menu(
            pystray.MenuItem("Open Apex Hub", self._restore_from_tray, default=True),
            pystray.MenuItem("Exit", self._exit_app)
        )
        self.tray_icon = pystray.Icon("ApexHub", img, "Apex Hub (Gaming Suite)", menu)

    def _minimize_to_tray(self):
        self.withdraw()
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def _restore_from_tray(self, icon=None, item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        self.after(0, self.deiconify)

    def _on_close(self):
        # Minimize to tray or quit cleanly
        self._exit_app()

    def _exit_app(self, icon=None, item=None):
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except Exception:
                pass
        keyboard_service.stop_hook()
        mouse_service.stop_autoclicker()
        screen_glow_service.stop_overlay()
        self.destroy()
        os._exit(0)
