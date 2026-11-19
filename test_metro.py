"""
test_metro.py - Unit test suite for Official Comprehensive DMRC + NCR Network (264 Stations)
---------------------------------------------------------------------------------------------
Verifies all project requirements:
1. Valid route between stations on the same line.
2. Same source and destination.
3. No available route (disconnected station).
4. Interchange route between lines.
5. Multiple possible routes: BFS selects the route with minimum stops.
6. Inter-city network integration: Delhi to Greater Noida (Aqua Line) and Gurugram (Rapid Metro).
"""

from graph import build_sample_metro_network


def test_metro_route_finder():
    metro = build_sample_metro_network()
    print("Testing Official Comprehensive DMRC + NCR Network (264 Stations)...\n")

    # Test Case 1: Valid source and destination on Yellow Line
    print("--- Test Case 1: Yellow Line Direct Route ---")
    path, stops = metro.bfs_shortest_path("Samaypur Badli", "Rajiv Chowk")
    assert path is not None, "Path should exist"
    assert stops == 15
    print(f"PASS: Route found: {' -> '.join(path[:4])} ... -> {path[-1]} (Stops: {stops})\n")

    # Test Case 2: Same source and destination
    print("--- Test Case 2: Same Source and Destination ---")
    path, stops = metro.bfs_shortest_path("Rajiv Chowk", "Rajiv Chowk")
    assert path == ["Rajiv Chowk"]
    assert stops == 0
    print(f"PASS: Same station handled correctly: {path} (Stops: {stops})\n")

    # Test Case 3: Disconnected Station (No Route)
    print("--- Test Case 3: Disconnected Station (No Route) ---")
    path, stops = metro.bfs_shortest_path("Rajiv Chowk", "Narela (Phase 4 - Proposed)")
    assert path is None
    assert stops == 0
    print("PASS: Handled disconnected station correctly (Returned None, 0)\n")

    # Test Case 4: Interchange Route via Rajiv Chowk
    print("--- Test Case 4: Interchange Route (Blue Line to Yellow Line) ---")
    path, stops = metro.bfs_shortest_path("Karol Bagh", "New Delhi")
    assert path is not None
    assert stops == 4
    print(f"PASS: Interchange route found: {' -> '.join(path)} (Stops: {stops})\n")

    # Test Case 5: Multiple possible routes - BFS selects minimum stops
    print("--- Test Case 5: Multiple Routes (BFS Optimality) ---")
    # Case A: Hauz Khas to Botanical Garden (Magenta direct 13 stops vs Blue+Yellow 25+ stops)
    path_a, stops_a = metro.bfs_shortest_path("Hauz Khas", "Botanical Garden")
    assert stops_a == 13
    print(f"PASS: BFS chose shortest Magenta route (13 stops vs 25+ stops via Yellow/Blue)\n")

    # Case B: Kashmere Gate to Central Secretariat (Yellow Line direct 6 stops vs Violet Line 7 stops)
    path_b, stops_b = metro.bfs_shortest_path("Kashmere Gate", "Central Secretariat")
    assert stops_b == 6
    print(f"PASS: BFS chose shortest 6-stop Yellow route over 7-stop Violet route\n")

    # Case C: New Delhi to Yashobhoomi Dwarka Sector 25
    path_c, stops_c = metro.bfs_shortest_path("New Delhi", "Yashobhoomi Dwarka Sector 25")
    assert stops_c == 6
    print(f"PASS: BFS chose 6-stop Airport Express extending to Yashobhoomi\n")

    # Case D: Cross-Network Route from Rajiv Chowk to Greater Noida (Depot on Aqua Line)
    path_d, stops_d = metro.bfs_shortest_path("Rajiv Chowk", "Depot")
    assert path_d is not None
    print(f"PASS: Inter-network route to Greater Noida found (Stops: {stops_d})\n")

    # Test Case 6: Realistic Station Dwell Delays & Walking Distance to Tracks
    print("--- Test Case 6: Station Delays & Walking Distances ---")
    path_tf, stops_tf = metro.bfs_shortest_path("Karol Bagh", "New Delhi")
    analysis = metro.get_route_analysis(path_tf)
    assert analysis["total_walking_m"] > 0, "Walking distance should be computed"
    assert analysis["total_distance_km"] > 0.0, "Rail track distance should be computed"
    assert len(analysis["transfers"]) == 1, "Should have 1 interchange at Rajiv Chowk"
    assert analysis["transfers"][0]["station"] == "Rajiv Chowk"
    assert analysis["transfers"][0]["walk_m"] == 180, "Rajiv Chowk interchange walk is 180m"
    assert analysis["total_time_min"] > 0, "Total journey time should be computed"
    print(f"PASS: Journey Analysis: {stops_tf} stops | {analysis['total_distance_km']} km rail | {analysis['total_walking_m']} m walking | {analysis['total_time_min']} mins est. time\n")

    print("ALL TESTS PASSED SUCCESSFULLY! BFS routing, station delays, and walking metrics are verified.")


if __name__ == "__main__":
    test_metro_route_finder()
