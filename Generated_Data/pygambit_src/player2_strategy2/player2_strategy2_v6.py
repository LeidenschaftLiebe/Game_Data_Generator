import pygambit as gbt

# Pattern: Fractional values (0.1–0.9)
# Version: V6 — 2 players, 2 strategies each

players = ["Player1", "Player2"]
p1_actions = ["A1", "A2"]
p2_actions = ["B1", "B2"]

base_payoffs = {
    "Player1": [0.3, 0.7],
    "Player2": [0.5, 0.9]
}

def adjusted_payoffs(i, j):
    raw = [base_payoffs["Player1"][i], base_payoffs["Player2"][j]]
    avg = sum(raw) / 2
    return [round(p - avg, 2) for p in raw]

g = gbt.Game.new_tree(players=players, title="Two-player zero-sum V6 - Fractional values (0.1 to 0.9)")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_V6_{i}{j}"
        g.set_outcome(n2, g.add_outcome(adjusted_payoffs(i, j), label=label))
