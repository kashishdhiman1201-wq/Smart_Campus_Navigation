
import tkinter as tk
from tkinter import ttk


# ---------------- THEME COLORS ----------------

BG = "#F3F6FC"
WHITE = "#FFFFFF"
NAVY = "#14213D"
BLUE = "#356AE6"
GREEN = "#16A36A"
PURPLE = "#805AD5"
TEXT = "#263449"
MUTED = "#718096"
BORDER = "#E5EAF2"


class AboutPage:

    def __init__(self, root):
        self.root = root
        self.setup_style()
        self.setup_ui()

    # ---------------- STYLE ----------------

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "About.Vertical.TScrollbar",
            background="#DCE4F0",
            troughcolor=BG,
            bordercolor=BG,
            arrowcolor=NAVY
        )

    # ---------------- SCROLLABLE PAGE ----------------

    def setup_ui(self):

        self.root.configure(bg=BG)

        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            container,
            bg=BG,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview,
            style="About.Vertical.TScrollbar"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.main_frame = tk.Frame(
            self.canvas,
            bg=BG
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.main_frame,
            anchor="nw"
        )

        self.main_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.update_canvas_width
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        self.build_content()

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def update_canvas_width(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    def on_mousewheel(self, event):

        if self.root.winfo_exists():

            self.canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

    # ---------------- REUSABLE CARD ----------------

    def create_card(self, parent, title, accent=BLUE):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        tk.Frame(
            card,
            bg=accent,
            height=4
        ).pack(fill="x")

        content = tk.Frame(
            card,
            bg=WHITE
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=17
        )

        tk.Label(
            content,
            text=title,
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(anchor="w", pady=(0, 12))

        return card, content

    # ---------------- SECTION ITEM ----------------

    def add_item(self, parent, text):

        row = tk.Frame(
            parent,
            bg=WHITE
        )

        row.pack(
            fill="x",
            anchor="w",
            pady=5
        )

        tk.Label(
            row,
            text="●",
            font=("Segoe UI", 8),
            bg=WHITE,
            fg=BLUE
        ).pack(
            side="left",
            anchor="n",
            padx=(0, 9),
            pady=3
        )

        tk.Label(
            row,
            text=text,
            font=("Segoe UI", 10),
            bg=WHITE,
            fg=TEXT,
            justify="left",
            anchor="w",
            wraplength=480
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

    # ---------------- CONTENT ----------------

    def build_content(self):

        main = self.main_frame

        main.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=22
        )

        # HEADER

        header = tk.Frame(main, bg=BG)
        header.pack(fill="x", pady=(0, 20))

        title_area = tk.Frame(header, bg=BG)
        title_area.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_area,
            text="About Smart Campus Navigation",
            font=("Segoe UI", 22, "bold"),
            bg=BG,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            title_area,
            text="Project Information and System Architecture",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            header,
            text="MCA  |  DAA PROJECT",
            font=("Segoe UI", 9, "bold"),
            bg="#EAF0FF",
            fg=BLUE,
            padx=14,
            pady=9
        ).pack(side="right", anchor="n")

        # PROJECT OVERVIEW

        overview_card, overview_content = self.create_card(
            main,
            "Project Overview",
            BLUE
        )

        overview_card.pack(
            fill="x",
            pady=(0, 17)
        )

        tk.Label(
            overview_content,
            text="Smart Campus Navigation and Emergency Evacuation System",
            font=("Segoe UI", 15, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(anchor="w", pady=(0, 10))

        intro_text = (
            "Smart Campus Navigation and Emergency Evacuation System "
            "is a graph-based application designed to provide efficient "
            "navigation inside a university campus.\n\n"

            "The system represents campus locations as graph nodes and "
            "pathways as weighted edges. It calculates suitable routes "
            "between locations and helps users find alternative paths "
            "when a pathway becomes unavailable.\n\n"

            "It also provides an emergency evacuation feature to guide "
            "users towards a designated safe zone. The application "
            "demonstrates the practical use of graph data structures "
            "and graph traversal and shortest-path algorithms."
        )

        tk.Label(
            overview_content,
            text=intro_text,
            font=("Segoe UI", 10),
            bg=WHITE,
            fg=TEXT,
            justify="left",
            anchor="w",
            wraplength=1100
        ).pack(fill="x")

        # PROJECT STATISTICS

        stats_frame = tk.Frame(main, bg=BG)
        stats_frame.pack(fill="x", pady=(0, 17))

        statistics = [
            ("15", "Campus Locations", BLUE),
            ("25", "Pathways", GREEN),
            ("4", "Algorithms", PURPLE)
        ]

        for value, label, accent in statistics:

            card = tk.Frame(
                stats_frame,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 12)
            )

            inner = tk.Frame(card, bg=WHITE)
            inner.pack(
                fill="both",
                padx=17,
                pady=13
            )

            tk.Label(
                inner,
                text=value,
                font=("Segoe UI", 23, "bold"),
                bg=WHITE,
                fg=accent
            ).pack(anchor="w")

            tk.Label(
                inner,
                text=label.upper(),
                font=("Segoe UI", 9, "bold"),
                bg=WHITE,
                fg=MUTED
            ).pack(anchor="w", pady=(3, 0))

        # OBJECTIVES AND FEATURES

        content_frame = tk.Frame(main, bg=BG)
        content_frame.pack(
            fill="x",
            pady=(0, 17)
        )

        objectives_card, objectives_content = self.create_card(
            content_frame,
            "Project Objectives",
            BLUE
        )

        objectives_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        objectives = [
            "Find shortest routes between campus locations.",
            "Provide alternative routes when pathways are blocked.",
            "Support emergency evacuation towards a safe zone.",
            "Compare the performance of different algorithms.",
            "Display campus pathways through a visual map."
        ]

        for item in objectives:
            self.add_item(objectives_content, item)

        features_card, features_content = self.create_card(
            content_frame,
            "Key Features",
            GREEN
        )

        features_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        features = [
            "Interactive campus navigation.",
            "Shortest path calculation.",
            "Blocked pathway simulation.",
            "Emergency evacuation routing.",
            "Algorithm performance visualization."
        ]

        for item in features:
            self.add_item(features_content, item)

        # ALGORITHMS AND TECHNOLOGIES

        bottom_frame = tk.Frame(main, bg=BG)
        bottom_frame.pack(
            fill="x",
            pady=(0, 17)
        )

        algorithm_card, algorithm_content = self.create_card(
            bottom_frame,
            "Algorithms Implemented",
            PURPLE
        )

        algorithm_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        algorithms = [
            "Dijkstra's Shortest Path Algorithm",
            "A* Search Algorithm",
            "Breadth-First Search (BFS)",
            "Depth-First Search (DFS)"
        ]

        for item in algorithms:
            self.add_item(algorithm_content, item)

        technology_card, technology_content = self.create_card(
            bottom_frame,
            "Technologies Used",
            BLUE
        )

        technology_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        technologies = [
            "Python Programming Language",
            "Tkinter for GUI Development",
            "NetworkX for Graph Representation",
            "Matplotlib for Visualization",
            "Pandas and NumPy for Data Analysis"
        ]

        for item in technologies:
            self.add_item(technology_content, item)

        # SYSTEM WORKFLOW

        workflow_card, workflow_content = self.create_card(
            main,
            "System Workflow",
            GREEN
        )

        workflow_card.pack(
            fill="x",
            pady=(0, 17)
        )

        workflow = [
            ("01", "Campus Graph", "Represent locations and pathways as a weighted graph."),
            ("02", "Route Calculation", "Apply graph algorithms to calculate routes."),
            ("03", "Pathway Management", "Simulate blocked pathways and alternative routes."),
            ("04", "Emergency Evacuation", "Find a route towards the designated safe zone."),
            ("05", "Performance Analysis", "Compare algorithm execution time and explored nodes.")
        ]

        for number, heading, description in workflow:

            row = tk.Frame(
                workflow_content,
                bg=WHITE
            )

            row.pack(
                fill="x",
                pady=6
            )

            tk.Label(
                row,
                text=number,
                font=("Segoe UI", 10, "bold"),
                bg="#EAF0FF",
                fg=BLUE,
                width=4,
                pady=7
            ).pack(side="left", padx=(0, 12))

            text_frame = tk.Frame(row, bg=WHITE)
            text_frame.pack(
                side="left",
                fill="x",
                expand=True
            )

            tk.Label(
                text_frame,
                text=heading,
                font=("Segoe UI", 10, "bold"),
                bg=WHITE,
                fg=NAVY
            ).pack(anchor="w")

            tk.Label(
                text_frame,
                text=description,
                font=("Segoe UI", 9),
                bg=WHITE,
                fg=MUTED,
                wraplength=850,
                justify="left"
            ).pack(anchor="w", pady=(2, 0))

        # FOOTER

        footer = tk.Frame(
            main,
            bg=NAVY
        )

        footer.pack(
            fill="x",
            pady=(0, 8)
        )

        tk.Label(
            footer,
            text="SMART CAMPUS NAVIGATION",
            font=("Segoe UI", 12, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(pady=(15, 4))

        tk.Label(
            footer,
            text="Smart Campus Navigation and Emergency Evacuation System",
            font=("Segoe UI", 9),
            bg=NAVY,
            fg="#CBD5E1"
        ).pack(pady=(0, 5))

        tk.Label(
            footer,
            text="MCA Project | Design and Analysis of Algorithms",
            font=("Segoe UI", 9),
            bg=NAVY,
            fg="#CBD5E1"
        ).pack(pady=(0, 15))

    # ---------------- SHOW / HIDE ----------------

    def show(self):
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()


# ---------------- STANDALONE RUN ----------------

if __name__ == "__main__":

    root = tk.Tk()

    root.title("About Smart Campus Navigation")
    root.geometry("1200x850")
    root.minsize(950, 650)

    page = AboutPage(root)

    root.mainloop()
