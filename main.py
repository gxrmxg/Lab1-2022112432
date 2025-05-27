from text_processor import process_text
from graph import Graph
from algorithms import (
    query_bridge_words,
    generate_new_text,
    calc_shortest_path,
    calc_pagerank,
    random_walk
)
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
        print("6. Random Walk")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ").strip()

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
            try:
                word_freq = graph.get_word_freq()
                pr = calc_pagerank(graph, word_freq)
                print("\nPageRank Scores:")
                for node, score in sorted(pr.items(), key=lambda x: -x[1]):
                    print(f"{node}: {score:.4f}")
            except Exception as e:
                print(f"Error calculating PageRank: {e}")

        elif choice == '6':
            start = input("Enter start word (or press Enter to choose randomly): ").strip()
            if start and not validate_word(graph, start):
                print("Invalid start word. It does not exist in the graph.")
                continue
            path = random_walk(graph, start_word=start if start else None)
            print(" -> ".join(path))

        elif choice == '7':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
