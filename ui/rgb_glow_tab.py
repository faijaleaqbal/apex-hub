import customtkinter as ctk
from core.screen_glow_service import screen_glow_service
from core.config_manager import config_manager
from ui.theme import *

class RgbGlowTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text="✨ Screen Ambient RGB Glow",
            font=(FONT_FAMILY, 24, "bold"),
            text_color=NEON_CYAN
        )
        header.pack(anchor="w", padx=20, pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Brings the missing RGB experience right onto your monitor with ultra-smooth screen edge lighting.",
            font=(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(anchor="w", padx=20, pady=(0, 15))

        scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=10, pady=0)

        # Main Toggle Card
        main_card = ctk.CTkFrame(scrollable, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        main_card.pack(fill="x", padx=10, pady=(0, 15))

        top_row = ctk.CTkFrame(main_card, fg_color="transparent")
        top_row.pack(fill="x", padx=15, pady=(15, 15))

        ctk.CTkLabel(top_row, text="🖥️ Ambient Screen Edge Lighting", font=(FONT_FAMILY, 15, "bold"), text_color=TEXT_PRIMARY).pack(side="left")

        self.glow_switch = ctk.CTkSwitch(
            top_row,
            text="Enable Keystroke Glow Pulse",
            font=(FONT_FAMILY, 13, "bold"),
            progress_color=NEON_CYAN,
            command=self._on_toggle_glow
        )
        if screen_glow_service.enabled:
            self.glow_switch.select()
        else:
            self.glow_switch.deselect()
        self.glow_switch.pack(side="right")

        # Color Selector Card
        color_card = ctk.CTkFrame(scrollable, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        color_card.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(color_card, text="🎨 Choose Ambient Neon Aura", font=(FONT_FAMILY, 15, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w", padx=15, pady=(15, 10))

        palettes = [
            ("#00F0FF", "Cyber Cyan", "Futuristic neon blue glow"),
            ("#FF0055", "Crimson Red", "High-octane aggressive gaming aura"),
            ("#BD00FF", "Electric Violet", "Deep royal cyberpunk violet"),
            ("#00FF7F", "Toxic Lime", "Vibrant esports green"),
            ("#FFB700", "Solar Amber", "Warm golden glow"),
            ("#FFFFFF", "Pure White", "Minimalist studio backlight")
        ]

        grid = ctk.CTkFrame(color_card, fg_color="transparent")
        grid.pack(fill="x", padx=15, pady=(0, 15))
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        for i, (hex_code, name, desc) in enumerate(palettes):
            row_idx = i // 3
            col_idx = i % 3

            cell = ctk.CTkFrame(grid, fg_color="#1A202C", corner_radius=8, border_width=1, border_color="#2D3748")
            cell.grid(row=row_idx, column=col_idx, sticky="nsew", padx=5, pady=5)

            badge = ctk.CTkLabel(cell, text="  ", fg_color=hex_code, width=20, height=20, corner_radius=4)
            badge.pack(side="left", padx=(10, 5), pady=10)

            btn = ctk.CTkButton(
                cell,
                text=name,
                font=(FONT_FAMILY, 12, "bold"),
                fg_color="transparent",
                hover_color="#283141",
                text_color=TEXT_PRIMARY,
                anchor="w",
                command=lambda h=hex_code: self._set_color(h)
            )
            btn.pack(side="left", fill="x", expand=True)

        # Flash Test Bar
        bar = ctk.CTkFrame(scrollable, fg_color="#0A0E14", corner_radius=8, border_width=1, border_color="#1E2631")
        bar.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(
            bar,
            text="💡 Completely transparent and click-through — never interrupts clicks in games or apps!",
            font=(FONT_FAMILY, 12),
            text_color=NEON_PURPLE
        ).pack(side="left", padx=15, pady=12)

        test_pulse_btn = ctk.CTkButton(
            bar,
            text="⚡ Test Screen Glow Pulse",
            font=(FONT_FAMILY, 12, "bold"),
            fg_color=NEON_PINK,
            hover_color="#ff3388",
            command=self._test_pulse
        )
        test_pulse_btn.pack(side="right", padx=15, pady=12)

    def _on_toggle_glow(self):
        state = (self.glow_switch.get() == 1)
        screen_glow_service.set_enabled(state)
        cfg = config_manager.config
        if "glow" not in cfg:
            cfg["glow"] = {}
        cfg["glow"]["enabled"] = state
        config_manager.save_config()

    def _set_color(self, hex_code: str):
        screen_glow_service.set_color(hex_code)
        cfg = config_manager.config
        if "glow" not in cfg:
            cfg["glow"] = {}
        cfg["glow"]["color"] = hex_code
        config_manager.save_config()
        self._test_pulse()

    def _test_pulse(self):
        old = screen_glow_service.enabled
        screen_glow_service.set_enabled(True)
        screen_glow_service.trigger_pulse()
        if not old:
            # Revert if it was off
            pass
