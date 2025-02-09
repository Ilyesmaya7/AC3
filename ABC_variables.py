from collections import deque

# Define the constraints in a form of a dictionary
# (X, Y) -> constraint between X and Y
constraints = {
    ('A', 'B'): lambda a, b: a > b,   # A > B
    ('B', 'A'): lambda a, b: b > a,   # B > A
    ('B', 'C'): lambda b, c: b == c,  # B = C
    ('C', 'B'): lambda c, b: c == b   # C = B
}

# Domains of variables
domains = {
    'A': {1, 2, 3},
    'B': {1, 2, 3},
    'C': {1, 2, 3}
}

def revise(X, Y):
    """Revise the domain of X based on the constraint with Y"""
    revised = False
    for x in list(domains[X]):  # Make a copy of the domain of X
        # Check if there's no value in domain of Y that satisfies the constraint
        if not any(constraints[(X, Y)](x, y) for y in domains[Y]):
            domains[X].remove(x)  # Remove value from domain of X if it doesn't satisfy the constraint
            revised = True
    return revised

def ac3():
    """Apply AC-3 algorithm to enforce arc consistency"""
    queue = deque([(X, Y) for (X, Y) in constraints.keys()])  # Initialize the queue with all arcs
    
    while queue:
        X, Y = queue.popleft()  # Get the next arc
        if revise(X, Y):
            # If the domain of X has been modified, add all arcs involving X to the queue
            for Z in domains:
                if Z != X and (Z, X) in constraints:
                    queue.append((Z, X))
    
    # Return the final domains
    return domains

# Apply AC-3 to the problem
final_domains = ac3()

# Output the results
print("Final domains after applying AC-3:")
for var, dom in final_domains.items():
    print(f"{var}: {dom}")
