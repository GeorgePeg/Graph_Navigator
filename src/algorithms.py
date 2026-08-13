"""
    Name: Graph Navigator
    Copyright: © Georgios Pegiazis 2026
    Author: Georgios Pegiazis (https://github.com/GeorgePeg)
    Date: 12/08/2026
    Version: 1.0.0
    License: GNU General Public License v3.0, 29 June 2007
    Description: Εδώ υλοποιούνται οι αλγόριθμοι για την εύρεση των διαδρομών.
    Υλοποιώ from-scratch τον αλγόριθμο αναζήτησης Dijkstra για την εύρεση της ελάχιστης 
    διαδρομής και τον αλγόριθμο αναζήτησης A* για τον υπολογισμό της πραγματικής απόστασης
    πάνω στην σφαίρα της Γης, μέσω της ευρετικής συνάρτησης Haversine. 
"""
import heapq
import math
import time
import networkx as nx
from typing import Dict, List, Tuple, Optional

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Εδώ υπολογίζεται η μεγάλη κυκλική απόσταση (Great-Circle Distance) μεταξύ δύο σημείων πάνω
    στη Γη (σε μέτρα). 
    """
    # Μέση ακτίνα της Γης σε μέτρα
    R = 6371000.0
    # Μετατροπή των συντεταγμένων από μοίρες σε ακτίνια (rad)
    phi1,phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lamda = math.radians(lon2 - lon1)
    # Τύπος Haversine
    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lamda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0-a))

    return R * c
# Κλάση για την υλοποίηση των custom αλγορίθμων
class PathFinder:
    def __init__(self, graph: nx.MultiDiGraph) :
        self.graph = graph
    # Υλοποίηση αλγορίθμου Dijkstra
    def dijkstra_custom(self, start_node: int, target_node: int) -> Tuple[Optional[List[int]], float, float]:
        """
        Χρησιμοποίηση Min-Heap (Priority Queue)
        Ο αλγόριθμος παίρνει ως ορίσματα τον κόμβο εκκίνησης και τον κόμβο στόχου και
        επιστρέφει ένα Tuple που περιέχει μια λίστα των κόμβων της διαδρομή, την συνολική
        απόσταση και το χρόνο εκτέλεσης.
        """
        start_time = time.perf_counter()
        # Αρχικοποίηση των αποστάσεων
        distances: Dict[int, float] = {node: float('inf') for node in self.graph.nodes}
        previous: Dict[int, Optional[int]] = {node: None for node in self.graph.nodes}
        # Απόσταση αφετηρίας από τον εαυτό της
        distances[start_node] = 0.0
        # Ορισμός της ουράς προτεραιότητας -> Αποθηκεύονται ζεύγη τρέχουσας απόστασης και κόμβου
        priority_queue = [(0.0, start_node)]

        while priority_queue:
            # Λήψη κόμου με την ελάχιστη έως εκείνη τη στιγμή απόσταση
            current_distance, current_node = heapq.heappop(priority_queue)
            # Αν target_node, τότε η αναζήτηση σταματά
            if current_node == target_node:
                break
            # Αν βρέθηκε ήδη μικρότερη διαδρομή για αυτό το κόμβο, τότε η αναζήτηση συνεχίζεται
            if current_distance > distances[current_node]:
                continue
            # Εξετάζω όλους τους γειτονικούς κόμβους
            for neighbor, edges in self.graph[current_node].items():
                # Στο MultiDiGraphs μπορεί να υπάρχουν παράλληλοι δρόμοι (δηλ.ακμές)
                # Παίρνω το ελάχιστο μήκος μεταξύ αυτών των ακμών
                edge_weight = min(edge.get('length', 1.0) for edge in edges.values())
                new_distance = edge_weight + current_distance
                # Αν βρέθηκε συντομότερη διαδρομή προς τον γείτονα, τότε σταματά η αναζήτηση
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] =  current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))
        execution_time = time.perf_counter() - start_time
        # Αν δεν φτάσαμε στον στόχο, τότε επιστρέφει άπειρο
        if distances[target_node] == float('inf'):
            return None, float('inf'), execution_time
        # Αν πάω από τον στόχο στην αφετηρία, τότε ανακατασκευάζω την διαδρομή
        path = []
        curr = target_node
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse() # Από την αφετηρία στο στόχο
        return path, distances[target_node], execution_time
    def a_star_search(self, start_node: int, target_node: int) -> Tuple[Optional[List[int]], float, float]:
        """
        Υλοποίηση αλγορίθμου αναζήτησης Α* με την ευρετική συνάρτηση Haversine και Min-Heap 
        """
        start_time = time.perf_counter()
        # Ορίζω τις γεωγραφικές συντεταγμένες του στόχου
        target_lat = self.graph.nodes[target_node]['y']
        target_lon = self.graph.nodes[target_node]['x']
        # Εσωτερική ευρετική συνάρτηση haversine -> υπολογίζει την ευθεία απόσταση από οποιοδήποτε κόμβο
        # μέχρι τον τελικό στόχο.
        def heuristic(node: int) -> float:
            node_lat = self.graph.nodes[node]['y']
            node_lon = self.graph.nodes[node]['x']
            return haversine_distance(node_lat, node_lon, target_lat, target_lon)
        # Πραγματικό κόστος (απόσταση) από τον κόμβο αφετηρίας μέχρι τον στόχο
        g_cost: Dict[int, float] = {node: float('inf') for node in self.graph.nodes}
        # Τελικό κόστος
        final_cost: Dict[int, float] = {node: float('inf') for node in self.graph.nodes}
        previous: Dict[int, Optional[int]] = {node: None for node in self.graph.nodes}

        # Κόμβος αφετηρίας
        g_cost[start_node] =  0.0
        final_cost[start_node] = heuristic(start_node)

        # Ουρά προτεραιότητας
        pq = [(final_cost[start_node], start_node)]
        while pq:
            # Λήψη κόμβου με το μικρότερο κόστος
            _, current_node = heapq.heappop(pq)
            # Αν φτάσαμε στον στόχο, η διαδικασία ολοκληρώνεται
            if current_node == target_node:
                break
            # Εξέταση όλων των κόμβων
            for neighbor, edges in self.graph[current_node].items():
                edge_weight = min(edge.get('length', 1.0) for edge in edges.values())
                tg =  g_cost[current_node] + edge_weight
                # Αν βρέθηκε καλύτερη διαδρομή προς τον γείτονα
                if tg < g_cost[neighbor]:
                    previous[neighbor] = current_node
                    g_cost[neighbor] = tg
                    final_cost[neighbor] = tg + heuristic(neighbor)
                    heapq.heappush(pq, (final_cost[neighbor], neighbor))
        execution_time = time.perf_counter() - start_time
        # Αν δεν υπάρχει διαδρομή προς τον στόχο
        if g_cost[target_node] == float('inf'):
            return None, float('inf'), execution_time
        # Αν πάω από τον στόχο στην αφετηρία, τότε ανακατασκευάζω την διαδρομή
        path = []
        curr = target_node
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse() # Από την αφετηρία στο στόχο
        return path, g_cost[target_node], execution_time
    
        
