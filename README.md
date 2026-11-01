# Smart Campus Navigation and Emergency Evacuation System

## Project Overview

The **Smart Campus Navigation and Emergency Evacuation System** is a Python-based desktop application developed as an academic project for the subject **Design and Analysis of Algorithm (DAA)**.

The system represents a campus environment as an undirected weighted graph, where locations are represented as vertices and pathways are represented as edges. Each edge contains an approximate distance value.

The application helps users explore campus locations, calculate shortest routes, visualize the campus graph, and identify emergency evacuation routes using graph-based algorithms.

## Objectives

- To represent campus locations and pathways using graph theory.
- To implement shortest-path algorithms.
- To demonstrate graph traversal techniques.
- To provide an emergency evacuation route feature.
- To visualize campus pathways and algorithm results.
- To compare the behavior of different algorithms.

## Key Features

- Campus map visualization using graph representation.
- Shortest path calculation using Dijkstra's Algorithm.
- Heuristic-based route finding using A* Search.
- Graph traversal using Breadth-First Search (BFS).
- Graph traversal using Depth-First Search (DFS).
- Emergency evacuation route planning.
- Algorithm performance comparison.
- Interactive graphical user interface using Tkinter.
- Modular project structure for better code organization.

## Algorithms Implemented

| Algorithm | Purpose |
|---|---|
| Dijkstra's Algorithm | Finds the shortest weighted path |
| A* Search | Uses path cost and heuristic estimation |
| BFS | Performs breadth-first graph traversal |
| DFS | Performs depth-first graph traversal |

## Campus Graph Information

The predefined campus model contains:

- **15 campus locations**
- **25 connecting pathways**
- **2 designated emergency exit locations**
- **1 designated safe assembly location**

The graph uses approximate pathway distances as edge weights.

## Technologies Used

- Python
- Tkinter
- NetworkX
- Matplotlib
- NumPy
- Pandas
- Heapq
- Time

## Project Structure

```text
Smart_Campus_Navigation/
│
├── algorithms/
│   ├── dijkstra.py
│   ├── a_star.py
│   ├── bfs_dfs.py
│   └── performance_comparison.py
│
├── data/
│   └── campus_data.py
│
├── gui/
│   ├── dashboard.py
│   ├── navigation_page.py
│   ├── campus_map.py
│   ├── emergency_page.py
│   ├── algorithm_analysis_page.py
│   └── about_page.py
│
├── modules/
│   ├── graph_builder.py
│   └── emergency_evacuation.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kashishdhiman1201-wq/Smart_Campus_Navigation.git
```

### 2. Open the Project Directory

```bash
cd Smart_Campus_Navigation
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

## Application Modules

**1. Dashboard:** Provides access to the main features of the application.

**2. Navigation:** Allows users to select campus locations and calculate routes.

**3. Campus Map:** Displays the campus graph and connecting pathways.

**4. Emergency Evacuation:** Provides an evacuation route towards the designated safe location.

**5. Algorithm Analysis:** Provides information for comparing implemented algorithms.

**6. About:** Displays project-related information.

## Learning Outcomes

Through this project, the following concepts were explored:

- Graph data structures.
- Weighted and undirected graphs.
- Greedy algorithms.
- Heuristic search.
- Priority queues.
- BFS and DFS traversal.
- Algorithm performance analysis.
- Python GUI development.
- Modular programming.

## Limitations

- The campus environment uses predefined data.
- Live GPS tracking is not integrated.
- Real-time sensor data is not available.
- Dynamic obstacle detection is not implemented.
- Pathway distances are based on stored values.

## Future Scope

The project can be extended with live GPS integration, dynamic route updates, real-time emergency notifications, mobile application support, voice-based navigation, and intelligent route analysis.

## Academic Information

| Detail | Information |
|---|---|
| Project Title | Smart Campus Navigation and Emergency Evacuation System |
| Student Name | Kashish Dhiman |
| UID | 26MCI10292 |
| Programme | MCA (AI-ML) |
| Section | 26 MAM 5A |
| Subject | Design and Analysis of Algorithm |
| Subject Code | 26CAP-612 |
| University | Chandigarh University |

## Author

**Kashish Dhiman**

GitHub: [kashishdhiman1201-wq](https://github.com/kashishdhiman1201-wq)

## Repository

[Smart Campus Navigation and Emergency Evacuation System – GitHub Repository](https://github.com/kashishdhiman1201-wq/Smart_Campus_Navigation)
