import heapq
import re
import random
from graph import Graph
from typing import Dict, List
from collections import defaultdict


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



def calc_pagerank(graph: Graph, word_freq: Dict[str, int],
                  d: float = 0.85, tol: float = 1e-6, max_iter: int = 100) -> Dict[str, float]:
    if d is None:
        d = 0.85  # 默认阻尼系数

    all_nodes = list(graph.get_nodes())
    N = len(all_nodes)
    if N == 0:
        return {}

    pr = {node: 1.0 / N for node in all_nodes}

    for _ in range(max_iter):
        new_pr = {node: (1 - d) / N for node in all_nodes}
        for u in all_nodes:
            out_nodes = graph.adjacency_list.get(u, {})
            if len(out_nodes) == 0:
                continue
            share = pr[u] / len(out_nodes)
            for v in out_nodes:
                new_pr[v] += d * share

        total = sum(new_pr.values())
        for node in new_pr:
            new_pr[node] /= total

        diff = sum(abs(new_pr[node] - pr[node]) for node in all_nodes)
        pr = new_pr
        if diff < tol:
            break

    return pr
0



def random_walk(graph, start_word=None, max_steps=20):
    import random

    if not graph.adjacency_list:
        return []

    current = start_word if start_word else random.choice(list(graph.adjacency_list.keys()))
    path = [current]

    for _ in range(max_steps):
        neighbors = list(graph.adjacency_list.get(current, {}).keys())
        if not neighbors:
            break
        current = random.choice(neighbors)
        path.append(current)

    return path

