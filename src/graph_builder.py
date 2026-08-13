"""
    Name: Graph Navigator
    Copyright: © Georgios Pegiazis 2026
    Author: Georgios Pegiazis (https://github.com/GeorgePeg)
    Date: 12/08/2026
    Version: 1.0.0
    License: GNU General Public License v3.0, 29 June 2007
    Description: Εδώ κατεβαίνει το οδικό δίκτυο από το OpenStreetMap μέσω του osmnx και αποθηκεύ-
    εται στον φάκελο data σε μορφή .graphml (caching) για να μην καθυστερεί ξανά στις επόμενες εκτελέσεις.
"""
import os
import osmnx as ox
import networkx as nx
from typing import Tuple

# Κλάση για την λήωη του οδικού δικτύου
class GraphBuilder:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
    def get_graph(self, point: Tuple[float, float], 
        dist_meters: int = 10000, 
        networktype: str="drive",
        file_tag: str = "map") -> nx.MultiDiGraph:
        lat, lon = point
        cache_filename = os.path.join(self.data_dir, f"{file_tag}_{lat:.4f}_{lon:.4f}_{dist_meters}m.graphml")
        # Έλεγχος ύπραξης του γράφου σην cache
        if os.path.exists(cache_filename):
            print(f"Ο γράφος φορτώνεται από την cache: '{cache_filename}'")
            return ox.load_graphml(cache_filename)
        print(f"Λήψη οδικού δικτύου ({dist_meters}μ. γύρω από ({lat:.4f},{lon:.4f})...")
        graph = ox.graph_from_point(point, dist=dist_meters, network_type=networktype)
        ox.save_graphml(graph, cache_filename)
        print(f"Ο γράφος αποθηκεύτηκε στο αρχείο {cache_filename} στην cache!")
        return graph
    @staticmethod
    def get_nearest_node(graph: nx.MultiDiGraph, point: Tuple[float, float]) -> int:
        lat, lon = point
        return ox.distance.nearest_nodes(graph, X=lon, Y=lat)