import pygambit as gbt
import random

# 2-player, 2-action Extensive Form (sequential moves)
# Matching Pennies payoff logic (zero-sum):
#   Match (H,H) or (T,T): Player1 +1, Player2 -1
#   Mismatch (H,T) or (T,H): Player1 -1, Player2 +1

players = ["Player1", "Player2"]
actions = ["Heads", "Tails"]

def sample_mp_payoff():
    """Return a single integer magnitude for Player1's win."""
    return random.randint(3, 11)

# Sample payoff magnitude
win = sample_mp_payoff()
lose = -win  # strict zero-sum

# rows = P1 action (0=H,1=T), cols = P2 action (0=H,1=T)
U = {
    (0, 0): (win, lose),   # H,H
    (0, 1): (lose, win),   # H,T
    (1, 0): (lose, win),   # T,H
    (1, 1): (win, lose),   # T,T
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
