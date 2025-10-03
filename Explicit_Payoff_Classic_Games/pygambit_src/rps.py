import random
import pygambit as gbt

# ------------------------------------------------------------
# 2-player, 3-action Extensive Form (sequential moves)
# Rock–Paper–Scissors payoff logic with random payoff magnitude.
#
# Zero-sum: Player2 payoff = – Player1 payoff.
# Actions: Rock, Paper, Scissors
# ------------------------------------------------------------

players = ["Player1", "Player2"]
actions = ["Rock", "Paper", "Scissors"]

def sample_rps_payoff():
    """Return a single integer magnitude for the win payoff."""
    return random.randint(2, 10)

# Sample payoff magnitude
win = sample_rps_payoff()
lose = -win
tie = 0

# Outcome mapping (row = P1, col = P2)
# Rock beats Scissors, Scissors beats Paper, Paper beats Rock
U = {
    (0, 0): (tie, tie),   # Rock, Rock
    (0, 1): (lose, win),  # Rock, Paper
    (0, 2): (win, lose),  # Rock, Scissors
    (1, 0): (win, lose),  # Paper, Rock
    (1, 1): (tie, tie),   # Paper, Paper
    (1, 2): (lose, win),  # Paper, Scissors
    (2, 0): (lose, win),  # Scissors, Rock
    (2, 1): (win, lose),  # Scissors, Paper
    (2, 2): (tie, tie),   # Scissors, Scissors
}

def _u_pair(i, j):
    u1, u2 = U[(i, j)]
    return [u1, u2]

# Build the game tree
title = "3x3 Rock Paper Scissors Variant"
g = gbt.Game.new_tree(players=players, title=title)

# Player 1 move at root
g.append_move(g.root, players[0], actions)

# Player 2 moves after observing P1
for i, n1 in enumerate(g.root.children):
    g.append_move(n1, players[1], actions)
    for j, n2 in enumerate(n1.children):
        label = f"Outcome_{i}{j}"
        g.set_outcome(n2, g.add_outcome(_u_pair(i, j), label=label))
