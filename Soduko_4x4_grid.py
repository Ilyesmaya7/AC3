from collections import deque

def ac3(csp, domains, constraints):
    """
    Enforce arc consistency using the AC-3 algorithm.
    """
    queue = deque(constraints)  # Initialize queue with all constraints

    while queue:
        (xi, xj) = queue.popleft()  # Dequeue an arc (xi, xj)

        if revise(csp, domains, xi, xj):
            if not domains[xi]:  # If the domain of xi is empty, no solution exists
                return False

            # Add all arcs (xk, xi) where xk is a neighbor of xi (except xj)
            for xk in csp[xi]:
                if xk != xj:
                    queue.append((xk, xi))

    return True  # All arcs are consistent

def revise(csp, domains, xi, xj):
    """
    Revise the domain of xi to ensure consistency with xj.
    """
    revised = False

    for x in list(domains[xi]):  # Iterate over a copy of the domain of xi
        conflict = True

        for y in domains[xj]:
            if x != y:  # If there exists a value in xj's domain that is consistent with x
                conflict = False
                break

        if conflict:  # If no consistent value exists, remove x from xi's domain
            domains[xi].remove(x)
            revised = True

    return revised

def print_domains(domains):
    """
    Print the domains of all variables.
    """
    for var, dom in domains.items():
        print(f"{var}: {dom}")

def get_neighbors(i, j):
    """
    Get all neighbors of cell (i, j) in a 4x4 Sudoku grid.
    """
    neighbors = set()

    # Row and column neighbors
    for k in range(4):
        if k != i:
            neighbors.add((k, j))
        if k != j:
            neighbors.add((i, k))

    # 2x2 block neighbors
    block_start_i, block_start_j = (i // 2) * 2, (j // 2) * 2
    for k in range(block_start_i, block_start_i + 2):
        for l in range(block_start_j, block_start_j + 2):
            if (k, l) != (i, j):
                neighbors.add((k, l))

    return neighbors

# Initialize the Sudoku grid
grid = [
    [1, 0, 3, 0],
    [0, 0, 0, 0],
    [3, 0, 0, 0],
    [0, 2, 0, 0]
]

# Domains for each cell
domains = {
    (i, j): {1, 2, 3, 4} if grid[i][j] == 0 else {grid[i][j]}
    for i in range(4) for j in range(4)
}

# CSP: Map each cell to its neighbors
csp = {
    (i, j): get_neighbors(i, j)
    for i in range(4) for j in range(4)
}

# Constraints: Arcs between each cell and its neighbors
constraints = []
for i in range(4):
    for j in range(4):
        for neighbor in csp[(i, j)]:
            constraints.append(((i, j), neighbor))

# Apply AC-3
if ac3(csp, domains, constraints):
    print("Domains after AC-3:")
    print_domains(domains)
else:
    print("No solution exists.")