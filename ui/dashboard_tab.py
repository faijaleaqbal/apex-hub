import customtkinter as ctk
from core.device_detector import device_detector
from core.config_manager import config_manager
from ui.theme import *

class DashboardTab(ctk.CTkFrame):
    def __init__(self, master, on_profile_change_cb=None):
        super().__init__(master, fg_color="transparent")
        self.on_profile_change_cb = on_profile_change_cb
        self.summary = device_detector.get_hardware_summary()
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text="⚡ Apex Hub Dashboard",
            font=(FONT_FAMILY, 24, "bold"),
            text_color=NEON_CYAN
        )
        header.pack(anchor="w", padx=20, pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text=f"System: {self.summary.get('system_board', 'MSI B550M')} | 2.4GHz Wireless Peripherals Connected",
            font=(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(anchor="w", padx=20, pady=(0, 15))

        # Two-column layout
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=5)
        container.grid_columnconfigure((0, 1), weight=1)

        # Left Column: Keyboard Card
        kb_card = ctk.CTkFrame(container, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        kb_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

        ctk.CTkLabel(
            kb_card,
            text="⌨️  Keyboard Detected",
            font=(FONT_FAMILY, 16, "bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", padx=15, pady=(15, 5))

        kb_name = ctk.CTkLabel(
            kb_card,
            text="Karnage Visage Tri-Mode",
            font=(FONT_FAMILY, 15, "bold"),
            text_color=NEON_CYAN
        )
        kb_name.pack(anchor="w", padx=15)

        kb_details = [
            ("Model:", "WLKM-054 (84-Key Mecha-Membrane)"),
            ("Connection:", "2.4GHz Wireless / Bluetooth / Type-C"),
            ("Rotary Knob:", "Volume Dial & Mode Selector"),
            ("Status:", "🟢 Active & Synced")
        ]
        for label, val in kb_details:
            row = ctk.CTkFrame(kb_card, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=2)
            ctk.CTkLabel(row, text=label, font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY, width=90, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=val, font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_PRIMARY).pack(side="left")

        # RGB Shortcut Guide inside Keyboard card
        guide_box = ctk.CTkFrame(kb_card, fg_color="#0A0E14", corner_radius=6, border_width=1, border_color="#1E2631")
        guide_box.pack(fill="x", padx=15, pady=(12, 15))

        ctk.CTkLabel(
            guide_box,
            text="💡 Hardware RGB Quick Guide:",
            font=(FONT_FAMILY, 11, "bold"),
            text_color=NEON_PURPLE
        ).pack(anchor="w", padx=10, pady=(8, 2))

        shortcuts = [
            ("Fn + Enter", "Cycle 15 Lighting Effects"),
            ("Fn + \\", "Switch 8 Solid Colours"),
            ("Fn + Backspace", "Toggle RGB On / Off"),
            ("Fn + Arrows", "Adjust Brightness & Speed")
        ]
        for key_comb, effect in shortcuts:
            s_row = ctk.CTkFrame(guide_box, fg_color="transparent")
            s_row.pack(fill="x", padx=10, pady=1)
            ctk.CTkLabel(s_row, text=key_comb, font=(FONT_FAMILY, 11, "bold"), text_color=TEXT_PRIMARY, width=110, anchor="w").pack(side="left")
            ctk.CTkLabel(s_row, text=f"→ {effect}", font=(FONT_FAMILY, 11), text_color=TEXT_SECONDARY).pack(side="left")

        # Right Column: Mouse Card
        mouse_card = ctk.CTkFrame(container, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        mouse_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)

        ctk.CTkLabel(
            mouse_card,
            text="🖱️  Mouse Detected",
            font=(FONT_FAMILY, 16, "bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            mouse_card,
            text="Arctic Fox Wireless Gaming Mouse",
            font=(FONT_FAMILY, 15, "bold"),
            text_color=NEON_CYAN
        ).pack(anchor="w", padx=15)

        mouse_details = [
            ("Receiver:", "2.4GHz USB Nano Dongle"),
            ("Chipset:", "OnMicro Electronics (VID_32C2)"),
            ("Lighting:", "Onboard Cycle / DPI Indicator"),
            ("Status:", "🟢 Active & Synced")
        ]
        for label, val in mouse_details:
            row = ctk.CTkFrame(mouse_card, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=2)
            ctk.CTkLabel(row, text=label, font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY, width=90, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=val, font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_PRIMARY).pack(side="left")

        # Mouse Hardware Guide inside Mouse card
        m_guide_box = ctk.CTkFrame(mouse_card, fg_color="#0A0E14", corner_radius=6, border_width=1, border_color="#1E2631")
        m_guide_box.pack(fill="x", padx=15, pady=(12, 15))

        ctk.CTkLabel(
            m_guide_box,
            text="💡 Arctic Fox Mouse Controls:",
            font=(FONT_FAMILY, 11, "bold"),
            text_color=NEON_PINK
        ).pack(anchor="w", padx=10, pady=(8, 2))

        m_shortcuts = [
            ("Hold DPI (3s)", "Toggle RGB Effect / Color"),
            ("Bottom Switch", "Power OFF / ON / LED ON"),
            ("App F6 Key", "Instant Auto-Clicker Trigger"),
            ("App F7 Key", "Sniper Precision Aim Mode")
        ]
        for key_comb, effect in m_shortcuts:
            s_row = ctk.CTkFrame(m_guide_box, fg_color="transparent")
            s_row.pack(fill="x", padx=10, pady=1)
            ctk.CTkLabel(s_row, text=key_comb, font=(FONT_FAMILY, 11, "bold"), text_color=TEXT_PRIMARY, width=110, anchor="w").pack(side="left")
            ctk.CTkLabel(s_row, text=f"→ {effect}", font=(FONT_FAMILY, 11), text_color=TEXT_SECONDARY).pack(side="left")

        # Bottom Card: Quick Profiles
        profile_card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        profile_card.pack(fill="x", padx=20, pady=(10, 20))

        ctk.CTkLabel(
            profile_card,
            text="🎯 Active Profile Presets",
            font=(FONT_FAMILY, 14, "bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", padx=15, pady=(12, 8))

        btn_row = ctk.CTkFrame(profile_card, fg_color="transparent")
        btn_row.pack(fill="x", padx=15, pady=(0, 15))

        profiles = ["Gaming / FPS", "Productivity / Office", "Default"]
        for p in profiles:
            btn = ctk.CTkButton(
                btn_row,
                text=p,
                font=(FONT_FAMILY, 12, "bold"),
                fg_color="#21262D",
                hover_color=ACCENT_BLUE,
                text_color=TEXT_PRIMARY,
                width=160,
                height=35,
                command=lambda name=p: self._on_preset_click(name)
            )
            btn.pack(side="left", padx=(0, 10))

    def _on_preset_click(self, name: str):
        config_manager.apply_preset(name)
        if self.on_profile_change_cb:
            self.on_profile_change_cb(name)
