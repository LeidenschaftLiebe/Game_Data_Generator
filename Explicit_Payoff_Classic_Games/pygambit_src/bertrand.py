import random
import pygambit as gbt

# ------------------------------------------------------------
# 2-player, 2-action Extensive Form (sequential, perfect info)
# Hawk-Dove (Chicken) payoff structure:
# Actions: Hawk (H), Dove (D)
#
# Typical ordering:
#   Hawk vs Dove  : Hawk high reward, Dove small/negative
#   Dove vs Hawk  : Dove small/negative, Hawk high reward
#   Dove vs Dove  : both moderate reward
#   Hawk vs Hawk  : both heavy penalty
#
# Constraint idea: Reward > Moderate > Small > HeavyPenalty
# ------------------------------------------------------------

players = ["Player1", "Player2"]
actions  = ["Hawk", "Dove"]

def sample_hawk_dove():
    """
    Sample integer payoffs consistent with Hawk-Dove logic:
    reward (R) > moderate (M) > small (S) > penalty (P).
    """
    while True:
        R = random.randint(8, 15)               # Hawk's reward vs Dove
        M = random.randint(4, R - 2)            # Mutual Dove payoff
        S = random.randint(0, M - 1)            # Dove vs Hawk (smaller)
        P = random.randint(-10, S - 1)          # Mutual Hawk penalty
        if R > M > S > P:
            return R, M, S, P

# Draw a consistent payoff quadruple
R, M, S, P = sample_hawk_dove()

# Map (row, col) -> (u1, u2)
# rows = Player1 action (0=Hawk, 1=Dove), cols = Player2 action (0=Hawk, 1=Dove)
U = {
    (0, 0): (P, P),  # Hawk vs Hawk
    (0, 1): (R, S),  # Hawk vs Dove
    (1, 0): (S, R),  # Dove vs Hawk
    (1, 1): (M, M),  # Dove vs Dove
}

def _u_pair(i, j):
    u1, u2 = U[(i, j)]
    return [int(u1), int(u2)]

# Build the game tree (sequential, perfect information)
title = f"2x2 Hawk-Dove Variant"
g = gbt.Game.new_tree(players=players, title=title)

# Player 1 acts at root
g.append_move(g.root, players[0], actions)

# Player 2 acts after observing Player 1
for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_{i}{j}"
        g.set_outcome(n2, g.add_outcome(_u_pair(i, j), label=label))
