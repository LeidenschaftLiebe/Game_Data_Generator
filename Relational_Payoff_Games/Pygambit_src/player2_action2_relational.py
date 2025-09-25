import pygambit as gbt

# Players
g = gbt.Game.new_tree(players=["Hacker","Defender"], title="Hacker vs Firewall 3x3 (simultaneous)")
# Root: Hacker moves first with three actions
root = g.root
I1 = root.append_move(g.players[0], 3)      # actions indexed 0..2
I1.label = "Hacker chooses exploit"
I1.actions[0].label, I1.actions[1].label, I1.actions[2].label = "A","B","C"

# Defender moves second WITHOUT observing Hacker: one information set connecting the three nodes
# Create one infoset for Defender and attach to each of the 3 child nodes of the root
I2 = None
for a in I1.actions:
    node = a.outcome  # this is the next decision node after Hacker’s action
    if I2 is None:
        I2 = node.append_move(g.players[1], 3)
        I2.label = "Defender chooses firewall"
        I2.actions[0].label, I2.actions[1].label, I2.actions[2].label = "A","B","C"
    else:
        node.set_player(I2)   # merge nodes into the same information set

# Assign ordinal, zero-sum payoffs at the 3x3 terminals (P2: 2>1>0; P1 is negative)
# Mapping from (Hacker,Defender) to P2 payoff:
order = {
    ("A","A"):2, ("A","B"):1, ("A","C"):0,
    ("B","B"):2, ("B","C"):1, ("B","A"):0,
    ("C","C"):2, ("C","A"):1, ("C","B"):0,
}
# Fill terminal payoffs
for i,a1 in enumerate(["A","B","C"]):
    for j,a2 in enumerate(["A","B","C"]):
        term = I2.actions[j].outcome  # after Defender’s choice
        if term.is_terminal:
            p2 = order[(a1,a2)]
            term.set_payoffs([-p2, p2])  # zero-sum: P1 = -P2