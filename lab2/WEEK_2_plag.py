import heapq
from typing import List, Tuple, Dict

class State:
    def __init__(self, pos1: int, pos2: int, cost: int, aligned: List[Tuple[int, int]]):
        self.pos1 = pos1
        self.pos2 = pos2
        self.cost = cost
        self.aligned = aligned

    def __lt__(self, other):
        return self.cost < other.cost

def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def heuristic(state: State, doc1: List[str], doc2: List[str]) -> int:
    remaining_sentences1 = len(doc1) - state.pos1
    remaining_sentences2 = len(doc2) - state.pos2
    return abs(remaining_sentences1 - remaining_sentences2) * 5  # Rough estimate

def get_neighbors(state: State, doc1: List[str], doc2: List[str]) -> List[State]:
    neighbors = []

    # Align current sentences
    if state.pos1 < len(doc1) and state.pos2 < len(doc2):
        cost = levenshtein_distance(doc1[state.pos1], doc2[state.pos2])
        new_aligned = state.aligned + [(state.pos1, state.pos2)]
        neighbors.append(State(state.pos1 + 1, state.pos2 + 1, state.cost + cost, new_aligned))

    # Skip sentence in doc1
    if state.pos1 < len(doc1):
        neighbors.append(State(state.pos1 + 1, state.pos2, state.cost + 5, state.aligned))

    # Skip sentence in doc2
    if state.pos2 < len(doc2):
        neighbors.append(State(state.pos1, state.pos2 + 1, state.cost + 5, state.aligned))

    return neighbors

def astar_alignment(doc1: List[str], doc2: List[str]) -> List[Tuple[int, int]]:
    start_state = State(0, 0, 0, [])
    goal = (len(doc1), len(doc2))

    open_set = []
    heapq.heappush(open_set, (0, start_state))
    came_from: Dict[Tuple[int, int], State] = {}
    g_score: Dict[Tuple[int, int], int] = {(0, 0): 0}
    f_score: Dict[Tuple[int, int], int] = {(0, 0): heuristic(start_state, doc1, doc2)}

    while open_set:
        current_state = heapq.heappop(open_set)[1]

        if (current_state.pos1, current_state.pos2) == goal:
            return current_state.aligned

        for neighbor in get_neighbors(current_state, doc1, doc2):
            tentative_g_score = g_score[(current_state.pos1, current_state.pos2)] + neighbor.cost - current_state.cost

            if tentative_g_score < g_score.get((neighbor.pos1, neighbor.pos2), float('inf')):
                came_from[(neighbor.pos1, neighbor.pos2)] = current_state
                g_score[(neighbor.pos1, neighbor.pos2)] = tentative_g_score
                f_score[(neighbor.pos1, neighbor.pos2)] = g_score[(neighbor.pos1, neighbor.pos2)] + heuristic(neighbor, doc1, doc2)
                heapq.heappush(open_set, (f_score[(neighbor.pos1, neighbor.pos2)], neighbor))

    return []  # No alignment found

def detect_plagiarism(doc1: List[str], doc2: List[str], threshold: float = 0.8) -> List[Tuple[int, int, float]]:
    alignment = astar_alignment(doc1, doc2)
    plagiarism_cases = []

    for i, j in alignment:
        similarity = 1 - (levenshtein_distance(doc1[i], doc2[j]) / max(len(doc1[i]), len(doc2[j])))
        if similarity >= threshold:
            plagiarism_cases.append((i, j, similarity))

    return plagiarism_cases

# Example usage
doc1 = [
    "The quick brown fox jumps over the lazy dog.",
    "A journey of a thousand miles begins with a single step.",
    "To be or not to be, that is the question.",
]

doc2 = [
    "The quick brown fox leaps over the sleepy dog.",
    "The first step of a long journey is the hardest.",
    "To be or not to be, that is the inquiry.",
]

plagiarism_results = detect_plagiarism(doc1, doc2, threshold=0.7)
print("Potential plagiarism detected:")
for i, j, similarity in plagiarism_results:
    print(f"Doc1 sentence {i} and Doc2 sentence {j} - Similarity: {similarity:.2f}")
    print(f"Doc1: {doc1[i]}")
    print(f"Doc2: {doc2[j]}")
    print()