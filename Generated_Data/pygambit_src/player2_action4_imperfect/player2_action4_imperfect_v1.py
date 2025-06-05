import pygambit as gbt

players = ["Player1", "Player2"]
p1_actions = ["A1", "A2", "A3", "A4"]
p2_actions = ["B1", "B2", "B3", "B4"]

# Payoff matrix: diverse zero-sum values (some low, some high)
# Each row corresponds to a Player1 action (A1 to A4), and each column to a Player2 action (B1 to B4)
payoff_matrix = [
    [(2, -2), (-1, 1), (0, 0), (5, -5)],
    [(-3, 3), (1, -1), (4, -4), (-2, 2)],
    [(3, -3), (-2, 2), (1, -1), (0, 0)],
    [(0, 0), (2, -2), (-1, 1), (3, -3)]
]

g = gbt.Game.new_tree(players=players, title="player2_action4_imperfect_v1 - Two infosets for Player2 with 4x4 actions")

# Player1 moves
g.append_move(g.root, players[0], p1_actions)
a0, a1, a2, a3 = g.root.children

# Group A1 and A3 into one infoset for Player2
g.append_move(a0, players[1], p2_actions)
g.append_infoset(a2, a0.infoset)

# Group A2 and A4 into another infoset for Player2
g.append_move(a1, players[1], p2_actions)
g.append_infoset(a3, a1.infoset)

# Assign outcomes using labels like Outcome_A1_B1
for i, a in enumerate([a0, a1, a2, a3]):
    for j, b in enumerate(a.children):
        p1, p2 = payoff_matrix[i][j]
        label = f"Outcome_{p1_actions[i]}_{p2_actions[j]}"
        g.set_outcome(b, g.add_outcome([p1, p2], label=label))
