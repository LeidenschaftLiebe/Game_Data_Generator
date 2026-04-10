from pathlib import Path
import pygambit as gbt


def build_dynamic_consistency_fig1_v0():
    g = gbt.Game.new_tree(
        players=["1"],
        title="Dynamic Consistency and Imperfect Recall Figure 1 V0"
    )

    # Initial decision d0
    g.append_move(g.root, "1", actions=["T", "G"])
    d0 = g.root

    # Immediate terminal after T
    out_take_T = g.add_outcome([3], label="choose_T")
    g.set_outcome(d0.children["T"], out_take_T)

    # Chance after G
    chance_node = d0.children["G"]
    g.append_move(chance_node, g.players.chance, actions=["l", "r"])
    g.set_chance_probs(chance_node.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    left_branch = chance_node.children["l"]
    right_branch = chance_node.children["r"]

    # d1 after l
    g.append_move(left_branch, "1", actions=["E", "D"])
    d1 = left_branch

    # d2 after r
    g.append_move(right_branch, "1", actions=["E", "D"])
    d2 = right_branch

    # Immediate exits
    out_d1_E = g.add_outcome([2], label="d1_then_E")
    out_d2_E = g.add_outcome([2], label="d2_then_E")
    g.set_outcome(d1.children["E"], out_d1_E)
    g.set_outcome(d2.children["E"], out_d2_E)

    # d3 after D from either branch
    d3_left = d1.children["D"]
    g.append_move(d3_left, "1", actions=["L", "R"])
    d3_infoset = d3_left.infoset

    d3_right = d2.children["D"]
    g.append_infoset(d3_right, d3_infoset)

    # Outcomes after d3
    out_left_L = g.add_outcome([5], label="after_l_then_L")
    out_left_R = g.add_outcome([0], label="after_l_then_R")
    out_right_L = g.add_outcome([0], label="after_r_then_L")
    out_right_R = g.add_outcome([6], label="after_r_then_R")

    g.set_outcome(d3_left.children["L"], out_left_L)
    g.set_outcome(d3_left.children["R"], out_left_R)
    g.set_outcome(d3_right.children["L"], out_right_L)
    g.set_outcome(d3_right.children["R"], out_right_R)

    return g


if __name__ == "__main__":
    game = build_dynamic_consistency_fig1_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



    