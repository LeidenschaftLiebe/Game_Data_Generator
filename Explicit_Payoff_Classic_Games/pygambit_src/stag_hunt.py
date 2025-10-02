import random
import pygambit as gbt

# ------------------------------------------------------------
# 2-player, 2-action Extensive Form (sequential, perfect info)
# Stag Hunt payoff structure:
# Actions: Stag (S), Hare (H)
#
# Payoff ordering enforced: a > b > d > c
# Outcomes (row = P1, col = P2):
#   (S,S): (a, a)    - both cooperate on stag (highest for both)
#   (S,H): (c, d)    - P1 goes stag alone (worst), P2 plays safe
#   (H,S): (d, c)    - P1 plays safe, P2 goes stag alone (worst)
#   (H,H): (b, b)    - both play safe hare (middle for both)
# ------------------------------------------------------------

players = ["Player1", "Player2"]
actions  = ["Stag", "Hare"]

def sample_stag_hunt():
    """
    Sample integer payoffs (a, b, d, c) such that a > b > d > c.
    Typical shape: a high, b medium, d small, c worst (often 0 or negative is allowed).
    """
    while True:
        a = random.randint(10, 25)             # high mutual-stag payoff
        b = random.randint(5, a - 1)           # mutual-hare payoff below a
        d = random.randint(max(-5, b - 5), b - 1)  # hare-vs-stag payoff below b
        c = random.randint(max(-10, d - 5), d - 1) # worst payoff below d
        if a > b > d > c:
            return a, b, d, c

# Draw a consistent Stag Hunt quadruple
a, b, d, c = sample_stag_hunt()

# Map (row, col) -> (u1, u2)
# rows = Player1's action (0=Stag, 1=Hare), cols = Player2's action (0=Stag, 1=Hare)
U = {
    (0, 0): (a, a),  # S,S
    (0, 1): (c, d),  # S,H
    (1, 0): (d, c),  # H,S
    (1, 1): (b, b),  # H,H
}

def _u_pair(i, j):
    u1, u2 = U[(i, j)]
    return [int(u1), int(u2)]

# Build the game tree (sequential, perfect information)
title = f"2x2 Stag Hunt (a={a}, b={b}, d={d}, c={c})"
g = gbt.Game.new_tree(players=players, title=title)

# Player 1 acts at the root
g.append_move(g.root, players[0], actions)

# Player 2 moves after observing Player 1 (same action labels)
for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_{i}{j}"
        g.set_outcome(n2, g.add_outcome(_u_pair(i, j), label=label))
