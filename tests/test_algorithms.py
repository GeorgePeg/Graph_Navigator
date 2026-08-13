"""
    Name: Graph Navigator
    Copyright: © Georgios Pegiazis 2026
    Author: Georgios Pegiazis (https://github.com/GeorgePeg)
    Date: 12/08/2026
    Version: 1.0.0
    License: GNU General Public License v3.0, 29 June 2007
    Description: Εδώ δοκιμάζω τους αλγόριθμους αναζήτησης από το /src/algorithms.py
"""
import pytest
import networkx as nx
from src.algorithms import PathFinder, haversine_distance

@pytest.fixture 
def sample_graph():
    """
    Δημιουργώ έναν τεχνητό γράφο που αποτελείται από 4 κόμβους για να δοκιμάσω τους αλγόριθμους 
    αναζήτησης
    """
    # Δημιουργώ έναν κατευθυνόμενο γράφο που δέχεται και παράλληλες ακμές
    G = nx.MultiDiGraph()

    # Προσθέτω κόμβους που περιέχουν γεωγραφικές συντεταγμένες
    G.add_node(1, y=37.98, x=23.72)
    G.add_node(2, y=37.99, x=23.73)
    G.add_node(3, y=38.00, x=23.74)
    G.add_node(4, y=38.01, x=23.75)

    # Προσθήκη ακμών με βάρη (υποδηλώνουν το μήκος του δρόμου σε μέτρα)
    G.add_edge(1,2, length=100.0)
    G.add_edge(2,3, length=150.0)
    G.add_edge(1,3, length=500.0)
    G.add_edge(3,4, length=200.0)

    return G
def testing_haversine_distance():
    """
    Δοκιμάζω την Haversine αν υπολογίζει σωστά την απόσταση. Θα χρησιμοποιήσω τις συντεταγμένες 
    της Αθήνας και της Θεσσαλονίκης.
    """
    athens_lat, athens_lon = 37.9838, 23.7275
    skg_lat, skg_lon = 40.6401, 22.9444

    distance = haversine_distance(athens_lat, athens_lon, skg_lat, skg_lon)

    # Η απόσταση Αθήνα-Θεσσαλονίκη σε ΕΥΘΕΙΑ ΓΡΑΜΜΗ είναι περίπου 312 χλμ
    assert 300000 < distance < 320000
def testing_dijkstra(sample_graph):
    """
    Δοκιμάζω τον custom Dijkstra για την εύρεση της συντομότερη διαδρομής
    """
    finder = PathFinder(sample_graph)
    path, distance, exec_time = finder.dijkstra_custom(start_node=1, target_node=4)

    # 1ος Έλεγχος: Αναμενόμενη Λίστα 1->2->3->4
    assert path == [1,2,3,4]
    # 2ος Έλεγχος: Ορθός Υπολογισμός Διαδρομής
    assert distance == 450.0
    # 3ος Έλεγχος: Θετικός αριθμός για τον χρόνο εκτέλεσης
    assert exec_time > 0
def a_star_test(sample_graph):
    """
    Δοκιμάζω τον custom A* -> Πρέπει να βρει την ίδια συντομότερη διαδρομή με τον Dijkstra
    """ 
    finder = PathFinder(sample_graph)
    path, distance, exec_time = finder.a_star_search(start_node=1, target_node=4) 
    assert path == [1,2,3,4]
    assert distance == 450.0
    assert exec_time > 0
