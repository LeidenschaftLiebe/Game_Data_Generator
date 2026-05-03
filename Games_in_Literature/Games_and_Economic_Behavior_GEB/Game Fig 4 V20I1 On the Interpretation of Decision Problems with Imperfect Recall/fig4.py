from pathlib import Path
import pygambit as gbt


def build_example4_v0():
    g = gbt.Game.new_tree(
        players=["1"],
        title="Imperfect Recall Example 4 V0"
    )

    # First d1 node
    g.append_move(g.root, "1", actions=["L", "R"])
    first_d1 = g.root

    # Immediate terminal after first d1 then R
    out_first_R = g.add_outcome([0], label="first_d1_then_R")
    g.set_outcome(first_d1.children["R"], out_first_R)

    # Second d1 node, in the same information set as the first d1 node
    second_d1 = first_d1.children["L"]
    g.append_infoset(second_d1, first_d1.infoset)

    # d2 nodes reached after second d1
    left_d2 = second_d1.children["L"]
    right_d2 = second_d1.children["R"]

    # Build d2 move at left node
    g.append_move(left_d2, "1", actions=["L", "R"])
    d2_infoset = left_d2.infoset

    # Right d2 node is in the same information set
    g.append_infoset(right_d2, d2_infoset)

    # Distinct outcomes
    out_left_d2_L = g.add_outcome([1], label="left_d2_then_L")
    out_left_d2_R = g.add_outcome([0], label="left_d2_then_R")
    out_right_d2_L = g.add_outcome([0], label="right_d2_then_L")
    out_right_d2_R = g.add_outcome([3], label="right_d2_then_R")

    # Assign outcomes
    g.set_outcome(left_d2.children["L"], out_left_d2_L)
    g.set_outcome(left_d2.children["R"], out_left_d2_R)
    g.set_outcome(right_d2.children["L"], out_right_d2_L)
    g.set_outcome(right_d2.children["R"], out_right_d2_R)

    return g


if __name__ == "__main__":
    game = build_example4_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


    