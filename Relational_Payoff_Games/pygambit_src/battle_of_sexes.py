import random
import pygambit as gbt

# ------------------------------------------------------------
# 2-player, 2-action Extensive Form (sequential, perfect info)
# Battle of the Sexes payoff logic:
# Actions: Opera (O), Football (F)
#
# Coordination on O: (H1, L1) with H1 > L1 >= 0   (Player1 prefers Opera)
# Coordination on F: (L2, H2) with H2 > L2 >= 0   (Player2 prefers Football)
# Mismatch (O,F) or (F,O): (0, 0)
# ------------------------------------------------------------

players = ["Player1", "Player2"]
actions  = ["Opera", "Football"]

def sample_high_low():
    """Sample a single (H, L) pair with integers H > L >= 0."""
    H = random.randint(5, 15)
    L = random.randint(0, H - 1)
    return H, L

H, L = sample_high_low()

# Outcome map: rows = P1 action (0=Opera, 1=Football), cols = P2 action (0=Opera, 1=Football)
U = {
    (0, 0): (H, L),  # Opera, Opera
    (0, 1): (0, 0),  # Opera, Football (mismatch)
    (1, 0): (0, 0),  # Football, Opera (mismatch)
    (1, 1): (L, H),  # Football, Football
}

def _u_pair(i, j):
    u1, u2 = U[(i, j)]
    return [int(u1), int(u2)]

title = f"2x2 Battle of the Sexes Variant"
g = gbt.Game.new_tree(players=players, title=title)

# Player 1 acts at the root
g.append_move(g.root, players[0], actions)

# Player 2 acts after observing Player 1
for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_{i}{j}"
        g.set_outcome(n2, g.add_outcome(_u_pair(i, j), label=label))

