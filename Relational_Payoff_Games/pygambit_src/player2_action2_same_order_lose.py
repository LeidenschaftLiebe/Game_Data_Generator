import random
import pygambit as gbt

# 2-player, 2-action, perfect-information, zero-sum
players = ["Player1", "Player2"]
p1_actions = ["Action1", "Action2"]
p2_actions = ["Action1", "Action2"]

def _two_distinct_pos(lo=1, hi=100):
    a, b = random.randint(lo, hi), random.randint(lo, hi)
    while a == b:
        b = random.randint(lo, hi)
    return (a, b) if a > b else (b, a)  # return (high, low)

# Row 1 (P1=Action1): tie for P2, both negative (P2 loses to P1)
v = random.randint(1, 100)
row1_col1 = -v
row1_col2 = -v

# Row 2 (P1=Action2): P2 Action1 > Action2, both positive (P2 wins over P1)
high, low = _two_distinct_pos()
row2_col1 = high  # better for P2
row2_col2 = low   # worse for P2

# Assemble payoff map for Player 2
P2 = {
    (0, 0): row1_col1,  # tie, negative
    (0, 1): row1_col2,  # tie, negative
    (1, 0): row2_col1,  # better, positive
    (1, 1): row2_col2,  # worse, positive
}

def _u_pair(i, j):
    u2 = int(P2[(i, j)])
    u1 = -u2  # zero-sum
    return [u1, u2]

# Build the game tree (no file I/O here)
g = gbt.Game.new_tree(players=players, title="2x2 PI Zero-Sum (Row1 tie & P2 loses; Row2 P2 wins, A1 > A2)")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_{i}{j}"
        g.set_outcome(n2, g.add_outcome(_u_pair(i, j), label=label))

