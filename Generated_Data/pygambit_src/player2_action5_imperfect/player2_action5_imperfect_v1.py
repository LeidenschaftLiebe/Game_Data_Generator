import pygambit as gbt

players = ["Player1", "Player2"]
p1_actions = ["A1", "A2", "A3", "A4", "A5"]
p2_actions = ["B1", "B2", "B3", "B4", "B5"]

# Payoff matrix: mix of small and large zero-sum payoffs
# Each row is Player1's action, each column is Player2's action
payoff_matrix = [
    [(3, -3), (-1, 1), (0, 0), (2, -2), (-4, 4)],
    [(1, -1), (2, -2), (-2, 2), (0, 0), (3, -3)],
    [(5, -5), (-3, 3), (1, -1), (-1, 1), (4, -4)],
    [(0, 0), (-2, 2), (3, -3), (2, -2), (-1, 1)],
    [(4, -4), (0, 0), (-1, 1), (1, -1), (2, -2)]
]

g = gbt.Game.new_tree(players=players, title="player2_action5_imperfect_v1 - Grouped infosets with mixed payoff scales")

# Player1 moves
g.append_move(g.root, players[0], p1_actions)
a0, a1, a2, a3, a4 = g.root.children

# First info set: A1 and A2
g.append_move(a0, players[1], p2_actions)
g.append_infoset(a1, a0.infoset)

# Second info set: A3, A4, A5
g.append_move(a2, players[1], p2_actions)
g.append_infoset(a3, a2.infoset)
g.append_infoset(a4, a2.infoset)

# Assign outcomes
for i, a in enumerate([a0, a1, a2, a3, a4]):
    for j, b in enumerate(a.children):
        p1, p2 = payoff_matrix[i][j]
        label = f"Outcome_{p1_actions[i]}_{p2_actions[j]}"
        g.set_outcome(b, g.add_outcome([p1, p2], label=label))
