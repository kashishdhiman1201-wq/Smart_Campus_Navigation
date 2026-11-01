
import tkinter as tk
from tkinter import ttk, messagebox
import traceback
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algorithms.performance_comparison import compare_algorithms


# ---------------- THEME COLORS ----------------

BG = "#F3F6FC"
WHITE = "#FFFFFF"
NAVY = "#14213D"
BLUE = "#356AE6"
LIGHT_BLUE = "#EAF0FF"
GREEN = "#16A36A"
LIGHT_GREEN = "#E9F8F0"
TEXT = "#263449"
MUTED = "#718096"
BORDER = "#E5EAF2"


class AlgorithmAnalysisPage:

    def __init__(self, root):
        self.root = root
        self.last_df = None
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
            "Analysis.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=34,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Analysis.Treeview.Heading",
            background="#EAF0F7",
            foreground=NAVY,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=9
        )

        style.map(
            "Analysis.Treeview",
            background=[("selected", LIGHT_BLUE)],
            foreground=[("selected", NAVY)]
        )

    # ---------------- MAIN UI ----------------

    def setup_ui(self):

        self.root.configure(bg=BG)

        main_frame = tk.Frame(self.root, bg=BG)
        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # HEADER

        header = tk.Frame(main_frame, bg=BG)
        header.pack(fill="x", pady=(0, 18))

        title_area = tk.Frame(header, bg=BG)
        title_area.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_area,
            text="Algorithm Performance Analysis",
            font=("Segoe UI", 22, "bold"),
            bg=BG,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            title_area,
            text="Evaluate and compare graph algorithms used in campus navigation",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=(5, 0))

        self.status_label = tk.Label(
            header,
            text="●  NOT RUN",
            font=("Segoe UI", 9, "bold"),
            bg="#FFF5E8",
            fg="#B7791F",
            padx=13,
            pady=8
        )
        self.status_label.pack(side="right", anchor="n")

        # CONTROL CARD

        control_card = tk.Frame(
            main_frame,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        control_card.pack(fill="x", pady=(0, 16))

        control_inner = tk.Frame(control_card, bg=WHITE)
        control_inner.pack(fill="x", padx=18, pady=14)

        tk.Label(
            control_inner,
            text="Performance Testing",
            font=("Segoe UI", 12, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(side="left")

        self.run_button = tk.Button(
            control_inner,
            text="▶  Run Performance Analysis",
            command=self.run_analysis,
            bg=BLUE,
            fg=WHITE,
            activebackground="#2855C7",
            activeforeground=WHITE,
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=10,
            relief="flat",
            cursor="hand2"
        )
        self.run_button.pack(side="right")

        # SUMMARY CARDS

        summary_frame = tk.Frame(main_frame, bg=BG)
        summary_frame.pack(fill="x", pady=(0, 16))

        self.summary_values = {}

        cards = [
            ("ALGORITHMS TESTED", "0", BLUE),
            ("FASTEST EXECUTION", "N/A", GREEN),
            ("TOTAL NODES VISITED", "0", "#805AD5")
        ]

        for heading, value, accent in cards:

            card = tk.Frame(
                summary_frame,
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

            tk.Frame(
                card,
                bg=accent,
                height=4
            ).pack(fill="x")

            inner = tk.Frame(card, bg=WHITE)
            inner.pack(fill="both", padx=16, pady=11)

            tk.Label(
                inner,
                text=heading,
                font=("Segoe UI", 8, "bold"),
                bg=WHITE,
                fg=MUTED
            ).pack(anchor="w")

            value_label = tk.Label(
                inner,
                text=value,
                font=("Segoe UI", 18, "bold"),
                bg=WHITE,
                fg=accent
            )
            value_label.pack(anchor="w", pady=(5, 0))

            self.summary_values[heading] = value_label

        # COMPARISON TABLE

        table_card = tk.Frame(
            main_frame,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        table_card.pack(fill="x", pady=(0, 16))

        table_header = tk.Frame(table_card, bg=WHITE)
        table_header.pack(fill="x", padx=18, pady=(14, 9))

        tk.Label(
            table_header,
            text="Algorithm Comparison",
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            table_header,
            text="Measured performance results",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(3, 0))

        self.table_container = tk.Frame(table_card, bg=WHITE)
        self.table_container.pack(
            fill="x",
            padx=15,
            pady=(0, 14)
        )

        self.tree = ttk.Treeview(
            self.table_container,
            show="headings",
            height=5,
            style="Analysis.Treeview"
        )

        vertical_scroll = ttk.Scrollbar(
            self.table_container,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal_scroll = ttk.Scrollbar(
            self.table_container,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")

        self.table_container.grid_columnconfigure(0, weight=1)

        # CHART CARD

        chart_card = tk.Frame(
            main_frame,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        chart_card.pack(fill="both", expand=True)

        chart_header = tk.Frame(chart_card, bg=WHITE)
        chart_header.pack(fill="x", padx=18, pady=(13, 3))

        tk.Label(
            chart_header,
            text="Performance Visualization",
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            chart_header,
            text="Visual comparison of execution time and visited nodes",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(3, 0))

        # Figure height and spacing adjusted

        self.figure = Figure(
            figsize=(10, 3.5),
            dpi=100,
            facecolor=WHITE
        )

        self.ax1 = self.figure.add_subplot(121)
        self.ax2 = self.figure.add_subplot(122)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=chart_card
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        self.show_empty_charts()

    # ---------------- CHART FORMATTING ----------------

    def format_charts(self):

        self.figure.subplots_adjust(
            left=0.08,
            right=0.98,
            top=0.84,
            bottom=0.30,
            wspace=0.30
        )

        for ax in [self.ax1, self.ax2]:

            ax.set_facecolor(WHITE)

            ax.grid(
                axis="y",
                linestyle="--",
                alpha=0.25
            )

            ax.set_axisbelow(True)

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

            ax.tick_params(
                axis="x",
                labelsize=9,
                pad=7
            )

            ax.tick_params(
                axis="y",
                labelsize=9
            )

    # ---------------- EMPTY CHARTS ----------------

    def show_empty_charts(self):

        self.ax1.clear()
        self.ax2.clear()

        self.ax1.set_title(
            "Execution Time",
            fontsize=12,
            fontweight="bold",
            color=NAVY,
            pad=12
        )

        self.ax1.set_xlabel("Algorithms")
        self.ax1.set_ylabel("Time (milliseconds)")

        self.ax2.set_title(
            "Visited Nodes",
            fontsize=12,
            fontweight="bold",
            color=NAVY,
            pad=12
        )

        self.ax2.set_xlabel("Algorithms")
        self.ax2.set_ylabel("Number of Nodes")

        self.format_charts()
        self.canvas.draw()

    # ---------------- RUN ANALYSIS ----------------

    def run_analysis(self):

        try:

            self.run_button.config(state="disabled")
            self.root.update_idletasks()

            df = compare_algorithms()

            if df is None or df.empty:

                messagebox.showwarning(
                    "No Data",
                    "No performance data was returned."
                )
                return

            self.last_df = df.copy()

            self.display_table(df)
            self.display_charts(df)
            self.update_summary(df)

            self.status_label.config(
                text="●  ANALYSIS COMPLETED",
                bg=LIGHT_GREEN,
                fg=GREEN
            )

        except Exception as error:

            traceback.print_exc()

            self.status_label.config(
                text="●  ANALYSIS FAILED",
                bg="#FDECEC",
                fg="#C53030"
            )

            messagebox.showerror(
                "Analysis Error",
                f"Unable to run analysis:\n{error}"
            )

        finally:

            self.run_button.config(state="normal")

    # ---------------- SUMMARY CARDS ----------------

    def update_summary(self, df):

        display_df = df.copy()

        if display_df.index.name is not None:
            display_df = display_df.reset_index()

        columns = list(display_df.columns)

        time_col = next(
            (
                col for col in columns
                if "execution" in str(col).lower()
                or "time" in str(col).lower()
            ),
            None
        )

        visited_col = next(
            (
                col for col in columns
                if "visited" in str(col).lower()
                or "nodes" in str(col).lower()
            ),
            None
        )

        algorithm_col = next(
            (
                col for col in columns
                if "algorithm" in str(col).lower()
                or "method" in str(col).lower()
            ),
            None
        )

        # Number of algorithms

        if algorithm_col is not None:

            count = display_df[algorithm_col].nunique()

        else:

            count = len(display_df)

        self.summary_values["ALGORITHMS TESTED"].config(
            text=str(count)
        )

        # Fastest execution

        self.summary_values["FASTEST EXECUTION"].config(
            text="N/A"
        )

        if time_col is not None:

            times = pd.to_numeric(
                display_df[time_col],
                errors="coerce"
            )

            valid_times = times.dropna()

            if not valid_times.empty:

                fastest_index = valid_times.idxmin()

                if algorithm_col is not None:

                    fastest_name = str(
                        display_df.loc[
                            fastest_index,
                            algorithm_col
                        ]
                    )

                else:

                    fastest_name = "Available result"

                self.summary_values["FASTEST EXECUTION"].config(
                    text=fastest_name
                )

        # Total visited nodes

        self.summary_values["TOTAL NODES VISITED"].config(
            text="0"
        )

        if visited_col is not None:

            visited = pd.to_numeric(
                display_df[visited_col],
                errors="coerce"
            ).dropna()

            if not visited.empty:

                total = int(visited.sum())

                self.summary_values["TOTAL NODES VISITED"].config(
                    text=str(total)
                )

    # ---------------- DISPLAY TABLE ----------------

    def display_table(self, df):

        for item in self.tree.get_children():
            self.tree.delete(item)

        display_df = df.copy()

        if display_df.index.name is not None:
            display_df = display_df.reset_index()

        columns = list(display_df.columns)

        self.tree["columns"] = columns

        for column in columns:

            heading = str(column).replace(
                "_", " "
            ).title()

            self.tree.heading(
                column,
                text=heading
            )

            self.tree.column(
                column,
                width=180,
                minwidth=120,
                anchor="center"
            )

        for _, row in display_df.iterrows():

            values = []

            for value in row.tolist():

                if pd.api.types.is_scalar(value):

                    if pd.isna(value):
                        values.append("N/A")
                    else:
                        values.append(str(value))

                else:
                    values.append(str(value))

            self.tree.insert(
                "",
                "end",
                values=values
            )

    # ---------------- DISPLAY CHARTS ----------------

    def display_charts(self, df):

        display_df = df.copy()

        if display_df.index.name is not None:
            display_df = display_df.reset_index()

        columns = list(display_df.columns)

        # Algorithm column

        algorithm_col = next(
            (
                col for col in columns
                if "algorithm" in str(col).lower()
                or "method" in str(col).lower()
            ),
            None
        )

        if algorithm_col is not None:

            labels = display_df[
                algorithm_col
            ].astype(str).tolist()

        else:

            labels = [
                str(i)
                for i in range(len(display_df))
            ]

        # Time column

        time_col = next(
            (
                col for col in columns
                if "execution" in str(col).lower()
                or "time" in str(col).lower()
            ),
            None
        )

        # Visited nodes column

        visited_col = next(
            (
                col for col in columns
                if "visited" in str(col).lower()
                or "nodes" in str(col).lower()
            ),
            None
        )

        self.ax1.clear()
        self.ax2.clear()

        # EXECUTION TIME CHART

        if time_col is not None:

            times = pd.to_numeric(
                display_df[time_col],
                errors="coerce"
            )

            valid = times.notna()

            if valid.any():

                chart_labels = [
                    labels[i]
                    for i in range(len(labels))
                    if valid.iloc[i]
                ]

                chart_values = times[valid].tolist()

                bars = self.ax1.bar(
                    chart_labels,
                    chart_values,
                    color=BLUE,
                    width=0.55
                )

                self.ax1.bar_label(
                    bars,
                    fmt="%.3f",
                    padding=4,
                    fontsize=8
                )

                self.ax1.tick_params(
                    axis="x",
                    rotation=20
                )

            else:

                self.ax1.text(
                    0.5,
                    0.5,
                    "No numeric time data",
                    ha="center",
                    va="center",
                    transform=self.ax1.transAxes
                )

        else:

            self.ax1.text(
                0.5,
                0.5,
                "Execution time data unavailable",
                ha="center",
                va="center",
                transform=self.ax1.transAxes
            )

        # VISITED NODES CHART

        if visited_col is not None:

            visited = pd.to_numeric(
                display_df[visited_col],
                errors="coerce"
            )

            valid = visited.notna()

            if valid.any():

                chart_labels = [
                    labels[i]
                    for i in range(len(labels))
                    if valid.iloc[i]
                ]

                chart_values = visited[valid].tolist()

                bars = self.ax2.bar(
                    chart_labels,
                    chart_values,
                    color=GREEN,
                    width=0.55
                )

                self.ax2.bar_label(
                    bars,
                    padding=4,
                    fontsize=8
                )

                self.ax2.tick_params(
                    axis="x",
                    rotation=20
                )

            else:

                self.ax2.text(
                    0.5,
                    0.5,
                    "No numeric node data",
                    ha="center",
                    va="center",
                    transform=self.ax2.transAxes
                )

        else:

            self.ax2.text(
                0.5,
                0.5,
                "Visited node data unavailable",
                ha="center",
                va="center",
                transform=self.ax2.transAxes
            )

        # CHART TITLES AND LABELS

        self.ax1.set_title(
            "Execution Time",
            fontsize=12,
            fontweight="bold",
            color=NAVY,
            pad=12
        )

        self.ax1.set_xlabel("Algorithms")
        self.ax1.set_ylabel("Time (milliseconds)")

        self.ax2.set_title(
            "Visited Nodes",
            fontsize=12,
            fontweight="bold",
            color=NAVY,
            pad=12
        )

        self.ax2.set_xlabel("Algorithms")
        self.ax2.set_ylabel("Number of Nodes")

        self.format_charts()
        self.canvas.draw()

    # ---------------- SHOW / HIDE ----------------

    def show(self):
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()


# ---------------- STANDALONE RUN ----------------

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "Smart Campus - Algorithm Analysis"
    )

    root.geometry("1200x850")
    root.minsize(950, 700)

    page = AlgorithmAnalysisPage(root)

    root.mainloop()
