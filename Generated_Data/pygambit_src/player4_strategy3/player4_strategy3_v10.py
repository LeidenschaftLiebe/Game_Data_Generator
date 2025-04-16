import pygambit as gbt

# Pattern: Alternating highs and lows
# This is version V10 — 4 players, 3 strategies each

players = ["Player1", "Player2", "Player3", "Player4"]
p1_actions = ["A1", "A2", "A3"]
p2_actions = ["B1", "B2", "B3"]
p3_actions = ["C1", "C2", "C3"]
p4_actions = ["D1", "D2", "D3"]

base_payoffs = {
    "Player1": [10, -10, 10],
    "Player2": [-5, 5, -5],
    "Player3": [8, -8, 8],
    "Player4": [-2, 2, -2],
}

def adjusted_payoffs(i, j, k, l):
    raw = [
        base_payoffs["Player1"][i],
        base_payoffs["Player2"][j],
        base_payoffs["Player3"][k],
        base_payoffs["Player4"][l]
    ]
    avg = sum(raw) / 4
    return [round(p - avg, 4) for p in raw]

g = gbt.Game.new_tree(players=players, title="Four-player zero-sum V10 - Alternating highs and lows")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        g.append_move(n2, players[2], p3_actions)
        for k, n3 in enumerate(n2.children):
            g.append_move(n3, players[3], p4_actions)
            for l, n4 in enumerate(n3.children):
                label = f"Outcome_V10_{i}{j}{k}{l}"
                g.set_outcome(n4, g.add_outcome(adjusted_payoffs(i, j, k, l), label=label))
