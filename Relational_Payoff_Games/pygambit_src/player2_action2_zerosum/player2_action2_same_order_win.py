import random
import pygambit as gbt

# 2-player, 2-action, perfect-information, zero-sum
players = ["Player1", "Player2"]
p1_actions = ["Action1", "Action2"]
p2_actions = ["Action1", "Action2"]

def _pos_int(lo=1, hi=100):
    return random.randint(lo, hi)

def _two_distinct_pos(lo=1, hi=100):
    a, b = random.randint(lo, hi), random.randint(lo, hi)
    while a == b:
        b = random.randint(lo, hi)
    return a, b

# Row 1 (P1=Action1): tie in P2’s payoffs, both positive (P2 wins vs P1)
v = _pos_int()              # > 0
row1_col1 = v               # (0,0)
row1_col2 = v               # (0,1)

# Row 2 (P1=Action2): P2’s Action1 > Action2, both negative (P2 loses vs P1)
a, b = _two_distinct_pos()  # positive magnitudes
# Make them negative and order so that the one closer to zero is "better" for P2
neg_a, neg_b = -a, -b
high2, low2 = (neg_a, neg_b) if neg_a > neg_b else (neg_b, neg_a)
row2_col1 = high2           # (1,0) better for P2 (less negative)
row2_col2 = low2            # (1,1) worse for P2 (more negative)

# Assemble payoff map for Player 2
P2 = {
    (0, 0): row1_col1,  # tie, positive
    (0, 1): row1_col2,  # tie, positive
    (1, 0): row2_col1,  # better, negative
    (1, 1): row2_col2,  # worse, negative
}

def _u_pair(i, j):
    u2 = int(P2[(i, j)])
    u1 = -u2  # zero-sum
    return [u1, u2]

# Build the game tree (no file I/O here)
g = gbt.Game.new_tree(players=players, title="2x2 PI Zero-Sum (Row1 tie & win for P2; Row2 P2 loses, A1 > A2)")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_{i}{j}"
        g.set_outcome(n2, g.add_outcome(_u_pair(i, j), label=label))
