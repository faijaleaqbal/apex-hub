import customtkinter as ctk
from core.mouse_service import mouse_service
from core.config_manager import config_manager
from ui.theme import *

class MouseTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text="🖱️ Mouse Performance & Customization",
            font=(FONT_FAMILY, 24, "bold"),
            text_color=NEON_CYAN
        )
        header.pack(anchor="w", padx=20, pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Real-time Windows pointer speed, precision sniper mode, and high-speed auto-clicker.",
            font=(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(anchor="w", padx=20, pady=(0, 15))

        scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=10, pady=0)

        # 1. System Pointer Speed Card
        speed_card = ctk.CTkFrame(scrollable, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        speed_card.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(speed_card, text="🎯 System Pointer Speed & Sensitivity", font=(FONT_FAMILY, 15, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w", padx=15, pady=(15, 5))

        slider_row = ctk.CTkFrame(speed_card, fg_color="transparent")
        slider_row.pack(fill="x", padx=15, pady=5)

        curr_speed = mouse_service.get_mouse_speed()
        self.speed_label = ctk.CTkLabel(slider_row, text=f"Speed: {curr_speed} / 20", font=(FONT_FAMILY, 13, "bold"), text_color=NEON_CYAN, width=110, anchor="w")
        self.speed_label.pack(side="left")

        self.speed_slider = ctk.CTkSlider(
            slider_row,
            from_=1,
            to=20,
            number_of_steps=19,
            button_color=NEON_CYAN,
            progress_color=ACCENT_BLUE,
            command=self._on_speed_slider_change
        )
        self.speed_slider.set(curr_speed)
        self.speed_slider.pack(side="left", fill="x", expand=True, padx=15)

        # Toggles Row
        toggles_row = ctk.CTkFrame(speed_card, fg_color="transparent")
        toggles_row.pack(fill="x", padx=15, pady=(10, 15))

        # Mouse Acceleration
        acc_state = mouse_service.get_acceleration()
        self.acc_switch = ctk.CTkSwitch(
            toggles_row,
            text="Enhance Pointer Precision (Acceleration)",
            font=(FONT_FAMILY, 13),
            progress_color=NEON_CYAN,
            command=self._on_acc_toggle
        )
        if acc_state:
            self.acc_switch.select()
        else:
            self.acc_switch.deselect()
        self.acc_switch.pack(side="left", padx=(0, 25))

        # Swap buttons
        self.swap_switch = ctk.CTkSwitch(
            toggles_row,
            text="Swap Left & Right Buttons",
            font=(FONT_FAMILY, 13),
            progress_color=NEON_CYAN,
            command=self._on_swap_toggle
        )
        self.swap_switch.pack(side="left")

        # 2. Sniper Aim Mode Card
        sniper_card = ctk.CTkFrame(scrollable, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        sniper_card.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(sniper_card, text="🔭 Sniper Precision Mode", font=(FONT_FAMILY, 15, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(
            sniper_card,
            text="Press or toggle the hotkey to drop mouse sensitivity to sniper precision for pixel-perfect headshots.",
            font=(FONT_FAMILY, 12),
            text_color=TEXT_SECONDARY
        ).pack(anchor="w", padx=15, pady=(0, 10))

        snip_row = ctk.CTkFrame(sniper_card, fg_color="transparent")
        snip_row.pack(fill="x", padx=15, pady=5)

        self.sniper_btn = ctk.CTkButton(
            snip_row,
            text="Toggle Sniper Mode (F7)",
            font=(FONT_FAMILY, 12, "bold"),
            fg_color="#21262D",
            hover_color=NEON_PURPLE,
            text_color=TEXT_PRIMARY,
            command=self._toggle_sniper_manual
        )
        self.sniper_btn.pack(side="left", padx=(0, 15))

        self.sniper_status_label = ctk.CTkLabel(
            snip_row,
            text="OFF (Normal Speed)",
            font=(FONT_FAMILY, 12, "bold"),
            text_color=TEXT_SECONDARY
        )
        self.sniper_status_label.pack(side="left")

        # 3. Auto Clicker Card
        auto_card = ctk.CTkFrame(scrollable, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        auto_card.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(auto_card, text="⚡ High-Speed Auto-Clicker", font=(FONT_FAMILY, 15, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w", padx=15, pady=(15, 5))

        # CPS Row
        cps_row = ctk.CTkFrame(auto_card, fg_color="transparent")
        cps_row.pack(fill="x", padx=15, pady=5)

        self.cps_label = ctk.CTkLabel(cps_row, text=f"Speed: {mouse_service.autoclicker_cps} CPS", font=(FONT_FAMILY, 13, "bold"), text_color=NEON_PINK, width=120, anchor="w")
        self.cps_label.pack(side="left")

        self.cps_slider = ctk.CTkSlider(
            cps_row,
            from_=1,
            to=50,
            number_of_steps=49,
            button_color=NEON_PINK,
            progress_color=NEON_PURPLE,
            command=self._on_cps_change
        )
        self.cps_slider.set(mouse_service.autoclicker_cps)
        self.cps_slider.pack(side="left", fill="x", expand=True, padx=15)

        # Options Row
        opt_row = ctk.CTkFrame(auto_card, fg_color="transparent")
        opt_row.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(opt_row, text="Button:", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(side="left", padx=(0, 5))
        self.btn_select = ctk.CTkSegmentedButton(
            opt_row,
            values=["Left", "Right", "Middle"],
            command=self._on_btn_select
        )
        self.btn_select.set("Left")
        self.btn_select.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(opt_row, text="Click Type:", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(side="left", padx=(0, 5))
        self.type_select = ctk.CTkSegmentedButton(
            opt_row,
            values=["Single", "Double"],
            command=self._on_type_select
        )
        self.type_select.set("Single")
        self.type_select.pack(side="left")

        # Action Button Row
        act_row = ctk.CTkFrame(auto_card, fg_color="transparent")
        act_row.pack(fill="x", padx=15, pady=(10, 15))

        self.start_autoclick_btn = ctk.CTkButton(
            act_row,
            text="▶ Start Auto-Clicker",
            font=(FONT_FAMILY, 13, "bold"),
            fg_color=SUCCESS_GREEN,
            hover_color="#2ea043",
            height=38,
            command=self._toggle_autoclick_manual
        )
        self.start_autoclick_btn.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(
            act_row,
            text="💡 Global Hotkey: Press F6 anywhere to Start/Stop",
            font=(FONT_FAMILY, 12, "bold"),
            text_color=TEXT_SECONDARY
        ).pack(side="left")

    def _on_speed_slider_change(self, val):
        val = int(val)
        self.speed_label.configure(text=f"Speed: {val} / 20")
        mouse_service.set_mouse_speed(val)

    def _on_acc_toggle(self):
        mouse_service.set_acceleration(self.acc_switch.get() == 1)

    def _on_swap_toggle(self):
        mouse_service.set_buttons_swapped(self.swap_switch.get() == 1)

    def _toggle_sniper_manual(self):
        is_active = mouse_service.toggle_sniper_mode()
        if is_active:
            self.sniper_status_label.configure(text="🔴 ACTIVE (Precision 3/20)", text_color=NEON_PINK)
            self.sniper_btn.configure(text="Exit Sniper Mode (F7)", fg_color=DANGER_RED)
        else:
            self.sniper_status_label.configure(text="OFF (Normal Speed)", text_color=TEXT_SECONDARY)
            self.sniper_btn.configure(text="Toggle Sniper Mode (F7)", fg_color="#21262D")
        self.speed_slider.set(mouse_service.get_mouse_speed())
        self.speed_label.configure(text=f"Speed: {mouse_service.get_mouse_speed()} / 20")

    def _on_cps_change(self, val):
        val = int(val)
        self.cps_label.configure(text=f"Speed: {val} CPS")
        mouse_service.autoclicker_cps = val

    def _on_btn_select(self, val):
        mouse_service.autoclicker_button = val.lower()

    def _on_type_select(self, val):
        mouse_service.autoclicker_type = val.lower()

    def _toggle_autoclick_manual(self):
        is_running = mouse_service.toggle_autoclicker()
        if is_running:
            self.start_autoclick_btn.configure(text="⏹ Stop Auto-Clicker", fg_color=DANGER_RED, hover_color="#b62324")
        else:
            self.start_autoclick_btn.configure(text="▶ Start Auto-Clicker", fg_color=SUCCESS_GREEN, hover_color="#2ea043")

    def refresh_from_system(self):
        curr_speed = mouse_service.get_mouse_speed()
        self.speed_slider.set(curr_speed)
        self.speed_label.configure(text=f"Speed: {curr_speed} / 20")
