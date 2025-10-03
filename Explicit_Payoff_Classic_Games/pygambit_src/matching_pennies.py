import pygambit as gbt

# 2-player, 2-action Extensive Form (sequential moves)
# Matching Pennies payoff logic (zero-sum):
#   Match (H,H) or (T,T): Player1 +1, Player2 -1
#   Mismatch (H,T) or (T,H): Player1 -1, Player2 +1

players = ["Player1", "Player2"]
actions = ["Heads", "Tails"]

# rows = P1 action (0=H,1=T), cols = P2 action (0=H,1=T)
U = {
    (0, 0): (1, -1),   # H,H
    (0, 1): (-1, 1),   # H,T
    (1, 0): (-1, 1),   # T,H
    (1, 1): (1, -1),   # T,T
}

def _u_pair(i, j):
    u1, u2 = U[(i, j)]
    return [int(u1), int(u2)]

# Build the game tree (sequential, perfect information)
title = "2x2 Matching Pennies Variant"
g = gbt.Game.new_tree(players=players, title=title)

# Player 1 move at root
g.append_move(g.root, players[0], actions)

# Player 2 moves after observing P1 (same action labels)
for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_{i}{j}"
        g.set_outcome(n2, g.add_outcome(_u_pair(i, j), label=label))
