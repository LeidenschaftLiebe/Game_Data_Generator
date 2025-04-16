import pygambit as gbt

# Pattern: High variance (10–100)
# Version: V2 — 2 players, 7 strategies each

players = ["Player1", "Player2"]
p1_actions = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
p2_actions = ["B1", "B2", "B3", "B4", "B5", "B6", "B7"]

base_payoffs = {
    "Player1": [10, 30, 55, 70, 85, 95, 100],
    "Player2": [90, 40, 60, 20, 80, 35, 75]
}

def adjusted_payoffs(i, j):
    raw = [base_payoffs["Player1"][i], base_payoffs["Player2"][j]]
    avg = sum(raw) / 2
    return [round(p - avg, 2) for p in raw]

g = gbt.Game.new_tree(players=players, title="Two-player zero-sum V2 - High variance (10 to 100)")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_V2_{i}{j}"
        g.set_outcome(n2, g.add_outcome(adjusted_payoffs(i, j), label=label))
