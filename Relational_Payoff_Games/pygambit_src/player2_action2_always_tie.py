import random
import pygambit as gbt

# 2-player, 2-action, perfect-information, zero-sum
players = ["Player1", "Player2"]
p1_actions = ["Action1", "Action2"]
p2_actions = ["Action1", "Action2"]

# Row 1 (P1=Action1): tie for P2, both negative
v_neg = -random.randint(1, 100)

# Row 2 (P1=Action2): tie for P2, both positive
v_pos =  random.randint(1, 100)

# Map (row, col) -> P2 payoff
P2 = {
    (0, 0): v_neg,  # tie, negative
    (0, 1): v_neg,  # tie, negative
    (1, 0): v_pos,  # tie, positive
    (1, 1): v_pos,  # tie, positive
}

def _u_pair(i, j):
    u2 = int(P2[(i, j)])
    u1 = -u2  # zero-sum
    return [u1, u2]

# Build the game tree (no file I/O here)
g = gbt.Game.new_tree(players=players, title="2x2 PI Zero-Sum (Row1 tie & P2 loses; Row2 tie & P2 wins)")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_{i}{j}"
        g.set_outcome(n2, g.add_outcome(_u_pair(i, j), label=label))
