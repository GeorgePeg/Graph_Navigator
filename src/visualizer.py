"""
    Name: Graph Navigator
    Copyright: © Georgios Pegiazis 2026
    Author: Georgios Pegiazis (https://github.com/GeorgePeg)
    Date: 12/08/2026
    Version: 1.0.0
    License: GNU General Public License v3.0, 29 June 2007
    Description: Εδώ δημιουργούνται διαδραστικά HTML χάρτες με τη χρήση του Folium
"""
import os
import folium
import networkx as nx
from typing import Optional, List

# Κλάση οπτικοποίησης διαδραστικών χαρτών
class MapVisualizer:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    # Μέθοδος δημιουργίας χάρτη
    def create_route_map(self, graph: nx.MultiDiGraph, path:List[int], total_distance: float,
        execution_time: float, 
        algorithm_name: str=" A* ", 
        filename: str = "route_map.html") -> str:
        """
        Δημιουργεί ένα HTML χάρτη με τη σχεδιασμένη διαδρομή.
        """
        if not path or len(path) < 2:
            raise ValueError("Σφάλμα: Η διαδρομή πρέπει να περιέχει τουλάχιστον δύο κόμβους!")
        # Συλλογή συντεταγμένων
        coordinates_record = []
        for node in path:
            lat = graph.nodes[node]['y']
            lon = graph.nodes[node]['x']
            coordinates_record.append((lat,lon))
        # Αρχικοποίηση του χάρτη 
        start_lat, start_lon = coordinates_record[0]
        end_lat, end_lon = coordinates_record[-1]

        # Κεντράρισμα χάρτη στο μέσο της διαδρομής
        center_lat = (start_lat + end_lat) / 2
        center_lon = (start_lon + end_lon) / 2
        router_map = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=14,
            titles="OpenStreetMap"
        )

        # Σχεδίαση της γραμμής διαδρομής
        folium.PolyLine(
            locations=coordinates_record,
            color="#010a50",
            weight=6,
            opacity=0.8,
            popup=f"Διαδρομή {algorithm_name}: {total_distance / 1000:.2f} χλμ."
        ).add_to(router_map)

        # Προσθήκη Πράσινου Marker στον κόμβο αφετηρίας
        folium.Marker(
            location=[start_lat, start_lon],
            popup=f"<b>Αφετηρία</b><br>Αλγόριθμος: {algorithm_name}",
            tooltip="Αφετηρία",
            icon=folium.Icon(color="green", icon="play", prefix="fa")
        ).add_to(router_map)
        # Προσθήκη Πράσινου Marker στον κόμβο αφετηρίας
        folium.Marker(
            location=[end_lat, end_lon],
            popup=(f"<b>Τερματισμός</b><br>"
                   f"Συνολική διαδρομή: {total_distance / 1000:.2f} χλμ <br>"
                   f"Χρόνος Υπολογισμού: {execution_time * 1000:.2f} ms"),
            tooltip="Προορισμός",
            icon=folium.Icon(color="red", icon="flag-checkered", prefix="fa")
        ).add_to(router_map)
        # Αποθήκευση του χάρτη ως HTML
        file_path = os.path.join(self.output_dir, filename)
        router_map.save(file_path)
        print(f"[Visualizer] Ο χάρτης αποθηκεύτηκε με επιτυχία στο {file_path}")

        return file_path