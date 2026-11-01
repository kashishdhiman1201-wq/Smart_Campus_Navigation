
# ============================================================
# SMART CAMPUS NAVIGATION & EMERGENCY EVACUATION SYSTEM
# Module: A* Search Algorithm
# ============================================================

import heapq
import math
import time


# ------------------------------------------------------------
# 1. HEURISTIC SCALE CALCULATION
# ------------------------------------------------------------

def calculate_heuristic_scale(graph):

    scale = float("inf")

    for u, v, data in graph.edges(data=True):

        u_data = graph.nodes[u]
        v_data = graph.nodes[v]

        dx = u_data["x"] - v_data["x"]
        dy = u_data["y"] - v_data["y"]

        straight_distance = math.sqrt(dx**2 + dy**2)

        if straight_distance > 0:

            ratio = data["distance"] / straight_distance

            scale = min(scale, ratio)

    if scale == float("inf"):
        return 0

    return scale


# ------------------------------------------------------------
# 2. HEURISTIC FUNCTION
# ------------------------------------------------------------

def heuristic(graph, current, destination, scale):

    current_data = graph.nodes[current]
    destination_data = graph.nodes[destination]

    dx = current_data["x"] - destination_data["x"]
    dy = current_data["y"] - destination_data["y"]

    straight_distance = math.sqrt(dx**2 + dy**2)

    return straight_distance * scale


# ------------------------------------------------------------
# 3. A* SEARCH ALGORITHM
# ------------------------------------------------------------

def a_star(graph, start, destination):

    start_time = time.perf_counter()

    # Validate locations
    if start not in graph or destination not in graph:

        return {
            "path": [],
            "distance": float("inf"),
            "visited_nodes": [],
            "execution_time": 0,
            "status": "Invalid location"
        }

    # Same source and destination
    if start == destination:

        return {
            "path": [start],
            "distance": 0,
            "visited_nodes": [start],
            "execution_time": 0,
            "status": "Success"
        }

    scale = calculate_heuristic_scale(graph)

    # Initialize actual distances
    g_score = {
        node: float("inf")
        for node in graph.nodes()
    }

    previous = {
        node: None
        for node in graph.nodes()
    }

    g_score[start] = 0

    # Priority Queue: (f_score, g_score, node)
    start_h = heuristic(graph, start, destination, scale)

    open_set = [(start_h, 0, start)]

    visited = []
    finalized = set()

    # Main A* loop
    while open_set:

        f_score, current_g, current = heapq.heappop(
            open_set
        )

        # Ignore outdated entries
        if current_g != g_score[current]:
            continue

        if current in finalized:
            continue

        finalized.add(current)
        visited.append(current)

        # Destination reached
        if current == destination:
            break

        # Explore neighboring locations
        for neighbor in graph.neighbors(current):

            edge_data = graph[current][neighbor]

            # Ignore blocked pathways
            if edge_data["blocked"]:
                continue

            tentative_g = (
                g_score[current] + edge_data["distance"]
            )

            # Update better route
            if tentative_g < g_score[neighbor]:

                g_score[neighbor] = tentative_g

                previous[neighbor] = current

                h_score = heuristic(
                    graph,
                    neighbor,
                    destination,
                    scale
                )

                new_f = tentative_g + h_score

                heapq.heappush(
                    open_set,
                    (new_f, tentative_g, neighbor)
                )

    # Check destination reachability
    if g_score[destination] == float("inf"):

        execution_time = (
            time.perf_counter() - start_time
        ) * 1000

        return {
            "path": [],
            "distance": float("inf"),
            "visited_nodes": visited,
            "execution_time": execution_time,
            "status": "No route available"
        }

    # Reconstruct path
    path = []
    current = destination

    while current is not None:

        path.append(current)
        current = previous[current]

    path.reverse()

    execution_time = (
        time.perf_counter() - start_time
    ) * 1000

    return {
        "path": path,
        "distance": g_score[destination],
        "visited_nodes": visited,
        "execution_time": execution_time,
        "status": "Success"
    }


# ------------------------------------------------------------
# 4. DISPLAY ROUTE DETAILS
# ------------------------------------------------------------

def display_route(graph, result):

    print("\nA* ROUTE ANALYSIS")
    print("=" * 45)

    if result["status"] != "Success":

        print("Status:", result["status"])
        return

    readable_path = [
        graph.nodes[node]["name"]
        for node in result["path"]
    ]

    print("Shortest Route:")
    print(" -> ".join(readable_path))

    print("\nTotal Distance:",
          result["distance"], "meters")

    print("Visited Nodes:",
          len(result["visited_nodes"]))

    print("Execution Time:",
          round(result["execution_time"], 5), "ms")

    print("Status:", result["status"])


# ------------------------------------------------------------
# 5. TEST A* ALGORITHM
# ------------------------------------------------------------

if __name__ == "__main__":

    from modules.graph_builder import (
        create_campus_graph,
        block_path
    )

    campus_graph = create_campus_graph()

    # Test 1: Normal navigation
    print("\nTEST 1: NORMAL CAMPUS NAVIGATION")

    result = a_star(
        campus_graph,
        "MAIN_GATE",
        "COMPUTER_LAB"
    )

    display_route(campus_graph, result)

    # Test 2: Emergency navigation
    print("\n\nTEST 2: EMERGENCY ROUTE")

    block_path(
        campus_graph,
        "MAIN_GATE",
        "ADMIN"
    )

    emergency_result = a_star(
        campus_graph,
        "MAIN_GATE",
        "COMPUTER_LAB"
    )

    display_route(campus_graph, emergency_result)
