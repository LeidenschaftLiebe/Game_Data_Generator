import pygambit as gbt

# Pattern: All negative values
# Version: V3 — 2 players, 3 strategies each

players = ["Player1", "Player2"]
p1_actions = ["A1", "A2", "A3"]
p2_actions = ["B1", "B2", "B3"]

base_payoffs = {
    "Player1": [-1, -3, -6],
    "Player2": [-4, -2, -5]
}

def adjusted_payoffs(i, j):
    raw = [base_payoffs["Player1"][i], base_payoffs["Player2"][j]]
    avg = sum(raw) / 2
    return [round(p - avg, 2) for p in raw]

g = gbt.Game.new_tree(players=players, title="Two-player zero-sum V3 - All negative values")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_V3_{i}{j}"
        g.set_outcome(n2, g.add_outcome(adjusted_payoffs(i, j), label=label))
