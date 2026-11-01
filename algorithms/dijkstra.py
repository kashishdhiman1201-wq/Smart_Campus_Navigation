
# ============================================================
# SMART CAMPUS NAVIGATION & EMERGENCY EVACUATION SYSTEM
# Module: Dijkstra's Shortest Path Algorithm
# ============================================================

import heapq
import time


# ------------------------------------------------------------
# 1. DIJKSTRA'S SHORTEST PATH ALGORITHM
# ------------------------------------------------------------

def dijkstra(graph, start, destination):

    start_time = time.perf_counter()

    # Validate source and destination
    if start not in graph or destination not in graph:

        return {
            "path": [],
            "distance": float("inf"),
            "visited_nodes": [],
            "execution_time": 0,
            "status": "Invalid location"
        }

    # Initialize distances
    distances = {
        node: float("inf")
        for node in graph.nodes()
    }

    previous = {
        node: None
        for node in graph.nodes()
    }

    distances[start] = 0

    # Priority Queue (Min Heap)
    priority_queue = [(0, start)]

    visited = []
    finalized = set()

    # Main Dijkstra loop
    while priority_queue:

        current_distance, current_node = heapq.heappop(
            priority_queue
        )

        # Ignore outdated heap entries
        if current_distance != distances[current_node]:
            continue

        # Ignore already finalized nodes
        if current_node in finalized:
            continue

        finalized.add(current_node)
        visited.append(current_node)

        # Destination reached
        if current_node == destination:
            break

        # Explore connected locations
        for neighbor in graph.neighbors(current_node):

            edge_data = graph[current_node][neighbor]

            # Ignore blocked pathways
            if edge_data["blocked"]:
                continue

            # Calculate new distance
            new_distance = (
                current_distance + edge_data["distance"]
            )

            # Update if shorter path is found
            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance

                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    # Check whether destination is reachable
    if distances[destination] == float("inf"):

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

    # Reconstruct shortest path
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
        "distance": distances[destination],
        "visited_nodes": visited,
        "execution_time": execution_time,
        "status": "Success"
    }


# ------------------------------------------------------------
# 2. DISPLAY ROUTE DETAILS
# ------------------------------------------------------------

def display_route(graph, result):

    print("\nDIJKSTRA ROUTE ANALYSIS")
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
# 3. TEST DIJKSTRA ALGORITHM
# ------------------------------------------------------------

if __name__ == "__main__":

    from modules.graph_builder import (
        create_campus_graph,
        block_path
    )

    campus_graph = create_campus_graph()

    # Test 1: Normal shortest route
    print("\nTEST 1: NORMAL CAMPUS NAVIGATION")

    result = dijkstra(
        campus_graph,
        "MAIN_GATE",
        "COMPUTER_LAB"
    )

    display_route(campus_graph, result)

    # Test 2: Emergency blocked path
    print("\n\nTEST 2: EMERGENCY ROUTE")

    block_path(
        campus_graph,
        "MAIN_GATE",
        "ADMIN"
    )

    emergency_result = dijkstra(
        campus_graph,
        "MAIN_GATE",
        "COMPUTER_LAB"
    )

    display_route(campus_graph, emergency_result)
