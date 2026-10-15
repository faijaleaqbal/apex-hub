import customtkinter as ctk
from core.keyboard_service import keyboard_service
from core.config_manager import config_manager
from ui.theme import *

class KeyboardTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text="⌨️ Keyboard Remap & Macro Engine",
            font=(FONT_FAMILY, 24, "bold"),
            text_color=NEON_CYAN
        )
        header.pack(anchor="w", padx=20, pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Remap any physical key on your Karnage Visage or any keyboard to Media controls, Quick Apps, or Text Macros.",
            font=(FONT_FAMILY, 13),
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(anchor="w", padx=20, pady=(0, 15))

        scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=10, pady=0)

        # 1. Add New Rule Card
        add_card = ctk.CTkFrame(scrollable, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        add_card.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(add_card, text="➕ Add Custom Remap or Macro", font=(FONT_FAMILY, 15, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w", padx=15, pady=(15, 10))

        form_row = ctk.CTkFrame(add_card, fg_color="transparent")
        form_row.pack(fill="x", padx=15, pady=5)

        # Trigger Key
        ctk.CTkLabel(form_row, text="When I Press Key:", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(side="left", padx=(0, 5))
        self.trigger_entry = ctk.CTkEntry(form_row, placeholder_text="e.g. F8, F9, q, space", width=140)
        self.trigger_entry.pack(side="left", padx=(0, 20))

        # Action Type
        ctk.CTkLabel(form_row, text="Action Category:", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(side="left", padx=(0, 5))
        self.action_type_menu = ctk.CTkOptionMenu(
            form_row,
            values=["Media Control", "Launch App", "Quick Text Snippet"],
            command=self._on_action_type_change,
            width=160
        )
        self.action_type_menu.set("Media Control")
        self.action_type_menu.pack(side="left", padx=(0, 20))

        # Value input
        ctk.CTkLabel(form_row, text="Action / Value:", font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY).pack(side="left", padx=(0, 5))
        self.value_menu = ctk.CTkOptionMenu(
            form_row,
            values=["mute", "vol_up", "vol_down", "play_pause", "next", "prev"],
            width=150
        )
        self.value_menu.pack(side="left", padx=(0, 20))

        self.text_entry = ctk.CTkEntry(form_row, placeholder_text="e.g. calc.exe or template text", width=180)

        # Add Button
        self.add_btn = ctk.CTkButton(
            form_row,
            text="+ Add Rule",
            font=(FONT_FAMILY, 12, "bold"),
            fg_color=NEON_PURPLE,
            hover_color="#6e1cb8",
            width=110,
            command=self._add_rule
        )
        self.add_btn.pack(side="left")

        # 2. Active Remap Rules Table
        self.table_card = ctk.CTkFrame(scrollable, fg_color=CARD_BG, corner_radius=10, border_width=1, border_color=BORDER_COLOR)
        self.table_card.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(self.table_card, text="📋 Active Key Remap Rules", font=(FONT_FAMILY, 15, "bold"), text_color=TEXT_PRIMARY).pack(anchor="w", padx=15, pady=(15, 10))

        self.rules_container = ctk.CTkFrame(self.table_card, fg_color="transparent")
        self.rules_container.pack(fill="x", padx=15, pady=(0, 15))

        self._render_rules()

        # 3. Karnage Hardware RGB Quick Reference Card
        rgb_ref_card = ctk.CTkFrame(scrollable, fg_color="#0D1117", corner_radius=10, border_width=1, border_color="#30363D")
        rgb_ref_card.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(
            rgb_ref_card,
            text="💡 Karnage Visage (WLKM-054) Hardware Lighting Master Reference",
            font=(FONT_FAMILY, 14, "bold"),
            text_color=NEON_CYAN
        ).pack(anchor="w", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            rgb_ref_card,
            text="Since this model has onboard hardware controller without PC companion app, use these physical key combinations:",
            font=(FONT_FAMILY, 12),
            text_color=TEXT_SECONDARY
        ).pack(anchor="w", padx=15, pady=(0, 10))

        ref_grid = ctk.CTkFrame(rgb_ref_card, fg_color="transparent")
        ref_grid.pack(fill="x", padx=15, pady=(0, 15))
        ref_grid.grid_columnconfigure((0, 1), weight=1)

        col1_items = [
            ("Fn + Enter", "Cycle 15 Lighting Effects (Wave, Reactive, etc.)"),
            ("Fn + \\", "Switch 8 Solid Colours (Red, Blue, Cyan, Purple...)"),
            ("Fn + Backspace", "Toggle RGB Backlight ON / OFF")
        ]
        col2_items = [
            ("Fn + Up / Down", "Adjust Brightness (4 intensity levels)"),
            ("Fn + Left / Right", "Adjust Effect Speed (Flow / Breathing pace)"),
            ("Knob Click", "Switch Rotary Knob function (Volume vs Brightness)")
        ]

        for i, (k, desc) in enumerate(col1_items):
            r = ctk.CTkFrame(ref_grid, fg_color="#161B22", corner_radius=6)
            r.grid(row=i, column=0, sticky="ew", padx=5, pady=4)
            ctk.CTkLabel(r, text=k, font=(FONT_FAMILY, 12, "bold"), text_color=NEON_PURPLE, width=110, anchor="w").pack(side="left", padx=10, pady=6)
            ctk.CTkLabel(r, text=desc, font=(FONT_FAMILY, 11), text_color=TEXT_PRIMARY).pack(side="left")

        for i, (k, desc) in enumerate(col2_items):
            r = ctk.CTkFrame(ref_grid, fg_color="#161B22", corner_radius=6)
            r.grid(row=i, column=1, sticky="ew", padx=5, pady=4)
            ctk.CTkLabel(r, text=k, font=(FONT_FAMILY, 12, "bold"), text_color=NEON_PINK, width=120, anchor="w").pack(side="left", padx=10, pady=6)
            ctk.CTkLabel(r, text=desc, font=(FONT_FAMILY, 11), text_color=TEXT_PRIMARY).pack(side="left")

    def _on_action_type_change(self, val):
        if val == "Media Control":
            self.text_entry.pack_forget()
            self.value_menu.pack(side="left", padx=(0, 20))
            self.value_menu.configure(values=["mute", "vol_up", "vol_down", "play_pause", "next", "prev"])
            self.value_menu.set("mute")
        else:
            self.value_menu.pack_forget()
            self.text_entry.pack(side="left", padx=(0, 20))
            if val == "Launch App":
                self.text_entry.configure(placeholder_text="calc.exe, notepad.exe, snippingtool")
            else:
                self.text_entry.configure(placeholder_text="Custom text to paste automatically")

    def _render_rules(self):
        for widget in self.rules_container.winfo_children():
            widget.destroy()

        remaps = keyboard_service.remaps
        if not remaps:
            ctk.CTkLabel(
                self.rules_container,
                text="No active remap rules. Add one above to get started!",
                font=(FONT_FAMILY, 12),
                text_color=TEXT_MUTED
            ).pack(anchor="w", pady=5)
            return

        for key, act in list(remaps.items()):
            row = ctk.CTkFrame(self.rules_container, fg_color="#1F242C", corner_radius=6)
            row.pack(fill="x", pady=3)

            k_badge = ctk.CTkLabel(row, text=f"Key: {key.upper()}", font=(FONT_FAMILY, 12, "bold"), text_color=NEON_CYAN, width=100, anchor="w")
            k_badge.pack(side="left", padx=(10, 5), pady=6)

            arrow = ctk.CTkLabel(row, text="→", font=(FONT_FAMILY, 14, "bold"), text_color=TEXT_MUTED, width=30)
            arrow.pack(side="left")

            act_str = f"[{act.get('type').upper()}] {act.get('value')}"
            desc = ctk.CTkLabel(row, text=act_str, font=(FONT_FAMILY, 12), text_color=TEXT_PRIMARY, anchor="w")
            desc.pack(side="left", fill="x", expand=True, padx=10)

            del_btn = ctk.CTkButton(
                row,
                text="✕ Remove",
                font=(FONT_FAMILY, 11),
                fg_color="#DA3633",
                hover_color="#b62324",
                width=80,
                height=26,
                command=lambda k=key: self._delete_rule(k)
            )
            del_btn.pack(side="right", padx=10)

    def _add_rule(self):
        key = self.trigger_entry.get().strip().lower()
        if not key:
            return

        act_category = self.action_type_menu.get()
        if act_category == "Media Control":
            act_type = "media"
            act_val = self.value_menu.get()
        elif act_category == "Launch App":
            act_type = "launch"
            act_val = self.text_entry.get().strip()
        else:
            act_type = "text"
            act_val = self.text_entry.get().strip()

        if not act_val:
            return

        keyboard_service.add_remap(key, act_type, act_val)
        cfg = config_manager.config
        if "keyboard" not in cfg:
            cfg["keyboard"] = {"remaps": {}}
        cfg["keyboard"]["remaps"][key] = {"type": act_type, "value": act_val}
        config_manager.save_config()

        self.trigger_entry.delete(0, "end")
        self.text_entry.delete(0, "end")
        self._render_rules()

    def _delete_rule(self, key: str):
        keyboard_service.remove_remap(key)
        cfg = config_manager.config
        if "keyboard" in cfg and "remaps" in cfg["keyboard"]:
            cfg["keyboard"]["remaps"].pop(key, None)
            config_manager.save_config()
        self._render_rules()
