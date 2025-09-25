import pygambit as gbt

# Variant: Match wins for Player2 (perfect information, zero-sum)
players = ["Player1", "Player2"]
p1_actions = ["A1", "A2"]
p2_actions = ["B1", "B2"]

# Ordinal matrix for Player 2 (bigger = better for P2). Player 1 gets the negative.
# Keys are (row i, col j): i indexes A1/A2; j indexes B1/B2.
P2 = {
    (0, 0): 2.0,  # A1 vs B1 -> best for P2 (match)
    (0, 1): 0.0,  # A1 vs B2 -> worst for P2
    (1, 0): 0.0,  # A2 vs B1 -> worst for P2
    (1, 1): 2.0,  # A2 vs B2 -> best for P2 (match)
}

def u_pair(i, j):
    u2 = P2[(i, j)]
    u1 = -u2  # zero-sum
    return [u1, u2]

g = gbt.Game.new_tree(players=players, title="V: match wins for Player2")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_match_{i}{j}"
        g.set_outcome(n2, g.add_outcome(u_pair(i, j), label=label))
