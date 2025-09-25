import pygambit as gbt

# Variant: Mismatch wins for Player2 (perfect information, zero-sum)
players = ["Player1", "Player2"]
p1_actions = ["A1", "A2"]
p2_actions = ["B1", "B2"]

# Ordinal matrix for Player 2 (bigger = better for P2): off-diagonals best.
P2 = {
    (0, 0): 0.0,  # match is worst for P2
    (0, 1): 2.0,  # mismatch is best
    (1, 0): 2.0,  # mismatch is best
    (1, 1): 0.0,  # match is worst
}

def u_pair(i, j):
    u2 = P2[(i, j)]
    u1 = -u2  # zero-sum
    return [u1, u2]

g = gbt.Game.new_tree(players=players, title="V: mismatch wins for Player2")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_mismatch_{i}{j}"
        g.set_outcome(n2, g.add_outcome(u_pair(i, j), label=label))
