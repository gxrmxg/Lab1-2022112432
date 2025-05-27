import pytest
from graph import Graph
from algorithms import query_bridge_words

@pytest.fixture
def sample_graph():
    g = Graph()
    g.add_edge("apple", "banana")
    g.add_edge("banana", "cherry")
    g.add_edge("apple", "cherry")
    return g

@pytest.mark.parametrize("word1, word2, expected", [
    ("apple", "cherry", "banana"),  # 存在桥接词
    ("apple", "banana", "No bridge words"),  # 无桥接词
    ("dog", "cat", "No dog or cat"),  # 单词不存在
    ("apple", "", "No apple or"),  # 空输入
    ("apple", "apple", "No bridge words")  # 相同单词
])
def test_query_bridge_words(sample_graph, word1, word2, expected):
    result = query_bridge_words(sample_graph, word1, word2)
    assert expected in result