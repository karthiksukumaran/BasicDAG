from collections import deque

def agent_execution_order(agents: list[str], dependencies: list[list[str]]) -> list[str]:
    """
    agents: list of agent IDs (alphanumeric strings)
    dependencies: list of [prerequisite, dependent] pairs
    Returns: valid execution order, or [] if cycle exists
    """
    # Map string IDs → integer indices internally
    idx = {agent: i for i, agent in enumerate(agents)}
    n = len(agents)

    graph = [[] for _ in range(n)]
    in_degree = [0] * n

    for prereq, dependent in dependencies:
        graph[idx[prereq]].append(idx[dependent])
        in_degree[idx[dependent]] += 1
    
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order_idx = []

    while queue:
        agent = queue.popleft()
        order_idx.append(agent)
        for neighbor in graph[agent]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order_idx) != n:
        return []  # Cycle detected

    return [agents[i] for i in order_idx]


# ── Test 1: Single root forks, converges at midpoint, then fans out ──────────
print("\n \n \nTest 1: Single root forks, converges at midpoint, then fans out ")
agents = ["agentA1", "agentB2", "agentC3", "agentD4", "agentE5"]
deps   = [["agentA1","agentC3"], ["agentB2","agentC3"],
          ["agentC3","agentD4"], ["agentC3","agentE5"], ["agentB2","agentA1"]]
print("agents =", agents)
print("deps =", deps)
print(agent_execution_order(agents, deps))
print("\n \n========================================== \n \n")
# → ['agentB2', 'agentA1', 'agentC3', 'agentD4', 'agentE5']

# ── Test 2: Linear chain  P0 → Q1 → R2 → S3 ─────────────────────
print("Test 2: Linear chain  P0 → Q1 → R2 → S3 ")
agents = ["P0", "Q1", "R2", "S3"]
deps   = [["P0","Q1"], ["Q1","R2"], ["R2","S3"]]
print("agents =", agents)
print("deps =", deps)
print(agent_execution_order(agents, deps))
print("\n \n========================================== \n \n")
# → ['P0', 'Q1', 'R2', 'S3']


# ── Test 3: Diamond  X0 → Y1, X0 → Z2, Y1 → W3, Z2 → W3 ────────
print("Test 3: Diamond  X0 → Y1, X0 → Z2, Y1 → W3, Z2 → W3 ")
agents = ["X0", "Y1", "Z2", "W3"]
deps   = [["X0","Y1"], ["X0","Z2"], ["Y1","W3"], ["Z2","W3"]]
print("agents =", agents)
print("deps =", deps)
print(agent_execution_order(agents, deps))
print("\n \n========================================== \n \n")
# → ['X0', 'Y1', 'Z2', 'W3']  or  ['X0', 'Z2', 'Y1', 'W3']


# ── Test 4: Completely independent agents ─────────────────────────
print("Test 4: Completely independent agents ")
agents = ["AG1", "AG2", "AG3"]
deps   = []
print("agents =", agents)
print("deps =", deps)
print(agent_execution_order(agents, deps))
print("\n \n========================================== \n \n")
# → ['AG1', 'AG2', 'AG3']


# ── Test 5: Cycle detection  M1 → N2 → O3 → M1 ──────────────────
print("Test 5: Cycle detection  M1 → N2 → O3 → M1 ")
agents = ["M1", "N2", "O3"]
deps   = [["M1","N2"], ["N2","O3"], ["O3","M1"]]
print("agents =", agents)
print("deps =", deps)
print(agent_execution_order(agents, deps))
print("\n \n========================================== \n \n")
# → []  (cycle detected)


# ── Test 6: Multiple roots → shared hub → split ───────────────────
print("Test 6: Multiple roots → shared hub → split ")
#   R0 \              / F4
#   R1  → HUB → BR5 → T6
#   R2 /
agents = ["R0", "R1", "R2", "HUB", "F4", "BR5", "T6"]
deps   = [["R0","HUB"], ["R1","HUB"], ["R2","HUB"],
          ["HUB","F4"], ["HUB","BR5"], ["BR5","T6"]]
print("agents =", agents)
print("deps =", deps)
print(agent_execution_order(agents, deps))
print("\n \n========================================== \n \n")
# → ['R0', 'R1', 'R2', 'HUB', 'F4', 'BR5', 'T6']


# ── Test 7: Single agent, no dependencies ─────────────────────────
print("Test 7: Single agent, no dependencies ")
agents = ["solo99"]
deps   = []
print("agents =", agents)
print("deps =", deps)
print(agent_execution_order(agents, deps))
print("\n \n========================================== \n \n")
# → ['solo99']


# ── Test 8: Two separate chains that never meet ───────────────────
#   alpha01 → beta02 → gamma03   and   delta04 → epsilon05
print("Test 8: Two separate chains that never meet ")
agents = ["alpha01", "beta02", "gamma03", "delta04", "epsilon05"]
deps   = [["alpha01","beta02"], ["beta02","gamma03"], ["delta04","epsilon05"]]
print("agents =", agents)
print("deps =", deps)
print(agent_execution_order(agents, deps))
print("\n \n========================================== \n \n")
# → ['alpha01', 'delta04', 'beta02', 'epsilon05', 'gamma03']
