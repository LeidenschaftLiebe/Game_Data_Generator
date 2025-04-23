import pygambit as gbt

# Pattern: Uniform low integers (0–3)
# Balanced and flat distribution for testing simple zero-sum behavior

players = ["Player1", "Player2", "Player3", "Player4"]
p1_actions = ["A1", "A2", "A3", "A4"]
p2_actions = ["B1", "B2", "B3", "B4"]
p3_actions = ["C1", "C2", "C3", "C4"]
p4_actions = ["D1", "D2", "D3", "D4"]

base_payoffs = {
    "Player1": [0, 1, 2, 3],
    "Player2": [3, 2, 1, 0],
    "Player3": [1, 0, 3, 2],
    "Player4": [2, 3, 0, 1]
}

def adjusted_payoffs(i, j, k, l):
    raw = [
        base_payoffs["Player1"][i],
        base_payoffs["Player2"][j],
        base_payoffs["Player3"][k],
        base_payoffs["Player4"][l]
    ]
    avg = sum(raw) / 4
    return [round(p - avg, 2) for p in raw]

# Build the extensive-form game tree
g = gbt.Game.new_tree(players=players, title="Four-player zero-sum V1 - Uniform Low Integers")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        g.append_move(n2, players[2], p3_actions)
        for k, n3 in enumerate(n2.children):
            g.append_move(n3, players[3], p4_actions)
            for l, n4 in enumerate(n3.children):
                adj = adjusted_payoffs(i, j, k, l)
                label = f"Outcome_{p1_actions[i]}_{p2_actions[j]}_{p3_actions[k]}_{p4_actions[l]}"
                g.set_outcome(n4, g.add_outcome(adj, label=label))
