import numpy as np
import heapq

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state  # Current state of the puzzle (2D list)
        self.parent = parent  # Parent node
        self.g = g  # Cost to reach this node
        self.h = h  # Heuristic cost to reach the goal
        self.f = g + h  # Total cost

    def __lt__(self, other):
        return self.f < other.f  # For priority queue

def heuristic(state, goal_state):
    """Computes the Manhattan distance heuristic."""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:  # Exclude the blank tile
                goal_position = np.argwhere(goal_state == state[i][j])[0]
                distance += abs(i - goal_position[0]) + abs(j - goal_position[1])
    return distance

def get_successors(node):
    """Generates all possible successor nodes."""
    successors = []
    zero_position = np.argwhere(node.state == 0)[0]  # Find position of the blank tile (0)
    x, y = zero_position[0], zero_position[1]

    # Possible movements: (dx, dy) pairs for up, down, left, right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in moves:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:  # Check bounds
            new_state = np.copy(node.state)
            # Swap the blank tile with the adjacent tile
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            g = node.g + 1  # Cost to reach this successor
            h = heuristic(new_state, goal_state)  # Heuristic cost
            successors.append(Node(new_state, node, g, h))

    return successors

def search_agent(start_state, goal_state):
    """Implements the A* search algorithm."""
    start_node = Node(start_state, None, 0, heuristic(start_state, goal_state))
    open_list = []
    heapq.heappush(open_list, start_node)
    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)

        # Check if we reached the goal
        if np.array_equal(current_node.state, goal_state):
            return current_node  # Return the goal node to backtrack

        closed_set.add(tuple(map(tuple, current_node.state)))  # Add state to closed set

        # Expand the node
        for successor in get_successors(current_node):
            if tuple(map(tuple, successor.state)) in closed_set:
                continue  # Skip already visited states

            heapq.heappush(open_list, successor)

    return None  # No solution found

def generate_puzzle(depth):
    """Generates a solvable puzzle instance with a specified depth."""
    initial_state = np.array([1, 2, 3, 4, 5, 6, 0, 7, 8]).reshape(3, 3)  # Goal state
    np.random.seed(0)  # For reproducibility
    for _ in range(depth):
        blank_position = np.argwhere(initial_state == 0)[0]
        possible_moves = []
        
        # Possible movements: (dx, dy) pairs for up, down, left, right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in moves:
            new_x, new_y = blank_position[0] + dx, blank_position[1] + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                possible_moves.append((new_x, new_y))
        
        if possible_moves:
            new_blank_position = possible_moves[np.random.choice(len(possible_moves))]
            initial_state[blank_position[0]][blank_position[1]], initial_state[new_blank_position[0]][new_blank_position[1]] = \
                initial_state[new_blank_position[0]][new_blank_position[1]], initial_state[blank_position[0]][blank_position[1]]

    return initial_state

def backtrack_path(goal_node):
    """Backtracks to find the path from the initial state to the goal state."""
    path = []
    while goal_node:
        path.append(goal_node.state)
        goal_node = goal_node.parent
    return path[::-1]  # Reverse the path to start from the initial state

# Example Usage
start_state = generate_puzzle(depth=10)  # Generate a puzzle instance
goal_state = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0]).reshape(3, 3)  # Goal state

print("Start State:")
print(start_state)

goal_node = search_agent(start_state, goal_state)

if goal_node:
    print("Goal State Reached!")
    path = backtrack_path(goal_node)
    print("Path to Goal State:")
    for state in path:
        print(state)
else:
    print("No solution found.")
