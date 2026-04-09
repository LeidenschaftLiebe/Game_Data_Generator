from pathlib import Path
import pygambit as gbt


def build_memory_action_recall_fig6_v0():
    g = gbt.Game.new_tree(
        players=["Player 1"],
        title="Memory and Perfect Recall Fig 6 V0"
    )

    # Nature chooses the entry
    g.append_move(g.root, g.players.chance, actions=["entryA", "entryB"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    entry_a = g.root.children["entryA"]
    entry_b = g.root.children["entryB"]

    # First junction
    g.append_move(entry_a, "Player 1", actions=["left1", "right1"])
    g.append_move(entry_b, "Player 1", actions=["left1", "right1"])

    # Second junction after entry A then left1
    a_left1 = entry_a.children["left1"]
    g.append_move(a_left1, "Player 1", actions=["left2", "right2"])

    # Second junction after entry A then right1
    a_right1 = entry_a.children["right1"]
    g.append_move(a_right1, "Player 1", actions=["left2", "right2"])

    # Second junction after entry B then left1
    b_left1 = entry_b.children["left1"]
    g.append_move(b_left1, "Player 1", actions=["left2", "right2"])

    # Second junction after entry B then right1
    b_right1 = entry_b.children["right1"]
    g.append_move(b_right1, "Player 1", actions=["left2", "right2"])

    # Final junction x after entry A -> right1 -> left2
    x_node = a_right1.children["left2"]
    g.append_move(x_node, "Player 1", actions=["left3", "right3"])

    # Final junction y after entry B -> right1 -> left2, same information set as x
    y_node = b_right1.children["left2"]
    g.append_infoset(y_node, x_node.infoset)

    # Distinct outcomes for every terminal node
    out_a_left1_left2_blocked = g.add_outcome([0], label="entryA_left1_left2_blocked")
    out_a_left1_right2_blocked = g.add_outcome([0], label="entryA_left1_right2_blocked")
    out_a_right1_right2_blocked = g.add_outcome([0], label="entryA_right1_right2_blocked")

    out_b_left1_left2_blocked = g.add_outcome([0], label="entryB_left1_left2_blocked")
    out_b_left1_right2_blocked = g.add_outcome([0], label="entryB_left1_right2_blocked")
    out_b_right1_right2_blocked = g.add_outcome([0], label="entryB_right1_right2_blocked")

    out_x_left3_exit = g.add_outcome([1], label="A_left3_exit")
    out_x_right3_blocked = g.add_outcome([0], label="A_right3_blocked")
    out_y_left3_blocked = g.add_outcome([0], label="B_left3_blocked")
    out_y_right3_exit = g.add_outcome([1], label="B_right3_exit")

    # Assign blocked outcomes on left branch from entry A
    g.set_outcome(a_left1.children["left2"], out_a_left1_left2_blocked)
    g.set_outcome(a_left1.children["right2"], out_a_left1_right2_blocked)

    # Assign outcomes on right branch from entry A
    g.set_outcome(a_right1.children["right2"], out_a_right1_right2_blocked)

    # Assign blocked outcomes on left branch from entry B
    g.set_outcome(b_left1.children["left2"], out_b_left1_left2_blocked)
    g.set_outcome(b_left1.children["right2"], out_b_left1_right2_blocked)

    # Assign outcomes on right branch from entry B
    g.set_outcome(b_right1.children["right2"], out_b_right1_right2_blocked)

    # Assign final-junction outcomes
    g.set_outcome(x_node.children["left3"], out_x_left3_exit)
    g.set_outcome(x_node.children["right3"], out_x_right3_blocked)
    g.set_outcome(y_node.children["left3"], out_y_left3_blocked)
    g.set_outcome(y_node.children["right3"], out_y_right3_exit)

    return g


if __name__ == "__main__":
    game = build_memory_action_recall_fig6_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



