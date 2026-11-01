
# ============================================================
# SMART CAMPUS NAVIGATION & EMERGENCY EVACUATION SYSTEM
# Module: BFS and DFS Graph Traversal
# ============================================================

from collections import deque
import time


# ------------------------------------------------------------
# 1. BREADTH FIRST SEARCH (BFS)
# ------------------------------------------------------------

def bfs(graph, start):

    start_time = time.perf_counter()

    if start not in graph:
        return {
            "traversal": [],
            "execution_time": 0,
            "status": "Invalid location"
        }

    visited = set()
    traversal = []

    # Queue for level-wise exploration
    queue = deque([start])

    visited.add(start)

    while queue:

        current = queue.popleft()

        traversal.append(current)

        # Explore neighboring locations
        for neighbor in graph.neighbors(current):

            if neighbor in visited:
                continue

            if graph[current][neighbor]["blocked"]:
                continue

            visited.add(neighbor)
            queue.append(neighbor)

    execution_time = (
        time.perf_counter() - start_time
    ) * 1000

    return {
        "traversal": traversal,
        "execution_time": execution_time,
        "status": "Success"
    }


# ------------------------------------------------------------
# 2. DEPTH FIRST SEARCH (DFS)
# ------------------------------------------------------------

def dfs(graph, start):

    start_time = time.perf_counter()

    if start not in graph:
        return {
            "traversal": [],
            "execution_time": 0,
            "status": "Invalid location"
        }

    visited = set()
    traversal = []

    # Stack for depth-wise exploration
    stack = [start]

    while stack:

        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        traversal.append(current)

        # Reverse maintains a consistent traversal order
        neighbors = list(graph.neighbors(current))

        for neighbor in reversed(neighbors):

            if neighbor in visited:
                continue

            if graph[current][neighbor]["blocked"]:
                continue

            stack.append(neighbor)

    execution_time = (
        time.perf_counter() - start_time
    ) * 1000

    return {
        "traversal": traversal,
        "execution_time": execution_time,
        "status": "Success"
    }


# ------------------------------------------------------------
# 3. DISPLAY TRAVERSAL RESULTS
# ------------------------------------------------------------

def display_traversal(graph, result, algorithm_name):

    print("\n" + algorithm_name + " RESULTS")
    print("=" * 45)

    if result["status"] != "Success":

        print("Status:", result["status"])
        return

    readable_locations = [
        graph.nodes[node]["name"]
        for node in result["traversal"]
    ]

    print("Traversal Order:")

    print(" -> ".join(readable_locations))

    print("\nTotal Visited Locations:",
          len(result["traversal"]))

    print("Execution Time:",
          round(result["execution_time"], 5), "ms")

    print("Status:", result["status"])


# ------------------------------------------------------------
# 4. TEST BFS AND DFS
# ------------------------------------------------------------

if __name__ == "__main__":

    from modules.graph_builder import (
        create_campus_graph,
        block_path
    )

    campus_graph = create_campus_graph()

    # BFS Test
    print("\nTEST 1: BREADTH FIRST SEARCH")

    bfs_result = bfs(
        campus_graph,
        "MAIN_GATE"
    )

    display_traversal(
        campus_graph,
        bfs_result,
        "BFS"
    )

    # DFS Test
    print("\nTEST 2: DEPTH FIRST SEARCH")

    dfs_result = dfs(
        campus_graph,
        "MAIN_GATE"
    )

    display_traversal(
        campus_graph,
        dfs_result,
        "DFS"
    )

    # Emergency blocked-path test
    print("\nTEST 3: EMERGENCY TRAVERSAL")

    block_path(
        campus_graph,
        "MAIN_GATE",
        "ADMIN"
    )

    emergency_result = bfs(
        campus_graph,
        "MAIN_GATE"
    )

    display_traversal(
        campus_graph,
        emergency_result,
        "BFS - EMERGENCY"
    )
