import pygambit as gbt

# Pattern: Payoffs vary randomly with both low and high values
# Emulates games with opportunity spikes and penalties

players = ["Player1", "Player2", "Player3"]
p1_actions = ["A1", "A2", "A3", "A4"]
p2_actions = ["B1", "B2", "B3", "B4"]
p3_actions = ["C1", "C2", "C3", "C4"]

base_payoffs = {
    "Player1": [3, 15, 2, 10],
    "Player2": [8, 1, 12, 4],
    "Player3": [7, 14, 6, 0]
}

def adjusted_payoffs(i, j, k):
    raw = [base_payoffs["Player1"][i], base_payoffs["Player2"][j], base_payoffs["Player3"][k]]
    avg = sum(raw) / 3
    return [round(p - avg, 2) for p in raw]

g = gbt.Game.new_tree(players=players, title="Three-player zero-sum V7 - Random Peaks")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        g.append_move(n2, players[2], p3_actions)
        for k, n3 in enumerate(n2.children):
            label = f"Outcome_V7_{i}{j}{k}"
            g.set_outcome(n3, g.add_outcome(adjusted_payoffs(i, j, k), label=label))
