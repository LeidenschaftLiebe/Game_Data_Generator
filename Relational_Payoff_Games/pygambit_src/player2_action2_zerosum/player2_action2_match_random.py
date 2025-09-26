import random
import pygambit as gbt

# 2-player, 2-action, perfect-information, zero-sum
players = ["Player1", "Player2"]
p1_actions = ["Action1", "Action2"]
p2_actions = ["Action1", "Action2"]

def _ordered_pair_signed(lo=10, hi=123):
    """Return a strictly ordered pair (low < 0 < high)."""
    low = -random.randint(lo, hi)   # negative
    high =  random.randint(lo, hi)  # positive
    return low, high


# Sample strictly ordered payoffs for Player 2 on each row:
# Row 1 (P1=Action1): P2 prefers col1 > col2
low1, high1 = _ordered_pair_signed()
# Row 2 (P1=Action2): P2 prefers col2 > col1
low2, high2 = _ordered_pair_signed()

# Map (row, col) -> P2 payoff (strictly ordered as specified)
# (0,0)=high1 > (0,1)=low1 ; (1,1)=high2 > (1,0)=low2
P2 = {
    (0, 0): high1,
    (0, 1): low1,
    (1, 0): low2,
    (1, 1): high2,
}

def _u_pair(i, j):
    u2 = float(P2[(i, j)])
    u1 = -u2  # zero-sum
    return [u1, u2]

# Build the game tree (no file I/O here)
g = gbt.Game.new_tree(players=players, title="2x2 PI Zero-Sum (row-match better for P2)")
g.append_move(g.root, players[0], p1_actions)

for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], p2_actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_{i}{j}"
        g.set_outcome(n2, g.add_outcome(_u_pair(i, j), label=label))
