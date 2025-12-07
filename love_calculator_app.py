"""
Love Calculator App
Copyright (c) 2025 Aravindkumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to use,
modify, and distribute copies of the Software, provided that this header
remains intact and credit is given to the original author: Aravindkumar.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import random
import os

# Try to import winsound for sound effects (Windows only)
try:
    import winsound

    def play_success_sound():
        # Simple pleasant beep
        winsound.Beep(900, 150)
        winsound.Beep(1200, 150)

    def play_error_sound():
        winsound.Beep(300, 250)

except ImportError:
    # Fallback if winsound is not available
    def play_success_sound():
        pass

    def play_error_sound():
        pass


# ----------------------------------------------------------------------
# CORE LOVE SCORE (NAME-BASED)
# ----------------------------------------------------------------------
def calculate_love_score(name1: str, name2: str) -> int:
    """
    Simple deterministic love score:
    - Remove spaces, lower case
    - Keep only alphabetic characters
    - Sum character codes and mod 101
    """
    combined = (name1 + name2).replace(" ", "").lower()
    filtered = "".join(ch for ch in combined if ch.isalpha())

    if not filtered:
        return 0

    total = sum(ord(ch) for ch in filtered)
    score = total % 101  # 0–100
    return score


def fake_vs_real_message(score: int) -> str:
    """
    Decide the "fake vs real" message based on score.
    Just for fun – not real relationship science 😄
    """
    if score >= 80:
        return "💘 Looks like REAL love!"
    elif score >= 50:
        return "💖 Could be real – give it time."
    elif score >= 30:
        return "😊 Cute crush vibes. See where it goes."
    else:
        return "😂 Mostly for fun (fake meter high)!"


# ----------------------------------------------------------------------
# ZODIAC COMPATIBILITY
# ----------------------------------------------------------------------
ZODIAC_SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

ZODIAC_ELEMENT = {
    "Aries": "Fire",
    "Leo": "Fire",
    "Sagittarius": "Fire",
    "Taurus": "Earth",
    "Virgo": "Earth",
    "Capricorn": "Earth",
    "Gemini": "Air",
    "Libra": "Air",
    "Aquarius": "Air",
    "Cancer": "Water",
    "Scorpio": "Water",
    "Pisces": "Water",
}


def zodiac_compatibility(sign1: str, sign2: str):
    """
    Simple zodiac compatibility:
    - If either not selected / invalid: 0 bonus, generic message.
    - Same sign: +15% bonus
    - Same element (Fire/Earth/Air/Water): +12%
    - Complementary elements (Fire-Air, Earth-Water): +8%
    - Otherwise: +3% small bonus
    Returns: (bonus, message)
    """
    if not sign1 or not sign2:
        return 0, "Select both zodiac signs to see star match bonus!"

    if sign1 not in ZODIAC_ELEMENT or sign2 not in ZODIAC_ELEMENT:
        return 0, "Unknown zodiac sign(s). No star bonus added."

    if sign1 == sign2:
        return 15, f"{sign1} & {sign2}: Same sign! Strong mutual understanding. 🌟"

    elem1 = ZODIAC_ELEMENT[sign1]
    elem2 = ZODIAC_ELEMENT[sign2]

    # Same element
    if elem1 == elem2:
        return 12, f"{sign1} & {sign2}: Both are {elem1} signs – natural flow and comfort. ✨"

    # Complementary elements
    complementary_pairs = {
        ("Fire", "Air"),
        ("Air", "Fire"),
        ("Earth", "Water"),
        ("Water", "Earth"),
    }
    if (elem1, elem2) in complementary_pairs:
        return 8, (
            f"{sign1} ({elem1}) & {sign2} ({elem2}): Complementary energies – "
            "good balance when you support each other. 💫"
        )

    # Everything else
    return 3, (
        f"{sign1} ({elem1}) & {sign2} ({elem2}): Different styles, but opposites "
        "can attract if you communicate well. 💞"
    )


# ----------------------------------------------------------------------
# MAIN APP
# ----------------------------------------------------------------------
class LoveCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Love Calculator – by Aravindkumar")
        self.geometry("620x420")
        self.resizable(False, False)

        # Fullscreen state
        self.is_fullscreen = False

        # Theme definitions
        self.themes = {
            "light": {
                "bg": "#f7f7ff",
                "fg": "#222222",
                "accent": "#ff4d6a",
                "card": "#ffffff",
                "entry_bg": "#ffffff",
            },
            "dark": {
                "bg": "#15151e",
                "fg": "#f0f0f5",
                "accent": "#ff4d6a",
                "card": "#1f1f2b",
                "entry_bg": "#2a2a3a",
            },
        }
        self.current_theme = "light"

        # history_items: (name1, name2, sign1, sign2, score, message, time)
        self.history_items = []

        # Background image / animated wallpaper frames
        self.bg_frames = []
        self.bg_frame_index = 0
        self._load_background_frames()

        self._build_ui()
        self._apply_theme()

        # Start background animation (if frames available)
        if self.bg_frames:
            self.animate_background()

        # Keyboard shortcuts for fullscreen
        self.bind("<F11>", self._toggle_fullscreen_event)
        self.bind("<Escape>", self._exit_fullscreen_event)

    # ------------------------------------------------------------------
    # BACKGROUND IMAGE / ANIMATED WALLPAPER
    # ------------------------------------------------------------------
    def _load_background_frames(self):
        """
        Load animated GIF frames for background if available.
        Fallback: single static image.
        Expected files in same folder:
        - 'love_bg.gif' (animated) OR
        - 'love_bg.png' (static)
        """
        # Try animated GIF first
        gif_path = "love_bg.gif"
        png_path = "love_bg.png"

        if os.path.exists(gif_path):
            try:
                i = 0
                while True:
                    frame = tk.PhotoImage(file=gif_path, format=f"gif -index {i}")
                    self.bg_frames.append(frame)
                    i += 1
            except tk.TclError:
                # Reached end of frames or error, ignore
                pass

        # If no GIF frames loaded, try static PNG
        if not self.bg_frames and os.path.exists(png_path):
            try:
                self.bg_frames.append(tk.PhotoImage(file=png_path))
            except tk.TclError:
                self.bg_frames = []

    def animate_background(self):
        """
        Animate the background by cycling through GIF frames.
        Only affects the Calculator tab background label.
        """
        if not self.bg_frames or not hasattr(self, "calc_bg_label"):
            return

        frame = self.bg_frames[self.bg_frame_index]
        self.calc_bg_label.configure(image=frame)
        self.calc_bg_label.image = frame  # keep reference

        self.bg_frame_index = (self.bg_frame_index + 1) % len(self.bg_frames)

        # Adjust speed here (in ms). 80–120 looks nice.
        self.after(100, self.animate_background)

    # ------------------------------------------------------------------
    # UI BUILDING
    # ------------------------------------------------------------------
    def _build_ui(self):
        # Top bar with title, theme switch, fullscreen
        top_bar = tk.Frame(self)
        top_bar.pack(fill="x", pady=(5, 0), padx=8)

        self.title_label = tk.Label(
            top_bar,
            text="❤️  Love Calculator  ❤️",
            font=("Segoe UI", 18, "bold"),
        )
        self.title_label.pack(side="left")

        self.theme_button = ttk.Button(
            top_bar,
            text="Switch to Dark Theme",
            command=self.toggle_theme,
        )
        self.theme_button.pack(side="right")

        self.fullscreen_button = ttk.Button(
            top_bar,
            text="Go Fullscreen",
            command=self.toggle_fullscreen,
        )
        self.fullscreen_button.pack(side="right", padx=(5, 0))

        # Notebook for multiple "pages"
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        # Tabs
        self.calc_frame = tk.Frame(self.notebook, bd=0, highlightthickness=0)
        self.history_frame = tk.Frame(self.notebook, bd=0, highlightthickness=0)
        self.about_frame = tk.Frame(self.notebook, bd=0, highlightthickness=0)

        self.notebook.add(self.calc_frame, text="Calculator")
        self.notebook.add(self.history_frame, text="History")
        self.notebook.add(self.about_frame, text="About")

        self._build_calc_tab()
        self._build_history_tab()
        self._build_about_tab()

    def _build_calc_tab(self):
        # Background image label for animated wallpaper
        # This fills the whole calculator tab
        self.calc_bg_label = tk.Label(self.calc_frame)
        self.calc_bg_label.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1
        )

        # Card-style container on top of background
        card = tk.Frame(self.calc_frame, bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.96, relheight=0.9)

        # Name inputs
        input_frame = tk.Frame(card)
        input_frame.pack(pady=10, fill="x", padx=10)

        self.your_name_label = tk.Label(
            input_frame,
            text="Your Name:",
            font=("Segoe UI", 11),
        )
        self.your_name_label.grid(row=0, column=0, sticky="w", pady=4)

        self.your_name_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 11),
        )
        self.your_name_entry.grid(row=0, column=1, sticky="ew", pady=4, padx=(5, 0))

        self.partner_name_label = tk.Label(
            input_frame,
            text="Partner's Name:",
            font=("Segoe UI", 11),
        )
        self.partner_name_label.grid(row=1, column=0, sticky="w", pady=4)

        self.partner_name_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 11),
        )
        self.partner_name_entry.grid(row=1, column=1, sticky="ew", pady=4, padx=(5, 0))

        input_frame.columnconfigure(1, weight=1)

        # Zodiac dropdowns
        zodiac_frame = tk.Frame(card)
        zodiac_frame.pack(pady=(0, 10), fill="x", padx=10)

        zodiac_label_you = tk.Label(
            zodiac_frame,
            text="Your Zodiac Sign:",
            font=("Segoe UI", 10),
        )
        zodiac_label_you.grid(row=0, column=0, sticky="w", pady=3)

        self.zodiac1_var = tk.StringVar(value="")
        self.zodiac1_combo = ttk.Combobox(
            zodiac_frame,
            textvariable=self.zodiac1_var,
            values=ZODIAC_SIGNS,
            state="readonly",
            width=16,
        )
        self.zodiac1_combo.grid(row=0, column=1, sticky="w", padx=(5, 15), pady=3)

        zodiac_label_partner = tk.Label(
            zodiac_frame,
            text="Partner's Zodiac Sign:",
            font=("Segoe UI", 10),
        )
        zodiac_label_partner.grid(row=1, column=0, sticky="w", pady=3)

        self.zodiac2_var = tk.StringVar(value="")
        self.zodiac2_combo = ttk.Combobox(
            zodiac_frame,
            textvariable=self.zodiac2_var,
            values=ZODIAC_SIGNS,
            state="readonly",
            width=16,
        )
        self.zodiac2_combo.grid(row=1, column=1, sticky="w", padx=(5, 15), pady=3)

        # Buttons
        button_frame = tk.Frame(card)
        button_frame.pack(pady=8)

        self.calculate_button = ttk.Button(
            button_frame,
            text="Calculate Love 💝",
            command=self.on_calculate_clicked,
        )
        self.calculate_button.grid(row=0, column=0, padx=5)

        self.clear_button = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_inputs,
        )
        self.clear_button.grid(row=0, column=1, padx=5)

        # Result section
        result_frame = tk.Frame(card)
        result_frame.pack(pady=10, fill="x", padx=10)

        self.result_label = tk.Label(
            result_frame,
            text="Love Score: -- %",
            font=("Segoe UI", 14, "bold"),
        )
        self.result_label.pack(pady=4)

        # Progress bar as love meter
        self.love_meter = ttk.Progressbar(
            result_frame,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            length=360,
        )
        self.love_meter.pack(pady=4)

        self.fake_real_label = tk.Label(
            result_frame,
            text="Fake vs Real meter will appear here.",
            font=("Segoe UI", 11),
        )
        self.fake_real_label.pack(pady=6)

        self.zodiac_result_label = tk.Label(
            result_frame,
            text="Zodiac match bonus will appear here.",
            font=("Segoe UI", 10, "italic"),
            wraplength=560,
            justify="center",
        )
        self.zodiac_result_label.pack(pady=(0, 6))

        # Heart animation canvas (extra visuals)
        self.heart_canvas = tk.Canvas(
            card,
            bd=0,
            highlightthickness=0,
            height=120,
        )
        self.heart_canvas.pack(fill="x", padx=10, pady=(0, 10))

        self.note_label = tk.Label(
            card,
            text=(
                "Note: This is just for fun. Real relationships need trust, "
                "respect, communication… and not only zodiac signs. 😊"
            ),
            font=("Segoe UI", 9, "italic"),
            wraplength=560,
            justify="center",
        )
        self.note_label.pack(side="bottom", pady=(10, 0))

    def _build_history_tab(self):
        outer = tk.Frame(self.history_frame)
        outer.pack(fill="both", expand=True, padx=10, pady=10)

        header = tk.Label(
            outer,
            text="History of Checked Pairs",
            font=("Segoe UI", 13, "bold"),
        )
        header.pack(anchor="w", pady=(0, 8))

        # Treeview for history
        columns = ("you", "partner", "sign_you", "sign_partner", "score", "meter", "time")
        self.history_tree = ttk.Treeview(
            outer,
            columns=columns,
            show="headings",
            height=10,
        )

        self.history_tree.heading("you", text="You")
        self.history_tree.heading("partner", text="Partner")
        self.history_tree.heading("sign_you", text="Your Sign")
        self.history_tree.heading("sign_partner", text="Partner Sign")
        self.history_tree.heading("score", text="Score %")
        self.history_tree.heading("meter", text="Fake vs Real")
        self.history_tree.heading("time", text="Time")

        self.history_tree.column("you", width=110)
        self.history_tree.column("partner", width=110)
        self.history_tree.column("sign_you", width=90)
        self.history_tree.column("sign_partner", width=100)
        self.history_tree.column("score", width=65, anchor="center")
        self.history_tree.column("meter", width=160)
        self.history_tree.column("time", width=80)

        self.history_tree.pack(fill="both", expand=True, pady=(0, 8))

        clear_btn = ttk.Button(
            outer,
            text="Clear History",
            command=self.clear_history,
        )
        clear_btn.pack(anchor="e")

    def _build_about_tab(self):
        about_card = tk.Frame(self.about_frame)
        about_card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.96, relheight=0.9)

        title = tk.Label(
            about_card,
            text="About This App",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(pady=(10, 5))

        body_text = (
            "Love Calculator App\n"
            "Version 1.1.0\n\n"
            "This fun app lets you enter two names and calculates a playful "
            "love score along with a “fake vs real love” meter.\n\n"
            "✨ Features:\n"
            "• Love percentage calculator (based on names)\n"
            "• Zodiac sign based star-match bonus\n"
            "• Fake vs real love meter\n"
            "• Dark / Light theme switch\n"
            "• Sound effects\n"
            "• History of checked pairs (with zodiac signs)\n"
            "• Fullscreen mode\n"
            "• Animated hearts & love report popup\n"
            "• Animated background wallpaper on calculator tab\n\n"
            "👨‍💻 Made with ❤️ by Aravindkumar\n"
        )

        body = tk.Label(
            about_card,
            text=body_text,
            justify="left",
            font=("Segoe UI", 11),
            wraplength=560,
        )
        body.pack(padx=10, pady=5, anchor="w")

        footer = tk.Label(
            about_card,
            text="© 2025 Aravindkumar. All rights reserved.",
            font=("Segoe UI", 9, "italic"),
        )
        footer.pack(side="bottom", pady=10)

    # ------------------------------------------------------------------
    # THEME HANDLING
    # ------------------------------------------------------------------
    def _apply_theme(self):
        theme = self.themes[self.current_theme]
        bg = theme["bg"]
        fg = theme["fg"]
        card_bg = theme["card"]

        self.configure(bg=bg)
        self.title_label.configure(bg=bg, fg=fg)

        # Update frames
        for frame in (self.calc_frame, self.history_frame, self.about_frame):
            frame.configure(bg=bg)

        # We need to walk deeper for nested frames
        def apply_recursive(widget):
            for child in widget.winfo_children():
                if isinstance(child, tk.Frame):
                    try:
                        child.configure(bg=card_bg)
                    except tk.TclError:
                        pass
                    apply_recursive(child)
                elif isinstance(child, tk.Label):
                    # Skip background label (image already set)
                    if child is getattr(self, "calc_bg_label", None):
                        continue
                    try:
                        child.configure(bg=card_bg, fg=fg)
                    except tk.TclError:
                        pass
                elif isinstance(child, tk.Entry):
                    try:
                        child.configure(
                            bg=self.themes[self.current_theme]["entry_bg"],
                            fg=fg,
                            insertbackground=fg,
                        )
                    except tk.TclError:
                        pass

        apply_recursive(self.calc_frame)
        apply_recursive(self.about_frame)
        apply_recursive(self.history_frame)

        # Heart canvas background (semi-overlay)
        if hasattr(self, "heart_canvas"):
            try:
                self.heart_canvas.configure(bg=card_bg)
            except tk.TclError:
                pass

        # Style for ttk elements
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "TButton",
            padding=6,
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "TNotebook",
            background=bg,
        )
        style.configure(
            "TNotebook.Tab",
            padding=(12, 5),
        )
        style.configure(
            "TProgressbar",
        )

        style.configure(
            "Treeview",
            rowheight=22,
            font=("Segoe UI", 10),
        )

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self._apply_theme()

        if self.current_theme == "dark":
            self.theme_button.configure(text="Switch to Light Theme")
        else:
            self.theme_button.configure(text="Switch to Dark Theme")

    # ------------------------------------------------------------------
    # FULLSCREEN HANDLING
    # ------------------------------------------------------------------
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        self._update_fullscreen_button_text()

    def _toggle_fullscreen_event(self, event=None):
        self.toggle_fullscreen()

    def _exit_fullscreen_event(self, event=None):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.attributes("-fullscreen", False)
            self._update_fullscreen_button_text()

    def _update_fullscreen_button_text(self):
        if self.is_fullscreen:
            self.fullscreen_button.configure(text="Exit Fullscreen")
        else:
            self.fullscreen_button.configure(text="Go Fullscreen")

    # ------------------------------------------------------------------
    # LOGIC
    # ------------------------------------------------------------------
    def on_calculate_clicked(self):
        name1 = self.your_name_entry.get().strip()
        name2 = self.partner_name_entry.get().strip()
        sign1 = self.zodiac1_var.get().strip()
        sign2 = self.zodiac2_var.get().strip()

        if not name1 or not name2:
            play_error_sound()
            messagebox.showwarning("Missing info", "Please enter both names.")
            return

        base_score = calculate_love_score(name1, name2)
        zodiac_bonus, zodiac_msg = zodiac_compatibility(
            sign1 if sign1 else None,
            sign2 if sign2 else None,
        )
        final_score = base_score + zodiac_bonus
        if final_score > 100:
            final_score = 100

        msg = fake_vs_real_message(final_score)

        self.result_label.configure(text=f"Love Score: {final_score} %")
        self.love_meter["value"] = final_score
        self.fake_real_label.configure(text=msg)

        if sign1 and sign2:
            self.zodiac_result_label.configure(
                text=f"Zodiac match bonus: +{zodiac_bonus}%\n{zodiac_msg}"
            )
        else:
            self.zodiac_result_label.configure(
                text="Zodiac match: select both signs to add a star-match bonus to the score. ✨"
            )

        # Color + pulse for high scores
        if final_score >= 80:
            accent = self.themes[self.current_theme]["accent"]
            self.result_label.configure(fg=accent)
            self._pulse_result_label()
        else:
            # reset to theme default color
            fg = self.themes[self.current_theme]["fg"]
            self.result_label.configure(fg=fg)

        # Start heart animation
        self.start_heart_animation(final_score)

        play_success_sound()

        # Save to history
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.history_items.append((name1, name2, sign1, sign2, final_score, msg, now))
        self.history_tree.insert(
            "",
            "end",
            values=(
                name1,
                name2,
                sign1 if sign1 else "-",
                sign2 if sign2 else "-",
                final_score,
                msg.replace("💘", "").replace("💖", "").replace("😊", "").replace("😂", ""),
                now,
            ),
        )

        # Show detailed love report popup
        self.show_love_report(name1, name2, sign1, sign2, base_score, zodiac_bonus, final_score, msg, zodiac_msg)

    def clear_inputs(self):
        self.your_name_entry.delete(0, "end")
        self.partner_name_entry.delete(0, "end")
        self.zodiac1_var.set("")
        self.zodiac2_var.set("")
        self.result_label.configure(text="Love Score: -- %")
        self.love_meter["value"] = 0
        self.fake_real_label.configure(text="Fake vs Real meter will appear here.")
        self.zodiac_result_label.configure(
            text="Zodiac match bonus will appear here."
        )
        self.heart_canvas.delete("all")

    def clear_history(self):
        if not self.history_items:
            messagebox.showinfo("History", "No history to clear.")
            return

        answer = messagebox.askyesno(
            "Clear History", "Are you sure you want to clear all history?"
        )
        if answer:
            self.history_items.clear()
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)

    # ------------------------------------------------------------------
    # EXTRA VISUALS & ANIMATIONS
    # ------------------------------------------------------------------
    def start_heart_animation(self, score: int):
        """Create floating heart animation on the canvas."""
        self.heart_canvas.delete("all")

        # More hearts for higher scores
        if score >= 80:
            num_hearts = 16
        elif score >= 50:
            num_hearts = 10
        else:
            num_hearts = 6

        # Get canvas width (fallback if not yet drawn)
        width = self.heart_canvas.winfo_width()
        if width <= 1:
            width = 560

        for _ in range(num_hearts):
            x = random.randint(20, width - 20)
            y = random.randint(70, 110)
            size = random.randint(16, 26)
            # Using Unicode heart as text
            item = self.heart_canvas.create_text(
                x,
                y,
                text="❤",
                font=("Segoe UI Emoji", size, "bold"),
            )
            dy = -random.uniform(1.0, 2.5)
            steps = random.randint(35, 55)
            delay = random.randint(0, 300)
            self.after(
                delay,
                lambda it=item, ddy=dy, st=steps: self._animate_heart(it, ddy, st),
            )

    def _animate_heart(self, item, dy, steps):
        if steps <= 0:
            self.heart_canvas.delete(item)
            return
        self.heart_canvas.move(item, 0, dy)
        self.heart_canvas.after(
            40, lambda it=item, ddy=dy, st=steps - 1: self._animate_heart(it, ddy, st)
        )

    def _pulse_result_label(self, step: int = 0):
        """Simple pulse animation on the result label."""
        sizes = [14, 16, 18, 16, 14]
        if step >= len(sizes):
            self.result_label.configure(font=("Segoe UI", 14, "bold"))
            return
        self.result_label.configure(font=("Segoe UI", sizes[step], "bold"))
        self.after(80, lambda: self._pulse_result_label(step + 1))

    # ------------------------------------------------------------------
    # LOVE REPORT POPUP
    # ------------------------------------------------------------------
    def show_love_report(
        self,
        name1: str,
        name2: str,
        sign1: str,
        sign2: str,
        base_score: int,
        zodiac_bonus: int,
        final_score: int,
        msg: str,
        zodiac_msg: str,
    ):
        """Show a nice popup window with detailed love report."""
        theme = self.themes[self.current_theme]
        card_bg = theme["card"]
        fg = theme["fg"]
        accent = theme["accent"]

        report_window = tk.Toplevel(self)
        report_window.title("Love Report")
        report_window.transient(self)
        report_window.grab_set()
        report_window.resizable(False, False)

        # Center slightly above main window
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 160
        y = self.winfo_y() + (self.winfo_height() // 2) - 140
        report_window.geometry(f"340x280+{x}+{y}")

        container = tk.Frame(report_window, bg=card_bg)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        title_label = tk.Label(
            container,
            text="💌 Love Report",
            font=("Segoe UI", 14, "bold"),
            bg=card_bg,
            fg=accent,
        )
        title_label.pack(pady=(0, 8))

        names_label = tk.Label(
            container,
            text=f"{name1} ❤️ {name2}",
            font=("Segoe UI", 12, "bold"),
            bg=card_bg,
            fg=fg,
        )
        names_label.pack(pady=(0, 4))

        if sign1 or sign2:
            sign_text = f"Zodiac: {sign1 if sign1 else '?'} & {sign2 if sign2 else '?'}"
        else:
            sign_text = "Zodiac: Not selected"

        sign_label = tk.Label(
            container,
            text=sign_text,
            font=("Segoe UI", 10),
            bg=card_bg,
            fg=fg,
        )
        sign_label.pack(pady=2)

        score_label = tk.Label(
            container,
            text=(
                f"Base Name Score: {base_score} %\n"
                f"Zodiac Bonus: +{zodiac_bonus} %\n"
                f"Final Love Score: {final_score} %"
            ),
            font=("Segoe UI", 10),
            bg=card_bg,
            fg=fg,
            justify="center",
        )
        score_label.pack(pady=4)

        meter_label = tk.Label(
            container,
            text=msg,
            font=("Segoe UI", 11),
            bg=card_bg,
            fg=fg,
            wraplength=300,
            justify="center",
        )
        meter_label.pack(pady=2)

        zodiac_label = tk.Label(
            container,
            text=zodiac_msg,
            font=("Segoe UI", 9, "italic"),
            bg=card_bg,
            fg=fg,
            wraplength=300,
            justify="center",
        )
        zodiac_label.pack(pady=(4, 6))

        advice = self._advice_for_score(final_score)
        advice_label = tk.Label(
            container,
            text=advice,
            font=("Segoe UI", 9, "italic"),
            bg=card_bg,
            fg=fg,
            wraplength=300,
            justify="center",
        )
        advice_label.pack(pady=(4, 8))

        # Buttons frame
        btn_frame = tk.Frame(container, bg=card_bg)
        btn_frame.pack(side="bottom", fill="x", pady=(10, 0))

        copy_btn = ttk.Button(
            btn_frame,
            text="Copy Result",
            command=lambda: self._copy_report_to_clipboard(
                name1,
                name2,
                sign1,
                sign2,
                final_score,
                msg,
            ),
        )
        copy_btn.pack(side="left", padx=(0, 5))

        close_btn = ttk.Button(
            btn_frame,
            text="Close",
            command=report_window.destroy,
        )
        close_btn.pack(side="right")

    def _copy_report_to_clipboard(
        self,
        name1: str,
        name2: str,
        sign1: str,
        sign2: str,
        score: int,
        msg: str,
    ):
        zodiac_part = ""
        if sign1 or sign2:
            zodiac_part = f" | Zodiac: {sign1 if sign1 else '?'} & {sign2 if sign2 else '?'}"

        text = f"{name1} ❤️ {name2}{zodiac_part} – Love Score: {score}% | {msg}"
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
        except tk.TclError:
            # If clipboard not available, silently ignore
            pass

    def _advice_for_score(self, score: int) -> str:
        """Give a short advice line based on score."""
        if score >= 90:
            return "Strong soulmate vibes! Keep nurturing this beautiful bond. 💞"
        elif score >= 75:
            return "Great connection! Communication and trust will make it even stronger."
        elif score >= 50:
            return "Nice chemistry! Take time to understand each other and grow together."
        elif score >= 30:
            return "Cute crush energy. Go slow, be yourself, and see where it goes."
        else:
            return (
                "Remember: this is just for fun! Focus on self-love and the right person "
                "will match your energy. 💫"
            )


if __name__ == "__main__":
    app = LoveCalculatorApp()
    app.mainloop()
