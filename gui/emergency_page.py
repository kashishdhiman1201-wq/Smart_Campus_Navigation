
import tkinter as tk
from tkinter import ttk, messagebox

from modules.graph_builder import create_campus_graph
from modules.emergency_evacuation import find_evacuation_route


# ---------- PROFESSIONAL THEME ----------

BG = "#F1F5F9"
WHITE = "#FFFFFF"
NAVY = "#14213D"
TEXT = "#1E293B"
MUTED = "#64748B"
BORDER = "#E2E8F0"

BLUE = "#2563EB"
BLUE_HOVER = "#1D4ED8"
RED = "#DC2626"
RED_HOVER = "#B91C1C"
GREEN = "#15803D"
LIGHT_BLUE = "#EFF6FF"
LIGHT_RED = "#FEE2E2"
LIGHT_GREEN = "#DCFCE7"
LIGHT_GRAY = "#F8FAFC"


class EmergencyPage:

    def __init__(self, root):

        self.root = root
        self.graph = create_campus_graph()
        self.locations = list(self.graph.nodes)

        self.blocked_paths = []

        self.setup_styles()
        self.setup_ui()

    # ---------- STYLES ----------

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Emergency.TCombobox",
            font=("Segoe UI", 10),
            padding=8,
            fieldbackground=WHITE,
            background=WHITE
        )

    def create_card(self, parent, padding=18):

        return tk.Frame(
            parent,
            bg=WHITE,
            padx=padding,
            pady=padding,
            highlightbackground=BORDER,
            highlightthickness=1
        )

    def create_button(
        self, parent, text, command,
        bg=BLUE, hover=BLUE_HOVER, fg=WHITE
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 9, "bold"),
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=fg,
            relief="flat",
            bd=0,
            padx=17,
            pady=10,
            cursor="hand2"
        )

        button.bind(
            "<Enter>",
            lambda event: button.configure(bg=hover)
        )

        button.bind(
            "<Leave>",
            lambda event: button.configure(bg=bg)
        )

        return button

    # ---------- MAIN UI ----------

    def setup_ui(self):

        self.root.configure(bg=BG)

        self.main_frame = tk.Frame(
            self.root,
            bg=BG
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=20
        )

        # Page heading

        heading = tk.Frame(
            self.main_frame,
            bg=BG
        )

        heading.pack(
            fill="x",
            pady=(0, 16)
        )

        tk.Label(
            heading,
            text="Emergency Evacuation",
            font=("Segoe UI", 23, "bold"),
            bg=BG,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            heading,
            text="Identify blocked pathways and find a safe route "
                 "to the campus assembly point.",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=(5, 0))

        # Information cards

        info_frame = tk.Frame(
            self.main_frame,
            bg=BG
        )

        info_frame.pack(
            fill="x",
            pady=(0, 16)
        )

        info_frame.columnconfigure(
            (0, 1, 2), weight=1
        )

        self.create_info_card(
            info_frame,
            0,
            "CAMPUS LOCATIONS",
            str(len(self.locations)),
            "Available locations"
        )

        self.create_info_card(
            info_frame,
            1,
            "SAFE ZONE",
            "ASSEMBLY",
            "Designated evacuation point"
        )

        self.create_info_card(
            info_frame,
            2,
            "EVACUATION ALGORITHM",
            "DIJKSTRA",
            "Shortest safe route"
        )

        # Main content area

        content = tk.Frame(
            self.main_frame,
            bg=BG
        )

        content.pack(
            fill="both",
            expand=True
        )

        content.columnconfigure(0, weight=5)
        content.columnconfigure(1, weight=6)
        content.rowconfigure(0, weight=1)

        # LEFT PANEL

        left_panel = tk.Frame(
            content,
            bg=BG
        )

        left_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        # Location selection card

        form_card = self.create_card(
            left_panel,
            20
        )

        form_card.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Label(
            form_card,
            text="Evacuation Controls",
            font=("Segoe UI", 15, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            form_card,
            text="Select your current campus location.",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(5, 18))

        tk.Label(
            form_card,
            text="CURRENT LOCATION",
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w")

        self.start_var = tk.StringVar(
            value="COMPUTER_LAB"
        )

        self.start_combo = ttk.Combobox(
            form_card,
            textvariable=self.start_var,
            values=self.locations,
            state="readonly",
            style="Emergency.TCombobox"
        )

        self.start_combo.pack(
            fill="x",
            pady=(7, 18)
        )

        # Safe zone display

        safe_frame = tk.Frame(
            form_card,
            bg=LIGHT_GREEN,
            padx=12,
            pady=10
        )

        safe_frame.pack(
            fill="x",
            pady=(0, 18)
        )

        tk.Label(
            safe_frame,
            text="DESIGNATED SAFE ZONE",
            font=("Segoe UI", 8, "bold"),
            bg=LIGHT_GREEN,
            fg=GREEN
        ).pack(anchor="w")

        tk.Label(
            safe_frame,
            text="ASSEMBLY",
            font=("Segoe UI", 15, "bold"),
            bg=LIGHT_GREEN,
            fg=GREEN
        ).pack(anchor="w", pady=(3, 0))

        # Block pathway section

        tk.Label(
            form_card,
            text="BLOCK AN UNAVAILABLE PATHWAY",
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(0, 10))

        tk.Label(
            form_card,
            text="First Location",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        self.path_a = ttk.Combobox(
            form_card,
            values=self.locations,
            state="readonly",
            style="Emergency.TCombobox"
        )

        self.path_a.pack(
            fill="x",
            pady=(5, 12)
        )

        tk.Label(
            form_card,
            text="Second Location",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        self.path_b = ttk.Combobox(
            form_card,
            values=self.locations,
            state="readonly",
            style="Emergency.TCombobox"
        )

        self.path_b.pack(
            fill="x",
            pady=(5, 16)
        )

        # Action buttons

        self.create_button(
            form_card,
            "BLOCK PATHWAY",
            self.add_blocked_path,
            bg=RED,
            hover=RED_HOVER
        ).pack(fill="x", pady=(0, 9))

        self.create_button(
            form_card,
            "FIND EVACUATION ROUTE",
            self.find_route,
            bg=BLUE,
            hover=BLUE_HOVER
        ).pack(fill="x", pady=(0, 9))

        self.create_button(
            form_card,
            "RESET SYSTEM",
            self.reset_page,
            bg="#E8EEF6",
            hover="#D9E4F2",
            fg=TEXT
        ).pack(fill="x")

        # Blocked pathways card

        blocked_card = self.create_card(
            left_panel,
            18
        )

        blocked_card.pack(
            fill="both",
            expand=True
        )

        blocked_header = tk.Frame(
            blocked_card,
            bg=WHITE
        )

        blocked_header.pack(fill="x")

        tk.Label(
            blocked_header,
            text="Blocked Pathways",
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(side="left")

        self.blocked_count = tk.Label(
            blocked_header,
            text="0",
            font=("Segoe UI", 9, "bold"),
            bg=LIGHT_RED,
            fg=RED,
            padx=9,
            pady=4
        )

        self.blocked_count.pack(side="right")

        tk.Label(
            blocked_card,
            text="Unavailable connections in the campus graph.",
            font=("Segoe UI", 8),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(5, 12))

        blocked_list_frame = tk.Frame(
            blocked_card,
            bg=LIGHT_GRAY,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        blocked_list_frame.pack(
            fill="both",
            expand=True
        )

        self.blocked_label = tk.Label(
            blocked_list_frame,
            text="No pathways blocked",
            font=("Segoe UI", 9),
            bg=LIGHT_GRAY,
            fg=MUTED,
            justify="left",
            anchor="nw",
            padx=12,
            pady=12
        )

        self.blocked_label.pack(
            fill="both",
            expand=True
        )

        # RIGHT PANEL

        right_panel = self.create_card(
            content,
            20
        )

        right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        # Result header

        result_header = tk.Frame(
            right_panel,
            bg=WHITE
        )

        result_header.pack(fill="x")

        tk.Label(
            result_header,
            text="Evacuation Report",
            font=("Segoe UI", 16, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(side="left")

        self.status_badge = tk.Label(
            result_header,
            text="WAITING",
            font=("Segoe UI", 8, "bold"),
            bg=LIGHT_BLUE,
            fg=BLUE,
            padx=11,
            pady=5
        )

        self.status_badge.pack(side="right")

        tk.Label(
            right_panel,
            text="Recommended safe route and evacuation details.",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(5, 18))

        # Result metric cards

        metrics = tk.Frame(
            right_panel,
            bg=WHITE
        )

        metrics.pack(
            fill="x",
            pady=(0, 18)
        )

        metrics.columnconfigure(
            (0, 1), weight=1
        )

        self.distance_value = self.create_metric(
            metrics,
            0,
            "ROUTE DISTANCE",
            "--",
            "meters"
        )

        self.stops_value = self.create_metric(
            metrics,
            1,
            "ROUTE LOCATIONS",
            "--",
            "locations"
        )

        # Report text

        tk.Label(
            right_panel,
            text="EVACUATION DETAILS",
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(0, 8))

        report_frame = tk.Frame(
            right_panel,
            bg=LIGHT_GRAY,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        report_frame.pack(
            fill="both",
            expand=True
        )

        self.result_text = tk.Text(
            report_frame,
            font=("Segoe UI", 10),
            bg=LIGHT_GRAY,
            fg=TEXT,
            relief="flat",
            bd=0,
            wrap="word",
            padx=15,
            pady=15,
            spacing1=4,
            spacing3=4
        )

        scrollbar = ttk.Scrollbar(
            report_frame,
            orient="vertical",
            command=self.result_text.yview
        )

        self.result_text.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.result_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.set_initial_report()

    # ---------- INFORMATION CARDS ----------

    def create_info_card(
        self, parent, column,
        heading, value, description
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            padx=16,
            pady=12,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=5
        )

        tk.Label(
            card,
            text=heading,
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w")

        tk.Label(
            card,
            text=value,
            font=("Segoe UI", 16, "bold"),
            bg=WHITE,
            fg=BLUE
        ).pack(anchor="w", pady=3)

        tk.Label(
            card,
            text=description,
            font=("Segoe UI", 8),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w")

    # ---------- METRIC CARDS ----------

    def create_metric(
        self, parent, column,
        heading, value, unit
    ):

        card = tk.Frame(
            parent,
            bg=LIGHT_BLUE,
            padx=12,
            pady=13
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=4
        )

        tk.Label(
            card,
            text=heading,
            font=("Segoe UI", 8, "bold"),
            bg=LIGHT_BLUE,
            fg=MUTED
        ).pack(anchor="w")

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 18, "bold"),
            bg=LIGHT_BLUE,
            fg=BLUE
        )

        value_label.pack(
            anchor="w",
            pady=4
        )

        tk.Label(
            card,
            text=unit,
            font=("Segoe UI", 8),
            bg=LIGHT_BLUE,
            fg=MUTED
        ).pack(anchor="w")

        return value_label

    # ---------- INITIAL REPORT ----------

    def set_initial_report(self):

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")

        self.result_text.insert(
            "end",
            "EMERGENCY EVACUATION SYSTEM\n"
            + "=" * 38
            + "\n\n"
            "Welcome to the evacuation management panel.\n\n"
            "1. Select your current campus location.\n"
            "2. Block any unavailable pathway if required.\n"
            "3. Click FIND EVACUATION ROUTE.\n\n"
            "The system will calculate a route to the "
            "designated safe zone: ASSEMBLY.\n\n"
            "System Status: Ready"
        )

        self.result_text.config(state="disabled")

    # ---------- UPDATE BLOCKED PATHS ----------

    def update_blocked_display(self):

        self.blocked_count.configure(
            text=str(len(self.blocked_paths))
        )

        if not self.blocked_paths:

            self.blocked_label.configure(
                text="No pathways blocked",
                fg=MUTED
            )

        else:

            display_text = "\n".join(
                f"  {index + 1}.  {a}  ↔  {b}"
                for index, (a, b)
                in enumerate(self.blocked_paths)
            )

            self.blocked_label.configure(
                text=display_text,
                fg=RED
            )

    # ---------- BLOCK PATHWAY ----------

    def add_blocked_path(self):

        location_a = self.path_a.get()
        location_b = self.path_b.get()

        if not location_a or not location_b:

            messagebox.showwarning(
                "Missing Selection",
                "Please select both pathway locations."
            )
            return

        if location_a == location_b:

            messagebox.showwarning(
                "Invalid Pathway",
                "Please select two different locations."
            )
            return

        if not self.graph.has_edge(location_a, location_b):

            messagebox.showerror(
                "Invalid Pathway",
                "No direct pathway exists between these locations."
            )
            return

        edge = (location_a, location_b)

        if (
            edge in self.blocked_paths
            or (location_b, location_a) in self.blocked_paths
        ):

            messagebox.showinfo(
                "Already Blocked",
                "This pathway is already blocked."
            )
            return

        self.blocked_paths.append(edge)

        self.update_blocked_display()

        self.path_a.set("")
        self.path_b.set("")

        self.status_badge.configure(
            text="PATHWAY BLOCKED",
            bg=LIGHT_RED,
            fg=RED
        )

    # ---------- FIND EVACUATION ROUTE ----------

    def find_route(self):

        start = self.start_var.get()

        if not start:

            messagebox.showwarning(
                "Missing Location",
                "Please select your current location."
            )
            return

        result = find_evacuation_route(
            start,
            self.blocked_paths
        )

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")

        self.result_text.insert(
            "end",
            "EMERGENCY EVACUATION REPORT\n"
            + "=" * 42
            + "\n\n"
        )

        self.result_text.insert(
            "end",
            f"Current Location : {start}\n"
        )

        self.result_text.insert(
            "end",
            "Designated Safe Zone : ASSEMBLY\n"
        )

        self.result_text.insert(
            "end",
            f"Blocked Pathways : {len(self.blocked_paths)}\n"
        )

        self.result_text.insert(
            "end",
            f"Status : {result.get('status', 'Unknown')}\n\n"
        )

        self.result_text.insert(
            "end",
            f"{result.get('message', '')}\n\n"
        )

        if result.get("path"):

            route = result["path"]

            self.status_badge.configure(
                text="SAFE ROUTE FOUND",
                bg=LIGHT_GREEN,
                fg=GREEN
            )

            self.distance_value.configure(
                text=str(result["distance"])
            )

            self.stops_value.configure(
                text=str(len(route))
            )

            self.result_text.insert(
                "end",
                "RECOMMENDED EVACUATION PATH\n\n"
            )

            for index, location in enumerate(route):

                self.result_text.insert(
                    "end",
                    f"  {index + 1}.  {location}\n"
                )

                if index < len(route) - 1:

                    self.result_text.insert(
                        "end",
                        "        ↓\n"
                    )

            self.result_text.insert(
                "end",
                "\n" + "-" * 42 + "\n\n"
            )

            self.result_text.insert(
                "end",
                f"Total Distance : {result['distance']} meters\n"
            )

            self.result_text.insert(
                "end",
                f"Locations in Route : {len(route)}\n"
            )

            self.result_text.insert(
                "end",
                "\nDestination: ASSEMBLY SAFE ZONE"
            )

        else:

            self.status_badge.configure(
                text="NO SAFE ROUTE",
                bg=LIGHT_RED,
                fg=RED
            )

            self.distance_value.configure(text="--")
            self.stops_value.configure(text="--")

            self.result_text.insert(
                "end",
                "No evacuation route is currently available.\n\n"
                "Please review the blocked pathways and "
                "try again from a different location."
            )

        self.result_text.config(state="disabled")

    # ---------- RESET SYSTEM ----------

    def reset_page(self):

        self.blocked_paths.clear()

        self.start_var.set("COMPUTER_LAB")
        self.path_a.set("")
        self.path_b.set("")

        self.update_blocked_display()

        self.distance_value.configure(text="--")
        self.stops_value.configure(text="--")

        self.status_badge.configure(
            text="WAITING",
            bg=LIGHT_BLUE,
            fg=BLUE
        )

        self.set_initial_report()

    # ---------- SHOW / HIDE ----------

    def show(self):

        self.root.deiconify()

    def hide(self):

        self.root.withdraw()


# ---------- RUN STANDALONE ----------

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "Smart Campus - Emergency Evacuation"
    )

    root.geometry("1250x850")
    root.minsize(1050, 720)

    page = EmergencyPage(root)

    root.mainloop()
