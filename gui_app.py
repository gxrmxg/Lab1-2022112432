import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from text_processor import process_text
from graph import Graph
from algorithms import (
    query_bridge_words,
    generate_new_text,
    calc_shortest_path,
    calc_pagerank,
    random_walk
)
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab1 - Graph Processor")
        self.graph = None
        self.create_widgets()

    def create_widgets(self):
        """创建GUI组件"""
        # 文件选择区域
        self.frame_file = ttk.LabelFrame(self.root, text="文件选择")
        self.frame_file.pack(padx=10, pady=5, fill="x")

        self.btn_open = ttk.Button(self.frame_file, text="选择文本文件", command=self.load_file)
        self.btn_open.pack(side=tk.LEFT, padx=5)

        self.label_file = ttk.Label(self.frame_file, text="未选择文件")
        self.label_file.pack(side=tk.LEFT)

        # 功能按钮区域
        self.frame_controls = ttk.LabelFrame(self.root, text="功能操作")
        self.frame_controls.pack(padx=10, pady=5, fill="x")

        self.btn_show_graph = ttk.Button(self.frame_controls, text="展示有向图", command=self.show_graph)
        self.btn_show_graph.pack(side=tk.LEFT, padx=2)

        self.btn_bridge = ttk.Button(self.frame_controls, text="查询桥接词", command=self.open_bridge_dialog)
        self.btn_bridge.pack(side=tk.LEFT, padx=2)

        self.btn_new_text = ttk.Button(self.frame_controls, text="生成新文本", command=self.open_text_dialog)
        self.btn_new_text.pack(side=tk.LEFT, padx=2)

        self.btn_shortest = ttk.Button(self.frame_controls, text="最短路径", command=self.open_shortest_dialog)
        self.btn_shortest.pack(side=tk.LEFT, padx=2)

        self.btn_pagerank = ttk.Button(self.frame_controls, text="PageRank", command=self.show_pagerank)
        self.btn_pagerank.pack(side=tk.LEFT, padx=2)

        self.btn_walk = ttk.Button(self.frame_controls, text="随机游走", command=self.do_random_walk)
        self.btn_walk.pack(side=tk.LEFT, padx=2)

        # 结果显示区域
        self.frame_output = ttk.LabelFrame(self.root, text="结果输出")
        self.frame_output.pack(padx=10, pady=5, fill="both", expand=True)

        self.text_output = tk.Text(self.frame_output, height=15)
        self.text_output.pack(fill="both", expand=True)

    def load_file(self):
        """加载文本文件并构建图"""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        try:
            words = process_text(file_path)
            self.graph = Graph()
            self.graph.build_from_words(words)
            self.label_file.config(text=f"已加载文件: {file_path}")
            self.text_output.insert(tk.END, "图构建成功！\n")
        except Exception as e:
            messagebox.showerror("错误", f"文件加载失败: {str(e)}")

    def show_graph(self):
        """可视化展示有向图（使用NetworkX和Matplotlib）"""
        if self.graph is None:
            messagebox.showwarning("警告", "请先加载文件！")
            return

        G = nx.DiGraph()
        for u in self.graph.adjacency_list:
            for v, w in self.graph.adjacency_list[u].items():
                G.add_edge(u, v, weight=w)

        fig = plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue',
                edge_color='gray', arrows=True)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # 将图形嵌入到Tkinter窗口
        top = tk.Toplevel()
        top.title("有向图可视化")
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def open_bridge_dialog(self):
        """打开桥接词查询对话框"""
        if self.graph is None:
            messagebox.showwarning("警告", "请先加载文件！")
            return

        dialog = tk.Toplevel()
        dialog.title("查询桥接词")

        tk.Label(dialog, text="Word1:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_word1 = ttk.Entry(dialog)
        self.entry_word1.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Word2:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_word2 = ttk.Entry(dialog)
        self.entry_word2.grid(row=1, column=1, padx=5, pady=5)

        btn_submit = ttk.Button(dialog, text="查询",
                                command=lambda: self.query_bridge())
        btn_submit.grid(row=2, column=0, columnspan=2, pady=5)

    def query_bridge(self):
        """执行桥接词查询"""
        word1 = self.entry_word1.get().strip()
        word2 = self.entry_word2.get().strip()
        result = query_bridge_words(self.graph, word1, word2)
        self.text_output.insert(tk.END, f"桥接词查询结果: {result}\n")

    def open_text_dialog(self):
        """打开新文本生成对话框"""
        dialog = tk.Toplevel()
        dialog.title("生成新文本")

        tk.Label(dialog, text="输入文本:").pack(padx=5, pady=5)
        self.entry_text = tk.Text(dialog, height=5, width=40)
        self.entry_text.pack(padx=5, pady=5)

        btn_submit = ttk.Button(dialog, text="生成",
                                command=lambda: self.generate_text())
        btn_submit.pack(pady=5)

    def generate_text(self):
        """生成新文本并显示"""
        input_text = self.entry_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("警告", "请输入文本！")
            return
        new_text = generate_new_text(self.graph, input_text)
        self.text_output.insert(tk.END, f"生成的新文本: {new_text}\n")

    def open_shortest_dialog(self):
        """打开最短路径查询对话框"""
        dialog = tk.Toplevel()
        dialog.title("最短路径")

        tk.Label(dialog, text="起点:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_start = ttk.Entry(dialog)
        self.entry_start.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="终点:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_end = ttk.Entry(dialog)
        self.entry_end.grid(row=1, column=1, padx=5, pady=5)

        btn_submit = ttk.Button(dialog, text="计算",
                                command=lambda: self.calc_shortest())
        btn_submit.grid(row=2, column=0, columnspan=2, pady=5)

    def calc_shortest(self):
        """计算最短路径"""
        start = self.entry_start.get().strip()
        end = self.entry_end.get().strip()
        result = calc_shortest_path(self.graph, start, end)
        self.text_output.insert(tk.END, f"最短路径结果: {result}\n")

    def show_pagerank(self):
        """显示PageRank结果"""
        if self.graph is None:
            messagebox.showwarning("警告", "请先加载文件！")
            return

        # 创建对话框让用户输入目标词
        dialog = tk.Toplevel()
        dialog.title("PageRank 分析")

        tk.Label(dialog, text="请输入目标词（可选，留空则不指定）:").pack(padx=10, pady=5)
        entry_target = ttk.Entry(dialog)
        entry_target.pack(padx=10, pady=5)

        def compute_and_show():
            target_word = entry_target.get().strip().lower() or None
            word_freq = self.graph.get_word_freq()
            pr = calc_pagerank(self.graph, word_freq, target_word)
            output = "\n".join([f"{word}: {score:.4f}" for word, score in pr.items()])
            self.text_output.insert(tk.END, "PageRank结果:\n" + output + "\n")
            dialog.destroy()

        btn_submit = ttk.Button(dialog, text="计算", command=compute_and_show)
        btn_submit.pack(pady=5)

    def do_random_walk(self):
        """执行随机游走"""
        if self.graph is None:
            messagebox.showwarning("警告", "请先加载文件！")
            return
        walk_result = random_walk(self.graph)
        self.text_output.insert(tk.END, f"随机游走结果: {walk_result}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()