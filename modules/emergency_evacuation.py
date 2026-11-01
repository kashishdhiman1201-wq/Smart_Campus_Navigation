
from modules.graph_builder import create_campus_graph
from algorithms.dijkstra import dijkstra


SAFE_ZONE = "ASSEMBLY"


def block_emergency_path(graph, location1, location2):
    """Mark a campus pathway as blocked during an emergency."""

    if not graph.has_edge(location1, location2):
        print("Invalid pathway:", location1, "-", location2)
        return False

    graph[location1][location2]["blocked"] = True
    print("Path blocked:", location1, "-", location2)
    return True


def find_evacuation_route(start_location, blocked_paths=None):

    graph = create_campus_graph()

    # Block unsafe pathways
    if blocked_paths:
        for location1, location2 in blocked_paths:
            block_emergency_path(graph, location1, location2)

    # Validate starting location
    if start_location not in graph:
        return {
            "status": "Failed",
            "message": "Starting location does not exist."
        }

    if start_location == SAFE_ZONE:
        return {
            "status": "Success",
            "path": [SAFE_ZONE],
            "distance": 0,
            "message": "You are already at the safe zone."
        }

    # Find shortest available route to safe zone
    result = dijkstra(graph, start_location, SAFE_ZONE)

    if result["status"] != "Success":
        return {
            "status": "Failed",
            "message": "No safe evacuation route available."
        }

    return {
        "status": "Success",
        "path": result["path"],
        "distance": result["distance"],
        "message": "Safe evacuation route found."
    }


def display_evacuation_route(result):

    print("\n========== EMERGENCY EVACUATION ==========")

    print("Status:", result["status"])
    print("Message:", result["message"])

    if result["status"] == "Success":
        print("Evacuation Route:")
        print(" -> ".join(result["path"]))

        print("Total Distance:", result["distance"], "meters")

    print("===========================================")


if __name__ == "__main__":

    # Test 1: Normal evacuation
    print("\nTEST 1: NORMAL EVACUATION")

    result = find_evacuation_route("COMPUTER_LAB")
    display_evacuation_route(result)

    # Test 2: Evacuation with a blocked pathway
    print("\nTEST 2: BLOCKED PATH EVACUATION")

    blocked = [("COMPUTER_LAB", "BLOCK_A")]

    result = find_evacuation_route(
        "COMPUTER_LAB",
        blocked
    )

    display_evacuation_route(result)
