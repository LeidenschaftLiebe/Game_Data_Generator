import pygambit as gbt

# Pattern: Negative staircase
# Version: V3 — 2 players, 15 strategies each

players = ["Player1", "Player2"]
p1_actions = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15']
p2_actions = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15']

base_payoffs = {
    "Player1": [0, -2, -4, -6, -8, -10, -12, -14, -16, -18, -20, -22, -24, -26, -28],
    "Player2": [0, -3, -6, -9, -12, -15, -18, -21, -24, -27, -30, -33, -36, -39, -42]
}

def adjusted_payoffs(i, j):
    raw = [base_payoffs["Player1"][i], base_payoffs["Player2"][j]]
    avg = sum(raw) / 2
    return [round(p - avg, 2) for p in raw]

g = gbt.Game.new_tree(players=players, title="Two-player zero-sum V3 - Negative staircase")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_V3_{i}_{j}"
        g.set_outcome(n2, g.add_outcome(adjusted_payoffs(i, j), label=label))
