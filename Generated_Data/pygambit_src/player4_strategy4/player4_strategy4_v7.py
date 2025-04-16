import pygambit as gbt

# Pattern: Each player's payoffs are symmetric or reflective around 5
# Useful for modeling equilibrium or balance

players = ["Player1", "Player2", "Player3", "Player4"]
p1_actions = ["A1", "A2", "A3", "A4"]
p2_actions = ["B1", "B2", "B3", "B4"]
p3_actions = ["C1", "C2", "C3", "C4"]
p4_actions = ["D1", "D2", "D3", "D4"]

base_payoffs = {
    "Player1": [4, 5, 6, 5],
    "Player2": [5, 6, 5, 4],
    "Player3": [6, 5, 4, 5],
    "Player4": [5, 4, 5, 6]
}

def adjusted_payoffs(i, j, k, l):
    raw = [base_payoffs["Player1"][i], base_payoffs["Player2"][j], base_payoffs["Player3"][k], base_payoffs["Player4"][l]]
    avg = sum(raw) / 4
    return [round(p - avg, 2) for p in raw]

g = gbt.Game.new_tree(players=players, title="Four-player zero-sum V7 - Centered Symmetry")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        g.append_move(n2, players[2], p3_actions)
        for k, n3 in enumerate(n2.children):
            g.append_move(n3, players[3], p4_actions)
            for l, n4 in enumerate(n3.children):
                adj = adjusted_payoffs(i, j, k, l)
                label = f"Outcome_V7_{i}{j}{k}{l}"
                g.set_outcome(n4, g.add_outcome(adj, label=label))
