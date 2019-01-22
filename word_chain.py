"""
word_chain.py

@autor Nathan Laing and Sam Fleury

"""
import sys
from collections import deque

word_to_index = {}
index_to_word = {}


class Node:
    """
    A class for the nodes of the graph.
    """
    def __init__(self, word, parent, cost):
        """
        Initialises the Node class objects
        :param word: The word this node is going to store
        :param parent: The Node that you traversed to this node from in the graph
        :param cost: The total cost to get here from the starting word
        """
        self.word = word
        self.parent = parent
        self.cost = cost

    def __str__(self):
        return "Word: " + self.word


def dif(word_a, word_b):
    """
    Our own method for edit distance for strings of the same length.
    :param word_a: The first word to be compared
    :param word_b: The second word to be compared
    :return: The edit distance between the words
    (how many single char edits you have to make to get from word_a => word_b)
    """
    i = 0
    difs = 0

    while i < len(word_a):
        if word_a[i] != word_b[i]:
            difs += 1
        i += 1

    return difs


def make_graph(words):
    """
    Generates the adjacency matrix used to store which words are 1 edit distance away from others
    :param words: A list of words to be added into the graph
    :return: A 2D list set up as an adjacency matrix where 1 represents an edge and 0 represents the lack of an edge
    """
    graph = [[0] * len(words) for i in range(len(words))]

    i = 0
    while i < len(words):
        j = 0
        while j < len(words):
            if dif(words.get(i), words.get(j)) == 1:
                graph[i][j] = 1
            j += 1
        i += 1
    return graph


def find_min(starting_word, target_word, graph):
    """
    Finds the minimum word chain between two words. Uses an algorithm based off of Dijkstra's algorithm
    :param starting_word: The starting word of the word chain
    :param target_word: The word you want to end up at
    :param graph: The adjacency matrix used to represent the relationships between the words
    :return: The minimum word chain or a not possible message
    """
    global index_to_word
    global word_to_index

    queue = deque()
    visited = []

    root = Node(word=starting_word, parent=None, cost=1)
    queue.append(root)
    current = root

    while current.word != target_word:
        if queue:
            current = queue.popleft()
            visited.append(current.word)

            edges = [j for j, x in enumerate(graph[(word_to_index.get(current.word))]) if x == 1]

            for i in range(len(edges)):
                if index_to_word.get(edges[i]) not in visited:
                    new_node = Node(index_to_word.get(edges[i]), current, current.cost + 1)
                    queue.append(new_node)
        else:
            return starting_word + " " + target_word + " not possible"

    answer = []
    while True:
        answer.insert(0, current.word)
        if current.parent is None:
            break
        else:
            current = current.parent

    return ' '.join(answer)


def find_chain_of_len(starting_word, target_word, chain_length, graph):
    """
    Finds a word chain between two words that is of the given length. Based off of a depth first limited search
    :param starting_word: The word that the word chain should begin with
    :param target_word: The word that the chain should end with
    :param chain_length: The length of the chain (also controls the depth of the search)
    :param graph: The adjacency matrix used to represent the relationships between the words
    :return: A word chain of the given length or a not possible message
    """
    global index_to_word
    global word_to_index

    root = Node(word=starting_word, parent=None, cost=1)
    queue = deque()
    visited = [[]]

    queue.append(root)

    while queue:
        current = queue.popleft()
        visited.append(get_chain(current))

        if current.word == target_word and current.cost == chain_length:

            answer = []
            while True:
                answer.insert(0, current.word)
                if current.parent is None:
                    break
                else:
                    current = current.parent

            return ' '.join(answer)

        elif current.cost < chain_length:

            edges = [j for j, x in enumerate(graph[(word_to_index.get(current.word))]) if x == 1]

            for i in range(len(edges)):
                check_path = get_chain(current)
                check_path.append(index_to_word.get(edges[i]))

                if check_path not in visited and index_to_word.get(edges[i]) not in get_chain(current):

                    if index_to_word.get(edges[i]) != target_word:
                        new_node = Node(index_to_word.get(edges[i]), current, current.cost + 1)
                        queue.appendleft(new_node)

                    elif current.cost + 1 == chain_length:
                        new_node = Node(index_to_word.get(edges[i]), current, current.cost + 1)
                        queue.appendleft(new_node)

    return starting_word + " " + target_word + " " + str(chain_length) + " not possible"


def get_chain(node):
    """
    Gets the chain of steps to how you got to this node.
    :param node: The end node of the chain
    :return: answer (the chain from root to current node)
    """
    answer = []
    while True:
        answer.append(node.word)
        if node.parent is None:
            break
        else:
            node = node.parent
    return answer


def main():
    """
    The main method. This reads in the parameters from the command line and the words from the text file to be used.
    It Then sets up the needed variables and calls the appropriate graph search method (based on chain length).
    :return:
    """
    global word_to_index
    global index_to_word

    if len(sys.argv) < 3:
        print("Please enter a word to chain from and a word to chain to.")

    elif len(sys.argv) > 4:
        print("Please enter only a starting word, target word and chain length.")

    else:
        starting_word = sys.argv[1]
        target_word = sys.argv[2]

        if len(sys.argv) == 4:
            chain_length = int(sys.argv[3])

            if dif(starting_word, target_word) > (chain_length + 1):
                print(starting_word + " " + target_word + " " + str(chain_length) + " not possible")
                return
        else:
            chain_length = -1

        i = 0
        line = sys.stdin.readline()

        while line:
            line = line.rstrip('\n')
            line = line.lower()

            word_to_index.update({line: i})
            index_to_word.update({i: line})

            i += 1
            line = sys.stdin.readline()

        if starting_word not in word_to_index.keys() or target_word not in word_to_index.keys():
            print(starting_word + " " + target_word + " " + str(chain_length) + " not possible")
            return
        else:

            graph = make_graph(index_to_word)

            if chain_length == -1:
                print(find_min(starting_word, target_word, graph))
            else:
                print(find_chain_of_len(starting_word, target_word, chain_length, graph))


if __name__ == "__main__":
    main()
