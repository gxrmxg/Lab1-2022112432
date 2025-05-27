from algorithms import calc_shortest_path
from graph import Graph

def test_same_node():
    g = Graph()
    g.add_edge("A", "B")
    result = calc_shortest_path(g, "A", "A")
    assert "length: 0" in result

def test_multiple_paths():
    g = Graph()
    g.add_edge("A", "B", weight=1)  # 显式指定参数名
    g.add_edge("A", "C", weight=5)
    g.add_edge("B", "C", weight=1)
    result = calc_shortest_path(g, "A", "C")
    assert "a -> b -> c" in result and "length: 2" in result

def test_unreachable():
    g = Graph()
    g.add_edge("A", "B")
    result = calc_shortest_path(g, "B", "A")
    assert "No path" in result

def test_invalid_nodes():
    g = Graph()
    result = calc_shortest_path(g, "X", "Y")
    assert "Invalid words" in result