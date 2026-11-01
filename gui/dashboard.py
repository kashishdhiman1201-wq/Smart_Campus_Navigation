import tkinter as tk
from tkinter import ttk

from gui.navigation_page import NavigationPage
from gui.campus_map import CampusMap
from gui.emergency_page import EmergencyPage
from gui.algorithm_analysis_page import AlgorithmAnalysisPage
from gui.about_page import AboutPage


# ---------- COLOR THEME ----------
BG = "#F1F5F9"
SIDEBAR = "#14213D"
PRIMARY = "#2563EB"
WHITE = "#FFFFFF"
TEXT = "#1E293B"
MUTED = "#64748B"
ACTIVE_BLUE = "#1D4ED8"


# ---------- WINDOW SETTINGS ----------
root = tk.Tk()
root.title("Smart Campus Navigation & Emergency Evacuation System")
root.geometry("1200x750")
root.minsize(1000, 650)
root.configure(bg=BG)


#---------- PAGE NAVIGATION FUNCTIONS ----------
def open_navigation():
    navigation_window = tk.Toplevel(root)
    navigation_window.title("Campus Navigation")
    navigation_window.geometry("1000x700")
    navigation_window.configure(bg=BG)
    page = NavigationPage(navigation_window)
    page.show()


def open_campus_map():
    map_window = tk.Toplevel(root)
    map_window.title("Smart Campus Map")
    map_window.geometry("1200x850")
    map_window.minsize(950, 700)
    page = CampusMap(map_window)
    page.show()


def open_emergency():
    emergency_window = tk.Toplevel(root)
    emergency_window.title("Emergency Evacuation")
    emergency_window.geometry("1000x750")
    page = EmergencyPage(emergency_window)
    page.show()


def open_algorithm_analysis():
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Algorithm Performance Analysis")
    analysis_window.geometry("1150x800")
    page = AlgorithmAnalysisPage(analysis_window)
    page.show()


def open_about():
    about_window = tk.Toplevel(root)
    about_window.title("About Smart Campus Navigation")
    about_window.geometry("1150x800")
    page = AboutPage(about_window)
    page.show()


# ---------- SIDEBAR ----------
sidebar = tk.Frame(root, bg=SIDEBAR, width=240)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

logo = tk.Label(
    sidebar, text="CAMPUS NAV",
    font=("Segoe UI", 19, "bold"),
    bg=SIDEBAR, fg=WHITE
)
logo.pack(pady=(30, 5))

subtitle = tk.Label(
    sidebar, text="SMART NAVIGATION SYSTEM",
    font=("Segoe UI", 8),
    bg=SIDEBAR, fg="#94A3B8"
)
subtitle.pack(pady=(0, 35))


# ---------- SIDEBAR ACTIVE AND HOVER EFFECTS ----------
active_button = None


def on_enter(event):
    if event.widget != active_button:
        event.widget.configure(bg=PRIMARY, fg=WHITE)  


def on_leave(event):
    if event.widget == active_button:
        event.widget.configure(bg=ACTIVE_BLUE, fg=WHITE)
    else:
        event.widget.configure(bg=SIDEBAR, fg=WHITE)


def select_menu(button):
    global active_button

    if active_button is not None:
        active_button.configure(bg=SIDEBAR, fg=WHITE)

    active_button = button
    active_button.configure(bg=ACTIVE_BLUE, fg=WHITE)


menu_items = [
    "Dashboard",
    "Campus Navigation",
    "Campus Map",
    "Emergency Evacuation",
    "Algorithm Analysis",
    "About Project"
]

page_actions = {
    "Campus Navigation": open_navigation,
    "Campus Map": open_campus_map,
    "Emergency Evacuation": open_emergency,
    "Algorithm Analysis": open_algorithm_analysis,
    "About Project": open_about
}

for item in menu_items:
    action = page_actions.get(item)

    btn = tk.Button(
        sidebar,
        text="   " + item,
        font=("Segoe UI", 11),
        bg=SIDEBAR,
        fg=WHITE,
        activebackground=PRIMARY,
        activeforeground=WHITE,
        relief="flat",
        anchor="w",
        padx=15,
        pady=13,
        cursor="hand2"
    )

    btn.configure(
        command=lambda b=btn, a=action: (
            select_menu(b),
            a() if a is not None else None
        )
    )

    btn.pack(fill="x", padx=12, pady=3)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    if item == "Dashboard":
        select_menu(btn)


# ---------- MAIN CONTENT ----------
main_area = tk.Frame(root, bg=BG)
main_area.pack(side="left", fill="both", expand=True)

# Header
header = tk.Frame(main_area, bg=WHITE, height=85)
header.pack(fill="x")
header.pack_propagate(False)

heading = tk.Label(
    header, text="Smart Campus Dashboard",
    font=("Segoe UI", 22, "bold"),
    bg=WHITE, fg=TEXT
)
heading.pack(side="left", padx=30, pady=20)

status = tk.Label(
    header, text="● SYSTEM ONLINE",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE, fg="#16A34A"
)
status.pack(side="right", padx=30)


# Welcome section
welcome = tk.Frame(main_area, bg=BG)
welcome.pack(fill="x", padx=30, pady=25)

tk.Label(
    welcome, text="Welcome to Smart Campus Navigation",
    font=("Segoe UI", 17, "bold"),
    bg=BG, fg=TEXT
).pack(anchor="w")

