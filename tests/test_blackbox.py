import pytest
from graph import Graph
from algorithms import query_bridge_words


@pytest.fixture
def sample_graph():
    g = Graph()
    g.add_edge("apple", "banana")
    g.add_edge("banana", "cherry")
    g.add_edge("apple", "cherry")  # 直接边，验证不影响桥接判断
    return g


@pytest.mark.parametrize("word1, word2, expected_substring", [
    # TC1: 有效桥接词
    ("apple", "cherry", "The bridge words from apple to cherry are: banana"),

    # TC2: 没有桥接词
    ("apple", "banana", "No bridge words from apple to banana!"),

    # TC3: 相同单词
    ("apple", "apple", "No bridge words from apple to apple!"),

    # TC4: word1 不存在
    ("dog", "cherry", "No dog or cherry in the graph!"),

    # TC5: word2 不存在
    ("apple", "lion", "No apple or lion in the graph!"),

    # TC6: word1 为空
    ("", "cherry", "No  or cherry in the graph!"),

    # TC7: word2 是空格
    ("apple", "  ", "No apple or    in the graph!"),
])
def test_query_bridge_words(sample_graph, word1, word2, expected_substring):
    result = query_bridge_words(sample_graph, word1, word2)
    assert expected_substring in result
