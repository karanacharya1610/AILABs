from collections import deque

def get_successors(state):
    successors = []
    empty_index = state.index('_')  # Find the empty spot
    
    # East-bound rabbits ('E') can move to the right (1 or 2 steps)
    if empty_index > 0:  # Ensure we can move leftwards in the array
        if state[empty_index - 1] == 'E':  # Move one step to the right
            new_state = list(state)
            new_state[empty_index], new_state[empty_index - 1] = new_state[empty_index - 1], new_state[empty_index]
            successors.append(''.join(new_state))
        if empty_index > 1 and state[empty_index - 2] == 'E':  # Jump two steps to the right
            new_state = list(state)
            new_state[empty_index], new_state[empty_index - 2] = new_state[empty_index - 2], new_state[empty_index]
            successors.append(''.join(new_state))
    
    # West-bound rabbits ('W') can move to the left (1 or 2 steps)
    if empty_index < len(state) - 1:  # Ensure we can move rightwards in the array
        if state[empty_index + 1] == 'W':  # Move one step to the left
            new_state = list(state)
            new_state[empty_index], new_state[empty_index + 1] = new_state[empty_index + 1], new_state[empty_index]
            successors.append(''.join(new_state))
        if empty_index < len(state) - 2 and state[empty_index + 2] == 'W':  # Jump two steps to the left
            new_state = list(state) 
            new_state[empty_index], new_state[empty_index + 2] = new_state[empty_index + 2], new_state[empty_index]
            successors.append(''.join(new_state))
    
    return successors

def bfs(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set([start_state])
    
    while queue:
        current_state, path = queue.popleft()
        
        # Check if we reached the goal state
        if current_state == goal_state:
            return path + [current_state]
        
        # Generate and explore successors
        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                queue.append((successor, path + [current_state]))
    
    return None

# Initial and goal states
start_state = 'EEE_WWW'
goal_state = 'WWW_EEE'

# Run the BFS algorithm to find the solution
solution = bfs(start_state, goal_state)

if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")