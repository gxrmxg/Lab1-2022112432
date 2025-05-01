from text_processor import process_text
from graph import Graph
from algorithms import query_bridge_words, generate_new_text, calc_shortest_path, calc_pagerank
from utils import input_file_path, validate_word
import sys


def main():
    # 读取文件并构建图
    try:
        file_path = input_file_path()
        words = process_text(file_path)
        graph = Graph()
        graph.build_from_words(words)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # 用户交互菜单
    while True:
        print("\n===== Menu =====")
        print("1. Show directed graph")
        print("2. Query bridge words")
        print("3. Generate new text")
        print("4. Calculate shortest path")
        print("5. Calculate PageRank")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            print("\nDirected Graph:")
            graph.show_directed_graph()

        elif choice == '2':
            word1 = input("Enter word1: ").strip()
            word2 = input("Enter word2: ").strip()
            if not validate_word(graph, word1) or not validate_word(graph, word2):
                print("Invalid words. Check if they exist in the graph.")
                continue
            print(query_bridge_words(graph, word1, word2))

        elif choice == '3':
            text = input("Enter new text: ").strip()
            print("Generated text:", generate_new_text(graph, text))

        elif choice == '4':
            start = input("Enter start word: ").strip()
            end = input("Enter end word: ").strip()
            if not validate_word(graph, start) or not validate_word(graph, end):
                print("Invalid words. Check if they exist in the graph.")
                continue
            print(calc_shortest_path(graph, start, end))

        elif choice == '5':
            pr = calc_pagerank(graph)
            print("\nPageRank Scores:")
            for node, score in sorted(pr.items(), key=lambda x: -x[1]):
                print(f"{node}: {score:.4f}")

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()"Modification in B1" 
