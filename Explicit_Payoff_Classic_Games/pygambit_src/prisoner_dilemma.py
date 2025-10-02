import random
import pygambit as gbt

# ------------------------------------------------------------
# 2-player, 2-action Extensive Form (sequential moves) with
# Prisoner's Dilemma payoffs embedded in the terminal nodes.
#
# PD constraints enforced:
#   T > R > P > S   and   2R > T + S
# Actions: Cooperate (C), Betray (B)
# Outcome mapping (row, col):
#   (C,C): (R, R)
#   (C,D): (S, T)
#   (D,C): (T, S)
#   (D,D): (P, P)
# ------------------------------------------------------------

players = ["Player1", "Player2"]
actions = ["Cooperate", "Betray"]

def sample_pd_payoffs():
    """Return integers (T, R, P, S) satisfying PD: T>R>P>S and 2R > T+S."""
    # Try until constraints are met (kept simple and fast for small ranges).
    while True:
        R = random.randint(3, 10)                 # baseline mutual-cooperation reward
        T = random.randint(R + 1, R + 5)          # temptation above R
        P = random.randint(max(-5, R - 4), R - 1) # punishment below R
        S = random.randint(max(-10, P - 4), P - 1)# cooperator below P

        if T > R > P > S and 2 * R > T + S:
            return T, R, P, S

# Sample a consistent PD payoff quadruple
T, R, P, S = sample_pd_payoffs()

# Map (row, col) -> (u1, u2) according to PD logic
# rows = Player1's action (0=C, 1=B), cols = Player2's action (0=C, 1=B)
U = {
    (0, 0): (R, R),  # C,C
    (0, 1): (S, T),  # C,B
    (1, 0): (T, S),  # B, C
    (1, 1): (P, P),  # B, B
}

def _u_pair(i, j):
    u1, u2 = U[(i, j)]
    return [int(u1), int(u2)]

# Build the game tree (sequential, perfect information)
title = f"2x2 Prisoner's Dilemma Variant"
g = gbt.Game.new_tree(players=players, title=title)

# Player 1 move at root
g.append_move(g.root, players[0], actions)

# Player 2 moves after observing P1 (same action labels)
for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_{i}{j}"
        g.set_outcome(n2, g.add_outcome(_u_pair(i, j), label=label))