tk.Label(
    welcome,
    text="Navigate campus locations and manage emergency routes efficiently.",
    font=("Segoe UI", 10),
    bg=BG, fg=MUTED
).pack(anchor="w", pady=6)


# ---------- STATISTICS CARDS ----------
stats_frame = tk.Frame(main_area, bg=BG)
stats_frame.pack(fill="x", padx=25, pady=10)

stats = [
    ("15", "Campus Locations"),
    ("25", "Pathways"),
    ("4", "Algorithms"),
    ("2", "Emergency Exits")
]

for value, label in stats:
    card = tk.Frame(
        stats_frame, bg=WHITE, padx=20, pady=22,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    card.pack(side="left", fill="both", expand=True, padx=7)

    tk.Label(
        card, text=value,
        font=("Segoe UI", 25, "bold"),
        bg=WHITE, fg=PRIMARY
    ).pack(anchor="w")

    tk.Label(
        card, text=label,
        font=("Segoe UI", 10),
        bg=WHITE, fg=MUTED
    ).pack(anchor="w", pady=(5, 0))


    # ---------- DASHBOARD CONTENT ----------
content = tk.Frame(main_area, bg=BG)
content.pack(fill="both", expand=True, padx=30, pady=15)

tk.Label(
    content, text="Quick Access",
    font=("Segoe UI", 17, "bold"),
    bg=BG, fg=TEXT
).pack(anchor="w", pady=(0, 12))

quick_frame = tk.Frame(content, bg=BG)
quick_frame.pack(fill="x")

quick_actions = [
    ("🧭", "Campus Navigation", "Find the shortest campus route", open_navigation),
    ("🗺", "Campus Map", "Explore campus locations", open_campus_map),
    ("🚨", "Emergency Evacuation", "Find a safe evacuation route", open_emergency),
    ("📊", "Algorithm Analysis", "Compare algorithm performance", open_algorithm_analysis)
]

for emoji, title_text, description, action in quick_actions:
    card = tk.Frame(
        quick_frame, bg=WHITE, padx=18, pady=17,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    card.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(
        card, text=emoji,
        font=("Segoe UI Emoji", 22),
        bg=WHITE
    ).pack(anchor="w")

    tk.Label(
        card, text=title_text,
        font=("Segoe UI", 11, "bold"),
        bg=WHITE, fg=TEXT
    ).pack(anchor="w", pady=(8, 4))

    tk.Label(
        card, text=description,
        font=("Segoe UI", 9),
        bg=WHITE, fg=MUTED,
        wraplength=190,
        justify="left"
    ).pack(anchor="w")

    tk.Button(
        card, text="Open →",
        font=("Segoe UI", 9, "bold"),
        bg="#EFF6FF", fg=PRIMARY,
        activebackground="#DBEAFE",
        relief="flat",
        cursor="hand2",
        command=action
    ).pack(anchor="w", pady=(12, 0))


# ---------- LOWER INFORMATION SECTION ----------
lower_frame = tk.Frame(content, bg=BG)
lower_frame.pack(fill="both", expand=True, pady=(22, 0))

overview = tk.Frame(
    lower_frame, bg=WHITE, padx=22, pady=20,
    highlightbackground="#E2E8F0",
    highlightthickness=1
)
overview.pack(side="left", fill="both", expand=True, padx=(5, 10))

tk.Label(
    overview, text="About the System",
    font=("Segoe UI", 15, "bold"),
    bg=WHITE, fg=TEXT
).pack(anchor="w")

tk.Label(
    overview,
    text=(
        "Smart Campus Navigation is a graph-based application "
        "designed to simplify campus navigation and emergency "
        "evacuation.\n\n"
        "It uses Dijkstra and A* for shortest-path calculation, "
        "BFS and DFS for graph traversal, and provides an "
        "interactive campus map and route analysis."
    ),
    font=("Segoe UI", 10),
    bg=WHITE, fg=MUTED,
    wraplength=530,
    justify="left"
).pack(anchor="w", pady=15)


system_panel = tk.Frame(
    lower_frame, bg=WHITE, padx=22, pady=20,
    highlightbackground="#E2E8F0",
    highlightthickness=1
)
system_panel.pack(side="right", fill="both", expand=True, padx=(10, 5))

tk.Label(
    system_panel, text="System Information",
    font=("Segoe UI", 15, "bold"),
    bg=WHITE, fg=TEXT
).pack(anchor="w", pady=(0, 15))

system_details = [
    ("Application Status", "ONLINE", "#16A34A"),
    ("Campus Locations", "15 Registered", PRIMARY),
    ("Pathways", "25 Connected", PRIMARY),
    ("Emergency Safe Zone", "ASSEMBLY", "#16A34A")
]

for label_text, value_text, value_color in system_details:
    row = tk.Frame(system_panel, bg=WHITE)
    row.pack(fill="x", pady=9)

    tk.Label(
        row, text=label_text,
        font=("Segoe UI", 10),
        bg=WHITE, fg=MUTED
    ).pack(side="left")

    tk.Label(
        row, text=value_text,
        font=("Segoe UI", 10, "bold"),
        bg=WHITE, fg=value_color
    ).pack(side="right")


# ---------- RUN APPLICATION ----------
if __name__ == "__main__":
    root.mainloop()
