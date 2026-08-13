"""
    Name: Graph Navigator
    Copyright: © Georgios Pegiazis 2026
    Author: Georgios Pegiazis (https://github.com/GeorgePeg)
    Date: 12/08/2026
    Version: 1.0.0
    License: GNU General Public License v3.0, 29 June 2007
    Description: Εδώ εκτελούνται τα πάντα.
"""
import sys
from src.visualizer import MapVisualizer
from src.algorithms import PathFinder
from src.geocoder import Geocoder
from src.graph_builder import GraphBuilder

def main():
    print("Καλωσορίσατε στον Graph Navigator!")

    # Αρχικοποίηση των modules
    geocoder = Geocoder()
    graph_builder = GraphBuilder()
    visualizer = MapVisualizer()

    print("\n Εισαγωγή Τοποθεσιών")
    start_address = input("Αφετηρία (π.χ. Syntagma Square, Athens):").strip()
    if not start_address:
        start_address = "Syntagma Square, Athens"
        print(f"--> Προεπιλογή: {start_address}")
    target_address = input("Προορισμός (π.χ. Monastiraki, Athens):").strip()
    if not target_address:
        target_address = "Monastyraki, Athens"
        print(f"--> Προεπιλογή: {target_address}")
    start_coordinates = geocoder.geocode(start_address)
    end_coordinates = geocoder.geocode(target_address)
    if not start_coordinates or not end_coordinates:
        print("Σφάλμα: Δεν ήταν δυνατός ο υπολογισμός διευθύνσεων. Παρακαλώ δοκιμάστε ξανά!")
        sys.exit(1)

    print(f"Αφετηρία: {start_coordinates}")
    print(f"Προορισμός: {end_coordinates}")

    print("\nΦόρτωση Οδικού Χάρτη")
    athens_center = (37.9755, 23.7348)

    graph = graph_builder.get_graph(
        point=athens_center,
        dist_meters=5000,
        file_tag="attica_region"
    )
    start_node = graph_builder.get_nearest_node(graph, start_coordinates)
    end_node = graph_builder.get_nearest_node(graph, end_coordinates)

    print("\nΕκτέλεση Αλγορίθμων Αναζήτησης Διαδρομής...")
    path_finder =PathFinder(graph)

    dijkstra_path, dijkstra_dist, dijkstra_time = path_finder.dijkstra_custom(start_node, end_node)
    a_star_path, a_star_dist, a_star_time = path_finder.a_star_search(start_node, end_node)

    print("\n ===== Αποτελέσματα & Σύγκριση =====")
    print("Dijkstra:")
    print(f"-> Απόσταση: {dijkstra_dist / 1000:.2f} χλμ.| Χρόνος Εκτέλεσης: {dijkstra_time} ms")
    print("Α*:")
    print(f"-> Απόσταση: {a_star_dist / 1000:.2f} χλμ.| Χρόνος Εκτέλεσης: {a_star_time} ms")
    print("=======================================")

    print("\n Δημιουργία HTML χάρτη")
    output_file = visualizer.create_route_map(
        graph=graph,
        path=a_star_path,
        total_distance=a_star_dist,
        execution_time=a_star_time,
        algorithm_name="A*",
        filename="navigator_route.html"
    )
    print(f"Η πλοήγηση ολοκληρώθηκε με επιτυχία! Ανοίξτε το αρχείο {output_file} στον browser σας για να δείτε το χάρτη.")
if __name__ == "__main__":
    main()