from pathlib import Path
import pygambit as gbt


def build_fig4_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2", "Player 3", "Player 4"],
        title="GEB Fig. 4 Inference Example V0"
    )

    # Player 1
    g.append_move(g.root, "Player 1", actions=["Out1", "In1"])
    out1 = g.root.children["Out1"]
    in1 = g.root.children["In1"]

    # Player 2
    g.append_move(in1, "Player 2", actions=["Out2", "In2"])
    out2 = in1.children["Out2"]
    in2 = in1.children["In2"]

    # Player 3
    g.append_move(in2, "Player 3", actions=["L3", "R3"])
    l3 = in2.children["L3"]
    r3 = in2.children["R3"]

    # Player 4 after L3
    g.append_move(l3, "Player 4", actions=["L4", "R4"])

    # Player 4 after R3 shares infoset
    g.append_infoset(r3, l3.infoset)

    # Outcomes
    out_out1 = g.add_outcome([0, 0, 0, 0], label="Out1")
    out_out2 = g.add_outcome([-1, 0, 0, 0], label="In1_Out2")
    out_l3_l4 = g.add_outcome([1, 1, 1, 1], label="In1_In2_L3_L4")
    out_l3_r4 = g.add_outcome([1, -5, 0, 0], label="In1_In2_L3_R4")
    out_r3_l4 = g.add_outcome([1, -5, 0, 0], label="In1_In2_R3_L4")
    out_r3_r4 = g.add_outcome([1, -5, 1, 1], label="In1_In2_R3_R4")

    # Assign outcomes
    g.set_outcome(out1, out_out1)
    g.set_outcome(out2, out_out2)
    g.set_outcome(l3.children["L4"], out_l3_l4)
    g.set_outcome(l3.children["R4"], out_l3_r4)
    g.set_outcome(r3.children["L4"], out_r3_l4)
    g.set_outcome(r3.children["R4"], out_r3_r4)

    return g


if __name__ == "__main__":
    g = build_fig4_v0()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
