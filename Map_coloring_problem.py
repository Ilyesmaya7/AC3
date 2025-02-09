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

# Variables and domains
variables = ['A', 'B', 'C','D','E']
domains = {var: {'Red', 'Blue'} for var in variables}

# CSP: Map each region to its neighbors
csp = {
    'A': {'B', 'C'},
    'B': {'A', 'C'},
    'C': {'A', 'B'},
    'D': {'E','A'},
    'E': {'E','B'}
}

# Constraints: Arcs between adjacent regions
constraints = [('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'B'), ('A', 'C'), ('C', 'A')]

# Apply AC-3
if ac3(csp, domains, constraints):
    print("Domains after AC-3:")
    print_domains(domains)
else:
    print("No solution exists.")