import pygambit as gbt

players = ["Player1", "Player2"]
p1_actions = ["A1", "A2", "A3"]
p2_actions = ["B1", "B2", "B3"]

payoff_matrix = [
    [(3, -3), (-2, 2), (1, -1)],
    [(0, 0), (2, -2), (-1, 1)],
    [(5, -5), (-3, 3), (4, -4)]
]

g = gbt.Game.new_tree(players=players, title="player2_action3_imperfect_v1")

# Player1 moves
g.append_move(g.root, players[0], p1_actions)
a0, a1, a2 = g.root.children

# Player2 moves in response to A1
g.append_move(a0, players[1], p2_actions)

# Player2 moves in response to A2 (same infoset as after A1)
g.append_infoset(a1, a0.infoset)

# Player2 moves in response to A3 (separate infoset)
g.append_move(a2, players[1], p2_actions)

# Assign outcomes
for i, a in enumerate([a0, a1, a2]):
    for j, b in enumerate(a.children):
        p1, p2 = payoff_matrix[i][j]
        label = f"Outcome_V1_{i}{j}"
        g.set_outcome(b, g.add_outcome([p1, p2], label=label))
