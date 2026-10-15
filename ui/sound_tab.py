import customtkinter as ctk
from core.sound_service import sound_service
from core.config_manager import config_manager
from ui.theme import *

class SoundTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text="🎧 Mechanical Switch Audio Simulator",
            font=(FONT_FAMILY, 24, "bold"),
            text_color=NEON_CYAN
        )
        header.pack(anchor="w", padx=20, pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Give your Karnage Visage mecha-membrane keyboard the rich acoustic feeling of high-end mechanical switches.",
            font=(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(anchor="w", padx=20, pady=(0, 15))

        scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=10, pady=0)

        # Main Switch Card
        main_card = ctk.CTkFrame(scrollable, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        main_card.pack(fill="x", padx=10, pady=(0, 15))

        top_row = ctk.CTkFrame(main_card, fg_color="transparent")
        top_row.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(top_row, text="🔊 Audio Engine Status", font=(FONT_FAMILY, 15, "bold"), text_color=TEXT_PRIMARY).pack(side="left")

        self.enable_switch = ctk.CTkSwitch(
            top_row,
            text="Enable Keystroke Sound Effects",
            font=(FONT_FAMILY, 13, "bold"),
            progress_color=NEON_CYAN,
            command=self._on_toggle_enabled
        )
        if sound_service.enabled:
            self.enable_switch.select()
        else:
            self.enable_switch.deselect()
        self.enable_switch.pack(side="right")

        # Sound Profile Selector Card
        prof_card = ctk.CTkFrame(scrollable, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        prof_card.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(prof_card, text="🎹 Select Switch Acoustic Profile", font=(FONT_FAMILY, 15, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w", padx=15, pady=(15, 10))

        self.profiles = [
            ("thock", "🪵 Thocky Tactile", "Deep, wooden, satisfying tactile bottom-out (Holy Panda / Boba U4T style)"),
            ("clicky", "⚡ Crisp Clicky", "Sharp, high-pitched mechanical snap (Cherry MX Blue / Box Jade style)"),
            ("creamy", "🧈 Creamy Linear", "Silky, lubed, low-pitched linear bottom-out (Gateron Yellow / Tangerine style)"),
            ("bubble", "🫧 Bubble Pop", "Ultra-soft and gentle popping sound for peaceful typing")
        ]

        self.profile_var = ctk.StringVar(value=sound_service.current_sound)

        for key, name, desc in self.profiles:
            row = ctk.CTkFrame(prof_card, fg_color="#1A202C", corner_radius=8, border_width=1, border_color="#2D3748")
            row.pack(fill="x", padx=15, pady=5)

            radio = ctk.CTkRadioButton(
                row,
                text=name,
                font=(FONT_FAMILY, 13, "bold"),
                value=key,
                variable=self.profile_var,
                text_color=TEXT_PRIMARY,
                fg_color=NEON_CYAN,
                command=self._on_profile_change
            )
            radio.pack(side="left", padx=15, pady=12)

            ctk.CTkLabel(row, text=desc, font=(FONT_FAMILY, 11), text_color=TEXT_SECONDARY).pack(side="left", padx=10)

            test_btn = ctk.CTkButton(
                row,
                text="▶ Play",
                font=(FONT_FAMILY, 11, "bold"),
                fg_color="#21262D",
                hover_color=ACCENT_BLUE,
                width=65,
                height=26,
                command=lambda k=key: self._test_sound(k)
            )
            test_btn.pack(side="right", padx=15)

        # Quick Test Bar
        bar = ctk.CTkFrame(scrollable, fg_color="#0A0E14", corner_radius=8, border_width=1, border_color="#1E2631")
        bar.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(
            bar,
            text="💡 Tip: Har key press par headphones ya speakers mein instant sound bajega bina kisi lag ke!",
            font=(FONT_FAMILY, 12),
            text_color=NEON_PURPLE
        ).pack(side="left", padx=15, pady=12)

        test_now_btn = ctk.CTkButton(
            bar,
            text="🔊 Test Active Switch Now",
            font=(FONT_FAMILY, 12, "bold"),
            fg_color=NEON_CYAN,
            text_color="#000",
            hover_color="#55f5ff",
            command=lambda: sound_service.play_key_sound()
        )
        test_now_btn.pack(side="right", padx=15, pady=12)

    def _on_toggle_enabled(self):
        state = (self.enable_switch.get() == 1)
        sound_service.set_enabled(state)
        cfg = config_manager.config
        if "sound" not in cfg:
            cfg["sound"] = {}
        cfg["sound"]["enabled"] = state
        config_manager.save_config()

    def _on_profile_change(self):
        chosen = self.profile_var.get()
        sound_service.set_sound(chosen)
        cfg = config_manager.config
        if "sound" not in cfg:
            cfg["sound"] = {}
        cfg["sound"]["current"] = chosen
        config_manager.save_config()
        sound_service.play_key_sound()

    def _test_sound(self, sound_key: str):
        old = sound_service.current_sound
        sound_service.set_sound(sound_key)
        old_enabled = sound_service.enabled
        sound_service.set_enabled(True)
        sound_service.play_key_sound()
        sound_service.set_sound(old)
        sound_service.set_enabled(old_enabled)
