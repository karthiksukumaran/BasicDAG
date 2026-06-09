from collections import deque

def agent_execution_order(n: int, dependencies: list[list[int]]) -> list[int]:
    """
    n: number of agents
    dependencies: list of [prerequisite, dependent] pairs
    Returns: valid execution order, or [] if cycle exists
    """
    # Build adjacency list and in-degree count
    graph = [[] for _ in range(n)]
    in_degree = [0] * n

    for prereq, dependent in dependencies:
        graph[prereq].append(dependent)
        in_degree[dependent] += 1

    # Start with all agents that have no dependencies
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []
    while queue:
        agent = queue.popleft()
        order.append(agent)

        for neighbor in graph[agent]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If not all agents are in order, there's a cycle
    return order if len(order) == n else []


# Test 1: Two independent roots converge then fan out
n = 5
deps = [[0,2],[1,2],[2,3],[2,4]]
print("n =", n)
print("deps =", deps)
print(agent_execution_order(n, deps))
# Possible output: [0, 1, 2, 3, 4]


# Test 2: Linear chain  A -> B -> C -> D
n = 4
deps = [[0,1],[1,2],[2,3]]
print(n)
print("deps =", deps)
print(agent_execution_order(n, deps))
# Output: [0, 1, 2, 3]

# Test 3: Diamond  0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
n = 4
deps = [[0,1],[0,2],[1,3],[2,3]]
print(n)
print("deps =", deps)
print(agent_execution_order(n, deps))
# Possible output: [0, 1, 2, 3] or [0, 2, 1, 3]

# Test 4: Completely independent agents (no dependencies)
n = 3
deps = []
print(n)
print("deps =", deps)
print(agent_execution_order(n, deps))
# Output: [0, 1, 2]


# Test 5: Cycle detection — 0 -> 1 -> 2 -> 0
n = 3
deps = [[0,1],[1,2],[2,0]]
print("n =", n)
print("deps =", deps)
print(agent_execution_order(n, deps))
# Output: []  (cycle detected)



# Test 6: Multiple roots, one shared dependency, then split
#   0 \          / 4
#   1  -> 3 -> 5
#   2 /          \ 6
n = 7
deps = [[0,3],[1,3],[2,3],[3,4],[3,5],[5,6]]
print(n)
print("deps =", deps)
print(agent_execution_order(n, deps))
# Possible output: [0, 1, 2, 3, 4, 5, 6]

# Test 7: Single agent, no dependencies
n = 1
deps = []
print(n)
print("deps =", deps)
print(agent_execution_order(n, deps))
# Output: [0]

# Test 8: Two separate chains that never meet
#   0 -> 1 -> 2   and   3 -> 4
n = 5
deps = [[0,1],[1,2],[3,4]]
print(n)
print("deps =", deps)
print(agent_execution_order(n, deps))
# Possible output: [0, 3, 1, 4, 2]
