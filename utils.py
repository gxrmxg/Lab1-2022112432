from graph import Graph

def validate_word(graph: Graph, word: str) -> bool:
    """验证单词是否在图中存在"""
    return word.lower() in graph.get_nodes()

def input_file_path() -> str:
    """安全获取用户输入的文件路径"""
    while True:
        path = input("Enter text file path: ").strip()
        if path:
            return path
        print("Invalid path. Try again.")