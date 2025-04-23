import pygambit as gbt

# Pattern: Skewed toward Player1
# Version: V7 — 2 players, 6 strategies each

players = ["Player1", "Player2"]
p1_actions = ["A1", "A2", "A3", "A4", "A5", "A6"]
p2_actions = ["B1", "B2", "B3", "B4", "B5", "B6"]

base_payoffs = {
    "Player1": [25, 30, 35, 40, 45, 50],
    "Player2": [2, 3, 4, 5, 6, 7]
}

def adjusted_payoffs(i, j):
    raw = [base_payoffs["Player1"][i], base_payoffs["Player2"][j]]
    avg = sum(raw) / 2
    return [round(p - avg, 2) for p in raw]

g = gbt.Game.new_tree(players=players, title="Two-player zero-sum V7 - Skewed toward Player1")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_V7_{i}{j}"
        g.set_outcome(n2, g.add_outcome(adjusted_payoffs(i, j), label=label))
