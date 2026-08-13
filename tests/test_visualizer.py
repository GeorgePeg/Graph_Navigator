"""
    Name: Graph Navigator
    Copyright: © Georgios Pegiazis 2026
    Author: Georgios Pegiazis (https://github.com/GeorgePeg)
    Date: 12/08/2026
    Version: 1.0.0
    License: GNU General Public License v3.0, 29 June 2007
    Description: Εδώ δοκιμάζω το /src/visualizer.py
"""
import os
import pytest
import networkx as nx
from src.visualizer import MapVisualizer

@pytest.fixture
def sample_graph():
    """
    Δημιουργώ έναν απλό διαδραστικό χάρτη με 2 κόμβους
    """
    G = nx.MultiDiGraph()
    G.add_node(1, y= 37.9755, x=23.7348) # Αθήνα (Σύνταγμα)
    G.add_node(2, y=37.9838, x=23.7255) # Αθήνα (Ομόνοια)
    G.add_edge(1,2, length=1000.0)
    return G
@pytest.fixture
def temp_output_dir(tmp_path):
    """
    Προσωρινός φάκελος δοκιμών μέσω του ενσωματωμένου fixture του pytest
    """
    return str(tmp_path)
def testing_create_route_map(sample_graph, temp_output_dir):
    """
    Δοκιμάζω την επιτυχή δημιουργία του διαδραστικού HTML χάρτη
    """
    visualizer = MapVisualizer(output_dir=temp_output_dir)
    test_filename = "test_map.html"

    output_path = visualizer.create_route_map(
        graph=sample_graph,
        path=[1,2],
        total_distance=1000.0,
        execution_time=0.005,
        algorithm_name="A*",
        filename=test_filename
    )
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0
    with open(output_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        assert "A*" in html_content
def invalid_path(sample_graph, temp_output_dir):
    """
    Δοκιμή μη έγκυρης διαδρομής
    """
    visualizer = MapVisualizer(output_dir=temp_output_dir)
    # "Πετάω" έναν ValueError αν η διαδρομή έχει είτε μόνο 1 κόμβο είτε είναι άδεια
    with pytest.raises(ValueError):
        visualizer.create_route_map(
            graph=sample_graph,
            path=[1],
            total_distance=0.0,
            execution_time=0.0,
            algorithm_name="Dijkstra"
        )