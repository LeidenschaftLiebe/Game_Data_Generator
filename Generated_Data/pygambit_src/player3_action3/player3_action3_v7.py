import pygambit as gbt

# Pattern: P1 has decreasing values, P2 increasing, P3 random
# Useful for asymmetric preference testing

players = ["Player1", "Player2", "Player3"]
p1_actions = ["A1", "A2", "A3"]
p2_actions = ["B1", "B2", "B3"]
p3_actions = ["C1", "C2", "C3"]

base_payoffs = {
    "Player1": [9, 6, 3],
    "Player2": [1, 4, 7],
    "Player3": [2, 5, 4]
}

def adjusted_payoffs(i, j, k):
    raw = [base_payoffs["Player1"][i], base_payoffs["Player2"][j], base_payoffs["Player3"][k]]
    avg = sum(raw) / 3
    return [round(p - avg, 2) for p in raw]

g = gbt.Game.new_tree(players=players, title="Three-player monotonic variation V7")
g.append_move(g.root, "Player1", p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, "Player2", p2_actions)
    for j, n2 in enumerate(n1.children):
        g.append_move(n2, "Player3", p3_actions)
        for k, n3 in enumerate(n2.children):
            adj = adjusted_payoffs(i, j, k)
            label = f"Outcome_{p1_actions[i]}_{p2_actions[j]}_{p3_actions[k]}"
            g.set_outcome(n3, g.add_outcome(adj, label=label))
