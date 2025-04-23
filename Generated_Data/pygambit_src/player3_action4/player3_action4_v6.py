import pygambit as gbt

# Pattern: Fractional decimal payoffs (0.1–1.0)
# Useful for simulating precision-based reward environments (e.g., probabilistic models)

players = ["Player1", "Player2", "Player3"]
p1_actions = ["A1", "A2", "A3", "A4"]
p2_actions = ["B1", "B2", "B3", "B4"]
p3_actions = ["C1", "C2", "C3", "C4"]

base_payoffs = {
    "Player1": [0.3, 0.7, 0.5, 0.9],
    "Player2": [0.6, 0.4, 0.2, 0.8],
    "Player3": [0.1, 0.9, 0.3, 0.6]
}

def adjusted_payoffs(i, j, k):
    raw = [base_payoffs["Player1"][i], base_payoffs["Player2"][j], base_payoffs["Player3"][k]]
    avg = sum(raw) / 3
    return [round(p - avg, 4) for p in raw]

g = gbt.Game.new_tree(players=players, title="Three-player zero-sum V6 - Fractional Payoffs")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        g.append_move(n2, players[2], p3_actions)
        for k, n3 in enumerate(n2.children):
            label = f"Outcome_V6_{i}{j}{k}"
            g.set_outcome(n3, g.add_outcome(adjusted_payoffs(i, j, k), label=label))
