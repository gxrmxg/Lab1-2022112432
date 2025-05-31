from collections import defaultdict

class Graph:
    """有向图类，基于邻接表存储"""

    def __init__(self):
        self.adjacency_list = defaultdict(lambda: defaultdict(int))  # 格式: {u: {v: weight}}
        self.word_freq = defaultdict(int)  # 词频统计

    def add_edge(self, u: str, v: str, weight: int = 1) -> None:
        """添加边并更新权重（可自定义权重）"""
        u = u.lower()
        v = v.lower()
        self.adjacency_list[u][v] += weight  # 累加权重（或直接赋值，根据需求选择）
        self.word_freq[u] += weight  # 根据权重更新词频
        self.word_freq[v] += weight  # 可选：根据需求决定是否更新终点词频

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
        nodes = set(self.adjacency_list.keys())
        for v_dict in self.adjacency_list.values():
            nodes.update(v_dict.keys())
        return nodes

    def get_word_freq(self) -> dict:
        """返回词频字典"""
        return dict(self.word_freq)
