import pygambit as gbt

players = ["Player1", "Player2"]
p1_actions = ["A1", "A2"]
p2_actions = ["B1", "B2"]

# Payoff matrix: combination of balanced and skewed zero-sum values
# e.g. mix of (2,-2), (0,0), (-1,1), (3,-3)
payoff_matrix = [
    [(2, -2), (-1, 1)],
    [(0, 0), (3, -3)]
]

g = gbt.Game.new_tree(players=players, title="player2_action2_imperfect_v1 - Balanced with neutral & skewed zero-sum payoffs")

# Player1 moves first
g.append_move(g.root, players[0], p1_actions)
a0, a1 = g.root.children

# Player2 moves in response to A1
g.append_move(a0, players[1], p2_actions)

# Player2 moves in response to A2 (same infoset as A1)
g.append_infoset(a1, a0.infoset)

# Assign outcomes
for i, a in enumerate([a0, a1]):
    for j, b in enumerate(a.children):
        p1, p2 = payoff_matrix[i][j]
        label = f"Outcome_{p1_actions[i]}_{p2_actions[j]}"
        g.set_outcome(b, g.add_outcome([p1, p2], label=label))
