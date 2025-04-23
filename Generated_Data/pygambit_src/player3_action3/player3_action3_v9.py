import pygambit as gbt

# Pattern: Player1 dominates in magnitude, testing sensitivity to payoff scaling

players = ["Player1", "Player2", "Player3"]
p1_actions = ["A1", "A2", "A3"]
p2_actions = ["B1", "B2", "B3"]
p3_actions = ["C1", "C2", "C3"]

base_payoffs = {
    "Player1": [20, 25, 30],
    "Player2": [5, 3, 6],
    "Player3": [2, 1, 4]
}

def adjusted_payoffs(i, j, k):
    raw = [base_payoffs["Player1"][i], base_payoffs["Player2"][j], base_payoffs["Player3"][k]]
    avg = sum(raw) / 3
    return [round(p - avg, 2) for p in raw]

g = gbt.Game.new_tree(players=players, title="Three-player high-magnitude P1 V9")
g.append_move(g.root, "Player1", p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, "Player2", p2_actions)
    for j, n2 in enumerate(n1.children):
        g.append_move(n2, "Player3", p3_actions)
        for k, n3 in enumerate(n2.children):
            adj = adjusted_payoffs(i, j, k)
            label = f"Outcome_{p1_actions[i]}_{p2_actions[j]}_{p3_actions[k]}"
            g.set_outcome(n3, g.add_outcome(adj, label=label))
