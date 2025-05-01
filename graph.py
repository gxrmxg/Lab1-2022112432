from collections import defaultdict


class Graph:
    """有向图类，基于邻接表存储"""

    def __init__(self):
        self.adjacency_list = defaultdict(lambda: defaultdict(int))  # 格式: {u: {v: weight}}

    def add_edge(self, u: str, v: str) -> None:
        """添加边并更新权重（相邻出现次数）"""
        u = u.lower()
        v = v.lower()
        self.adjacency_list[u][v] += 1

    def build_from_words(self, words: list) -> None:
        """从单词列表构建图"""
        if len(words) < 2:
            return
        for i in range(len(words) - 1):
            self.add_edge(words[i], words[i + 1])

    def show_directed_graph(self) -> None:
        """在命令行展示图结构"""
        for u in self.adjacency_list:
            neighbors = self.adjacency_list[u]
            if neighbors:
                edges = [f"{v}({count})" for v, count in neighbors.items()]
                print(f"{u} -> {', '.join(edges)}")

    def get_nodes(self) -> set:
        """返回所有节点"""
        return set(self.adjacency_list.keys())


