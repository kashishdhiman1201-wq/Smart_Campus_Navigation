import tkinter as tk
from tkinter import ttk, messagebox

import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.graph_builder import create_campus_graph
from algorithms.dijkstra import dijkstra


# ---------- PROFESSIONAL MAP THEME ----------

BG = "#F1F5F9"
WHITE = "#FFFFFF"
NAVY = "#14213D"
TEXT = "#1E293B"
MUTED = "#64748B"
BORDER = "#E2E8F0"

MAP_BG = "#EDF4EA"
ROAD_COLOR = "#FFFFFF"
ROAD_BORDER = "#D5DDD2"
BUILDING_COLOR = "#DCE4EE"
BUILDING_BORDER = "#9AAABD"
GREEN_COLOR = "#C5DEB8"

BLUE = "#2563EB"
BLUE_HOVER = "#1D4ED8"
START_COLOR = "#1677E8"
DESTINATION_COLOR = "#E5484D"
SAFE_COLOR = "#159447"


class CampusMap:

    def __init__(self, parent):

        self.parent = parent
        self.graph = create_campus_graph()
        self.locations = list(self.graph.nodes)

        self.start_location = tk.StringVar(value="MAIN_GATE")
        self.destination = tk.StringVar(value="ASSEMBLY")

        self.route = []
        self.route_distance = None

        self.frame = tk.Frame(parent, bg=BG)

        self.configure_styles()
        self.create_widgets()

    # ---------- STYLES ----------

    def configure_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Campus.TCombobox",
            font=("Segoe UI", 10),
            padding=8,
            fieldbackground=WHITE,
            background=WHITE
        )

    def create_card(self, parent, padding=16):

        return tk.Frame(
            parent,
            bg=WHITE,
            padx=padding,
            pady=padding,
            highlightbackground=BORDER,
            highlightthickness=1
        )

    def create_action_button(
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

    # ---------- USER INTERFACE ----------

    def create_widgets(self):

        # Page heading

        heading = tk.Frame(self.frame, bg=BG)
        heading.pack(fill="x", padx=28, pady=(22, 14))

        tk.Label(
            heading,
            text="Campus Map",
            font=("Segoe UI", 23, "bold"),
            bg=BG,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            heading,
            text="Explore campus buildings, pathways and shortest routes.",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=(4, 0))

        # Top information cards

        info = tk.Frame(self.frame, bg=BG)
        info.pack(fill="x", padx=28, pady=(0, 14))

        info.columnconfigure((0, 1, 2), weight=1)

        self.create_info_card(
            info, 0, "CAMPUS LOCATIONS",
            str(len(self.locations)), "Mapped locations"
        )

        self.create_info_card(
            info, 1, "SAFE ZONE",
            "ASSEMBLY", "Designated evacuation point"
        )

        self.create_info_card(
            info, 2, "ROUTE ALGORITHM",
            "DIJKSTRA", "Shortest-distance pathfinding"
        )

        # Route controls

        controls = self.create_card(self.frame, 18)
        controls.pack(fill="x", padx=28, pady=(0, 14))

        tk.Label(
            controls,
            text="Plan Your Journey",
            font=("Segoe UI", 14, "bold"),
            bg=WHITE,
            fg=NAVY
        ).grid(
            row=0, column=0,
            columnspan=6,
            sticky="w",
            pady=(0, 12)
        )

        tk.Label(
            controls,
            text="START LOCATION",
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).grid(row=1, column=0, sticky="w", padx=(0, 8))

        tk.Label(
            controls,
            text="DESTINATION",
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).grid(row=1, column=1, sticky="w", padx=8)

        self.start_box = ttk.Combobox(
            controls,
            textvariable=self.start_location,
            values=self.locations,
            state="readonly",
            style="Campus.TCombobox",
            width=22
        )

        self.start_box.grid(
            row=2, column=0,
            sticky="ew",
            padx=(0, 8),
            pady=(6, 0)
        )

        self.destination_box = ttk.Combobox(
            controls,
            textvariable=self.destination,
            values=self.locations,
            state="readonly",
            style="Campus.TCombobox",
            width=22
        )

        self.destination_box.grid(
            row=2, column=1,
            sticky="ew",
            padx=8,
            pady=(6, 0)
        )

        self.create_action_button(
            controls,
            "FIND ROUTE",
            self.find_route
        ).grid(
            row=2, column=2,
            padx=(12, 6),
            pady=(6, 0)
        )

        self.create_action_button(
            controls,
            "RESET MAP",
            self.reset_map,
            bg="#E8EEF6",
            hover="#D9E4F2",
            fg=TEXT
        ).grid(
            row=2, column=3,
            padx=6,
            pady=(6, 0)
        )

        controls.columnconfigure(0, weight=1)
        controls.columnconfigure(1, weight=1)

        # Map panel

        map_card = self.create_card(self.frame, 10)

        map_card.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=(0, 12)
        )

        map_header = tk.Frame(map_card, bg=WHITE)
        map_header.pack(fill="x", padx=8, pady=(2, 8))

        tk.Label(
            map_header,
            text="Campus Layout",
            font=("Segoe UI", 14, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(side="left")

        tk.Label(
            map_header,
            text="ILLUSTRATIVE CAMPUS GRAPH",
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(side="right")

        plot_frame = tk.Frame(
            map_card,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        plot_frame.pack(fill="both", expand=True)

        self.figure, self.ax = plt.subplots(
            figsize=(11, 6.2),
            dpi=100
        )

        self.figure.patch.set_facecolor(WHITE)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=plot_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        # Bottom status and legend

        bottom = tk.Frame(self.frame, bg=BG)

        bottom.pack(
            fill="x",
            padx=28,
            pady=(0, 18)
        )

        status_card = self.create_card(bottom, 12)
        status_card.pack(fill="x")

        status_top = tk.Frame(status_card, bg=WHITE)
        status_top.pack(fill="x")

        tk.Label(
            status_top,
            text="ROUTE STATUS",
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(side="left")

        self.status_badge = tk.Label(
            status_top,
            text="READY",
            font=("Segoe UI", 8, "bold"),
            bg="#EFF6FF",
            fg=BLUE,
            padx=10,
            pady=4
        )

        self.status_badge.pack(side="right")

        self.result_label = tk.Label(
            status_card,
            text="Select locations and click FIND ROUTE.",
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=TEXT,
            anchor="w",
            justify="left",
            wraplength=1000
        )

        self.result_label.pack(
            fill="x",
            pady=(9, 10)
        )

        legend = tk.Frame(status_card, bg=WHITE)
        legend.pack(fill="x")

        self.add_legend_item(legend, START_COLOR, "Start")
        self.add_legend_item(legend, DESTINATION_COLOR, "Destination")
        self.add_legend_item(legend, SAFE_COLOR, "Safe Zone")
        self.add_legend_item(legend, BLUE, "Selected Route")
        self.add_legend_item(legend, ROAD_BORDER, "Pathway")

        self.draw_map()

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

    def add_legend_item(self, parent, color, label):

        item = tk.Frame(parent, bg=WHITE)
        item.pack(side="left", padx=(0, 18))

        tk.Label(
            item,
            text="●",
            font=("Segoe UI", 11, "bold"),
            bg=WHITE,
            fg=color
        ).pack(side="left")

        tk.Label(
            item,
            text=label,
            font=("Segoe UI", 8),
            bg=WHITE,
            fg=MUTED
        ).pack(side="left", padx=(4, 0))

    # ---------- MAP DRAWING ----------

    def draw_map(self):

        self.ax.clear()
        self.ax.set_facecolor(MAP_BG)

        positions = {
            node: (
                self.graph.nodes[node]["x"],
                self.graph.nodes[node]["y"]
            )
            for node in self.graph.nodes
        }

        xs = [position[0] for position in positions.values()]
        ys = [position[1] for position in positions.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        x_range = max(max_x - min_x, 1)
        y_range = max(max_y - min_y, 1)

        radius = min(x_range, y_range) * 0.055

        # Campus background

        self.ax.fill(
            [min_x - 1, max_x + 1, max_x + 1, min_x - 1],
            [min_y - 1, min_y - 1, max_y + 1, max_y + 1],
            color=MAP_BG,
            zorder=0
        )

        # Decorative green spaces

        self.ax.add_patch(
            Circle(
                (min_x + x_range * 0.45, max_y - y_range * 0.12),
                radius=radius,
                color=GREEN_COLOR,
                alpha=0.75,
                zorder=1
            )
        )

        self.ax.add_patch(
            Circle(
                (min_x + x_range * 0.72, min_y + y_range * 0.15),
                radius=radius * 0.85,
                color=GREEN_COLOR,
                alpha=0.75,
                zorder=1
            )
        )

        # Pathways

        for u, v, data in self.graph.edges(data=True):

            x1, y1 = positions[u]
            x2, y2 = positions[v]

            blocked = data.get("blocked", False)

            self.ax.plot(
                [x1, x2],
                [y1, y2],
                color=ROAD_BORDER,
                linewidth=13,
                solid_capstyle="round",
                zorder=2
            )

            self.ax.plot(
                [x1, x2],
                [y1, y2],
                color="#E35A52" if blocked else ROAD_COLOR,
                linewidth=9,
                linestyle="--" if blocked else "-",
                solid_capstyle="round",
                zorder=3
            )

        # Highlight selected route

        if self.route:

            for u, v in zip(self.route, self.route[1:]):

                x1, y1 = positions[u]
                x2, y2 = positions[v]

                self.ax.plot(
                    [x1, x2],
                    [y1, y2],
                    color=BLUE,
                    linewidth=5,
                    solid_capstyle="round",
                    zorder=4
                )

        # Buildings and location markers

        for node, (x, y) in positions.items():

            is_start = node == self.start_location.get()
            is_destination = node == self.destination.get()
            is_safe = node == "ASSEMBLY"

            building = FancyBboxPatch(
                (x - 0.29, y - 0.22),
                0.58,
                0.44,
                boxstyle="round,pad=0.06,rounding_size=0.06",
                facecolor=BUILDING_COLOR,
                edgecolor=BUILDING_BORDER,
                linewidth=1.2,
                zorder=5
            )

            self.ax.add_patch(building)

            if is_start:
                marker_color = START_COLOR
                marker_text = "S"

            elif is_destination:
                marker_color = DESTINATION_COLOR
                marker_text = "D"

            elif is_safe:
                marker_color = SAFE_COLOR
                marker_text = "✓"

            else:
                marker_color = "#52769C"
                marker_text = ""

            self.ax.scatter(
                x,
                y + 0.32,
                s=205,
                color=marker_color,
                edgecolors=WHITE,
                linewidths=1.7,
                zorder=7
            )

            if marker_text:

                self.ax.text(
                    x,
                    y + 0.32,
                    marker_text,
                    color=WHITE,
                    fontsize=9,
                    fontweight="bold",
                    ha="center",
                    va="center",
                    zorder=8
                )

            self.ax.text(
                x,
                y - 0.02,
                node.replace("_", " "),
                fontsize=7,
                fontweight="bold",
                color="#25364A",
                ha="center",
                va="center",
                zorder=8
            )

        self.ax.set_title(
            "SMART CAMPUS  |  NAVIGATION NETWORK",
            fontsize=14,
            fontweight="bold",
            color=NAVY,
            pad=14
        )

        self.ax.set_xlim(min_x - 0.85, max_x + 0.85)
        self.ax.set_ylim(min_y - 0.85, max_y + 0.85)

        self.ax.set_aspect("equal", adjustable="datalim")
        self.ax.axis("off")

        self.figure.tight_layout(pad=1.5)
        self.canvas.draw_idle()

    # ---------- ROUTE CALCULATION ----------

    def find_route(self):

        start = self.start_location.get()
        destination = self.destination.get()

        if not start or not destination:

            messagebox.showwarning(
                "Missing Selection",
                "Please select both start and destination."
            )
            return

        if start == destination:

            messagebox.showwarning(
                "Invalid Selection",
                "Start and destination must be different."
            )
            return

        result = dijkstra(
            self.graph,
            start,
            destination
        )

        if result["status"] == "Success":

            self.route = result["path"]
            self.route_distance = result["distance"]

            self.status_badge.configure(
                text="ROUTE FOUND",
                bg="#DCFCE7",
                fg="#15803D"
            )

            self.result_label.configure(
                text=(
                    f"{'  →  '.join(self.route)}"
                    f"     |     Distance: "
                    f"{result['distance']} meters"
                ),
                fg=BLUE
            )

        else:

            self.route = []
            self.route_distance = None

            self.status_badge.configure(
                text="NO ROUTE",
                bg="#FEE2E2",
                fg="#B91C1C"
            )

            self.result_label.configure(
                text="No available route found between the selected locations.",
                fg="#B91C1C"
            )

        self.draw_map()

    # ---------- RESET MAP ----------

    def reset_map(self):

        self.route = []
        self.route_distance = None

        self.start_location.set("MAIN_GATE")
        self.destination.set("ASSEMBLY")

        self.status_badge.configure(
            text="READY",
            bg="#EFF6FF",
            fg=BLUE
        )

        self.result_label.configure(
            text="Map reset. Select locations to find a route.",
            fg=TEXT
        )

        self.draw_map()

    # ---------- SHOW / HIDE ----------

    def show(self):

        self.frame.pack(fill="both", expand=True)

    def hide(self):

        self.frame.pack_forget()


# ---------- RUN STANDALONE MAP ----------

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Smart Campus Navigation Map")
    root.geometry("1250x850")
    root.minsize(1000, 720)

    campus_map = CampusMap(root)
    campus_map.show()

    root.mainloop()