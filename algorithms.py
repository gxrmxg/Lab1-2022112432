import heapq
import re
import random
from graph import Graph
from typing import Dict, List


def query_bridge_words(graph: Graph, word1: str, word2: str) -> str:
    """查询桥接词"""
    word1 = word1.lower()
    word2 = word2.lower()
    nodes = graph.get_nodes()
    if word1 not in nodes or word2 not in nodes:
        return f"No {word1} or {word2} in the graph!"

    # 遍历所有可能的桥接词
    bridge_words = []
    for word3 in graph.adjacency_list.get(word1, {}):
        if word2 in graph.adjacency_list.get(word3, {}):
            bridge_words.append(word3)

    if not bridge_words:
        return f"No bridge words from {word1} to {word2}!"
    return f"The bridge words from {word1} to {word2} are: {', '.join(bridge_words)}."


def generate_new_text(graph: Graph, input_text: str) -> str:
    """根据桥接词生成新文本"""
    words = re.sub(r'[^a-zA-Z]', ' ', input_text).lower().split()
    new_text = []
    for i in range(len(words) - 1):
        u, v = words[i], words[i + 1]
        new_text.append(u)
        bridges = []
        # 查找桥接词
        for word3 in graph.adjacency_list.get(u, {}):
            if v in graph.adjacency_list.get(word3, {}):
                bridges.append(word3)
        if bridges:
            new_text.append(random.choice(bridges))
    new_text.append(words[-1])
    return ' '.join(new_text)


def calc_shortest_path(graph: Graph, start: str, end: str) -> str:
    """Dijkstra算法计算最短路径（权重和最小）"""
    start = start.lower()
    end = end.lower()
    nodes = graph.get_nodes()
    if start not in nodes or end not in nodes:
        return "Invalid words."

    distances = {node: float('inf') for node in nodes}
    distances[start] = 0
    predecessors = {}
    heap = [(0, start)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if u == end:
            break
        for v, weight in graph.adjacency_list[u].items():
            if distances[v] > current_dist + weight:
                distances[v] = current_dist + weight
                predecessors[v] = u
                heapq.heappush(heap, (distances[v], v))

    if distances[end] == float('inf'):
        return f"No path from {start} to {end}."
    path = []
    current = end
    while current in predecessors:
        path.insert(0, current)
        current = predecessors[current]
    path.insert(0, start)
    return f"Shortest path: {' -> '.join(path)}, length: {distances[end]}"


def calc_pagerank(graph: Graph, iterations: int = 100, d: float = 0.85) -> Dict[str, float]:
    """计算PageRank值"""
    nodes = list(graph.get_nodes())
    pr = {node: 1.0 / len(nodes) for node in nodes}
    for _ in range(iterations):
        new_pr = {}
        for node in nodes:
            incoming = [u for u in graph.adjacency_list if node in graph.adjacency_list[u]]
            new_pr[node] = (1 - d) / len(nodes) + d * sum(
                pr[u] / len(graph.adjacency_list[u]) for u in incoming
            )
        pr = new_pr
    return pr