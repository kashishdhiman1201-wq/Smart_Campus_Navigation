
import tkinter as tk
from tkinter import ttk, messagebox

from modules.graph_builder import create_campus_graph
from algorithms.dijkstra import dijkstra
from algorithms.a_star import a_star


# ---------- COLORS ----------

BG = "#F1F5F9"
WHITE = "#FFFFFF"
NAVY = "#14213D"
BLUE = "#2563EB"
BLUE_HOVER = "#1D4ED8"
TEXT = "#1E293B"
MUTED = "#64748B"
BORDER = "#E2E8F0"
GREEN = "#15803D"
LIGHT_GREEN = "#DCFCE7"
LIGHT_BLUE = "#EFF6FF"
LIGHT_GRAY = "#F8FAFC"


class NavigationPage:

    def __init__(self, parent):

        self.parent = parent
        self.graph = create_campus_graph()
        self.frame = tk.Frame(parent, bg=BG)

        self.locations = list(self.graph.nodes)

        self.create_widgets()

    # ---------- HELPER FUNCTIONS ----------

    def create_card(self, parent, padding=20):

        return tk.Frame(
            parent,
            bg=WHITE,
            padx=padding,
            pady=padding,
            highlightbackground=BORDER,
            highlightthickness=1
        )

    def create_label(self, parent, text, size=10,
                     color=TEXT, bold=False):

        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", size, "bold" if bold else "normal"),
            bg=WHITE,
            fg=color
        )

    def create_button(self, parent, text, command,
                      bg=BLUE, hover=BLUE_HOVER):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=bg,
            fg=WHITE,
            activebackground=hover,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            padx=18,
            pady=11,
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

    # ---------- MAIN PAGE ----------

    def create_widgets(self):

        # Header

        header = tk.Frame(self.frame, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 15))

        tk.Label(
            header,
            text="Campus Navigation",
            font=("Segoe UI", 23, "bold"),
            bg=BG,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Find the shortest and most efficient route "
                 "between campus locations.",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=(5, 0))

        # Information Cards

        info_frame = tk.Frame(self.frame, bg=BG)
        info_frame.pack(fill="x", padx=30, pady=(0, 18))

        info_frame.columnconfigure((0, 1, 2), weight=1)

        self.create_info_card(
            info_frame, 0, "CAMPUS LOCATIONS",
            str(len(self.locations)), "Available locations"
        )

        self.create_info_card(
            info_frame, 1, "PATHFINDING ALGORITHMS",
            "02", "Dijkstra and A*"
        )

        self.create_info_card(
            info_frame, 2, "ROUTE TYPE",
            "SHORTEST", "Distance-based routing"
        )

        # Main Content

        content = tk.Frame(self.frame, bg=BG)
        content.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        content.columnconfigure(0, weight=4)
        content.columnconfigure(1, weight=6)
        content.rowconfigure(0, weight=1)

        # Left: Route Selection

        selection_card = self.create_card(content, 22)
        selection_card.grid(
            row=0, column=0,
            sticky="nsew",
            padx=(0, 12)
        )

        self.create_label(
            selection_card,
            "Plan Your Route",
            16, NAVY, True
        ).pack(anchor="w")

        self.create_label(
            selection_card,
            "Choose your starting point and destination.",
            9, MUTED
        ).pack(anchor="w", pady=(5, 22))

        # Starting Location

        self.create_label(
            selection_card,
            "STARTING LOCATION",
            9, TEXT, True
        ).pack(anchor="w")

        self.start_box = ttk.Combobox(
            selection_card,
            values=self.locations,
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.start_box.pack(fill="x", pady=(8, 20))
        self.start_box.set(self.locations[0])

        # Destination

        self.create_label(
            selection_card,
            "DESTINATION",
            9, TEXT, True
        ).pack(anchor="w")

        self.destination_box = ttk.Combobox(
            selection_card,
            values=self.locations,
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.destination_box.pack(fill="x", pady=(8, 20))
        self.destination_box.set(self.locations[-1])

        # Algorithm

        self.create_label(
            selection_card,
            "SELECT ALGORITHM",
            9, TEXT, True
        ).pack(anchor="w")

        self.algorithm_box = ttk.Combobox(
            selection_card,
            values=["Dijkstra", "A*"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.algorithm_box.pack(fill="x", pady=(8, 22))
        self.algorithm_box.set("Dijkstra")

        # Buttons

        self.create_button(
            selection_card,
            "FIND SHORTEST ROUTE",
            self.find_route
        ).pack(fill="x", pady=(0, 10))

        reset_button = tk.Button(
            selection_card,
            text="RESET SELECTION",
            command=self.reset_page,
            font=("Segoe UI", 9, "bold"),
            bg=LIGHT_BLUE,
            fg=BLUE,
            activebackground="#DBEAFE",
            activeforeground=BLUE,
            relief="flat",
            bd=0,
            pady=10,
            cursor="hand2"
        )
        reset_button.pack(fill="x")

        # Right: Results

        result_card = self.create_card(content, 22)
        result_card.grid(
            row=0, column=1,
            sticky="nsew",
            padx=(12, 0)
        )

        result_header = tk.Frame(result_card, bg=WHITE)
        result_header.pack(fill="x")

        self.create_label(
            result_header,
            "Route Results",
            16, NAVY, True
        ).pack(side="left")

        self.status_label = tk.Label(
            result_header,
            text="WAITING",
            font=("Segoe UI", 8, "bold"),
            bg=LIGHT_BLUE,
            fg=BLUE,
            padx=12,
            pady=5
        )
        self.status_label.pack(side="right")

        self.create_label(
            result_card,
            "Your calculated route and performance details.",
            9, MUTED
        ).pack(anchor="w", pady=(5, 18))

        # Metric Cards

        metrics = tk.Frame(result_card, bg=WHITE)
        metrics.pack(fill="x", pady=(0, 18))

        metrics.columnconfigure((0, 1, 2), weight=1)

        self.distance_value = self.create_metric(
            metrics, 0, "DISTANCE", "--", "meters"
        )

        self.visited_value = self.create_metric(
            metrics, 1, "VISITED NODES", "--", "nodes"
        )

        self.time_value = self.create_metric(
            metrics, 2, "EXECUTION TIME", "--", "milliseconds"
        )

        # Route Details

        self.create_label(
            result_card,
            "CALCULATED PATH",
            9, TEXT, True
        ).pack(anchor="w", pady=(0, 8))

        route_frame = tk.Frame(
            result_card,
            bg=LIGHT_GRAY,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        route_frame.pack(fill="both", expand=True)

        self.result_text = tk.Text(
            route_frame,
            font=("Segoe UI", 10),
            bg=LIGHT_GRAY,
            fg=TEXT,
            relief="flat",
            bd=0,
            wrap="word",
            padx=15,
            pady=15,
            height=10,
            spacing1=4,
            spacing3=4
        )

        scrollbar = ttk.Scrollbar(
            route_frame,
            orient="vertical",
            command=self.result_text.yview
        )

        self.result_text.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(side="right", fill="y")
        self.result_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.result_text.insert(
            "end",
            "Welcome to Campus Navigation!\n\n"
            "Select a starting location and destination.\n"
            "Choose Dijkstra or A* algorithm and click "
            "FIND SHORTEST ROUTE to calculate your path."
        )

        self.result_text.config(state="disabled")

    # ---------- INFORMATION CARDS ----------

    def create_info_card(self, parent, column,
                         heading, value, description):

        card = tk.Frame(
            parent,
            bg=WHITE,
            padx=18,
            pady=14,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6
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
            font=("Segoe UI", 17, "bold"),
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

    def create_metric(self, parent, column,
                      heading, value, unit):

        card = tk.Frame(
            parent,
            bg=LIGHT_BLUE,
            padx=10,
            pady=12
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
            font=("Segoe UI", 7, "bold"),
            bg=LIGHT_BLUE,
            fg=MUTED
        ).pack(anchor="w")

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 16, "bold"),
            bg=LIGHT_BLUE,
            fg=BLUE
        )
        value_label.pack(anchor="w", pady=4)

        tk.Label(
            card,
            text=unit,
            font=("Segoe UI", 8),
            bg=LIGHT_BLUE,
            fg=MUTED
        ).pack(anchor="w")

        return value_label

    # ---------- FIND ROUTE ----------

    def find_route(self):

        start = self.start_box.get()
        destination = self.destination_box.get()
        algorithm = self.algorithm_box.get()

        if not start or not destination:
            messagebox.showwarning(
                "Missing Selection",
                "Please select both starting location "
                "and destination."
            )
            return

        if start == destination:
            messagebox.showwarning(
                "Invalid Selection",
                "Starting location and destination "
                "must be different."
            )
            return

        if algorithm not in ["Dijkstra", "A*"]:
            messagebox.showwarning(
                "Invalid Algorithm",
                "Please select a valid algorithm."
            )
            return

        if algorithm == "Dijkstra":
            result = dijkstra(
                self.graph, start, destination
            )
        else:
            result = a_star(
                self.graph, start, destination
            )

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")

        self.result_text.insert(
            "end",
            "CAMPUS ROUTE ANALYSIS\n"
            + "=" * 45 + "\n\n"
        )

        self.result_text.insert(
            "end", f"Algorithm       : {algorithm}\n"
        )
        self.result_text.insert(
            "end", f"Starting Point  : {start}\n"
        )
        self.result_text.insert(
            "end", f"Destination     : {destination}\n"
        )
        self.result_text.insert(
            "end", f"Route Status    : {result['status']}\n\n"
        )

        if result["status"] == "Success":

            path = result["path"]

            self.status_label.configure(
                text="ROUTE FOUND",
                bg=LIGHT_GREEN,
                fg=GREEN
            )

            self.distance_value.configure(
                text=str(result["distance"])
            )

            self.visited_value.configure(
                text=str(result["visited_nodes"])
            )

            self.time_value.configure(
                text=f"{result['execution_time'] * 1000:.4f}"
            )

            self.result_text.insert(
                "end", "OPTIMAL ROUTE\n\n"
            )

            for index, location in enumerate(path):

                self.result_text.insert(
                    "end",
                    f"  {index + 1}.  {location}\n"
                )

                if index < len(path) - 1:
                    self.result_text.insert(
                        "end", "        ↓\n"
                    )

            self.result_text.insert(
                "end",
                "\n" + "-" * 45 + "\n\n"
            )

            self.result_text.insert(
                "end",
                f"Total Distance : {result['distance']} meters\n"
            )

            self.result_text.insert(
                "end",
                f"Visited Nodes  : {result['visited_nodes']}\n"
            )

            self.result_text.insert(
                "end",
                f"Execution Time : "
                f"{result['execution_time'] * 1000:.4f} ms\n"
            )

        else:

            self.status_label.configure(
                text="NO ROUTE FOUND",
                bg="#FEE2E2",
                fg="#B91C1C"
            )

            self.distance_value.configure(text="--")
            self.visited_value.configure(text="--")
            self.time_value.configure(text="--")

            self.result_text.insert(
                "end",
                "\nNo route found between the selected "
                "locations.\n\n"
                "Please check the selected locations "
                "or pathway availability."
            )

        self.result_text.config(state="disabled")

    # ---------- RESET PAGE ----------

    def reset_page(self):

        self.start_box.set(self.locations[0])
        self.destination_box.set(self.locations[-1])
        self.algorithm_box.set("Dijkstra")

        self.distance_value.configure(text="--")
        self.visited_value.configure(text="--")
        self.time_value.configure(text="--")

        self.status_label.configure(
            text="WAITING",
            bg=LIGHT_BLUE,
            fg=BLUE
        )

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")

        self.result_text.insert(
            "end",
            "Selections have been reset.\n\n"
            "Choose your locations and algorithm "
            "to calculate a new route."
        )

        self.result_text.config(state="disabled")

    # ---------- SHOW / HIDE ----------

    def show(self):

        self.frame.pack(fill="both", expand=True)

    def hide(self):

        self.frame.pack_forget()
