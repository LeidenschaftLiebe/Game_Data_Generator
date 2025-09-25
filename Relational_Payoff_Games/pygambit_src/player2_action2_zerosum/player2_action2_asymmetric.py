import pygambit as gbt

# Variant: Asymmetric row-wise — Row 1 strict (B1 > B2), Row 2 tie for Player2
players = ["Player1", "Player2"]
p1_actions = ["A1", "A2"]
p2_actions = ["B1", "B2"]

# Player 2 ordinal outcomes:
# - If Player1 plays A1: B1 (2) > B2 (0)
# - If Player1 plays A2: B1 (1) = B2 (1)  (tie)
P2 = {
    (0, 0): 2.0,
    (0, 1): 0.0,
    (1, 0): 1.0,
    (1, 1): 1.0,
}

def u_pair(i, j):
    u2 = P2[(i, j)]
    u1 = -u2  # zero-sum
    return [u1, u2]

g = gbt.Game.new_tree(players=players, title="V: asymmetric row-wise (strict/tie)")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_asym_{i}{j}"
        g.set_outcome(n2, g.add_outcome(u_pair(i, j), label=label))
