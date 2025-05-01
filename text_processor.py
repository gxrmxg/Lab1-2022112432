import re

def process_text(file_path: str) -> list:
    """读取文本文件，清洗非字母字符，返回小写单词列表"""
    try:
        with open(file_path, 'r') as f:
            text = f.read()
        # 替换非字母字符为空格，转小写并分割
        words = re.sub(r'[^a-zA-Z]', ' ', text).lower().split()
        return words
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")