from pathlib import Path
import pygambit as gbt


def build_fig4_v0():
    g = gbt.Game.new_tree(
        players=["Alice", "Bob"],
        title="GEB Fig. 4 Another Signaling Game V0"
    )

    # Nature determines Alice's type
    g.append_move(g.root, g.players.chance, actions=["One", "Two"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 10), gbt.Rational(9, 10)])

    one_node = g.root.children["One"]
    two_node = g.root.children["Two"]

    # Alice moves after each type is realized
    g.append_move(one_node, "Alice", actions=["Out1", "In1"])
    g.append_move(two_node, "Alice", actions=["Out2", "In2"])

    out1_node = one_node.children["Out1"]
    in1_node = one_node.children["In1"]
    out2_node = two_node.children["Out2"]
    in2_node = two_node.children["In2"]

    # Immediate terminal outcomes if Alice chooses Out
    out_one = g.add_outcome([0, 0], label="One_Out1")
    out_two = g.add_outcome([0, 0], label="Two_Out2")
    g.set_outcome(out1_node, out_one)
    g.set_outcome(out2_node, out_two)

    # Bob moves after In1, and has the same information after In2
    g.append_move(in1_node, "Bob", actions=["U", "M", "D"])
    bob_infoset = in1_node.infoset
    g.append_infoset(in2_node, bob_infoset)

    # Distinct outcomes for every terminal history
    one_u = g.add_outcome([-1, 3], label="One_In1_U")
    one_m = g.add_outcome([-1, 2], label="One_In1_M")
    one_d = g.add_outcome([2, 0], label="One_In1_D")

    two_u = g.add_outcome([-3, 0], label="Two_In2_U")
    two_m = g.add_outcome([-1, 2], label="Two_In2_M")
    two_d = g.add_outcome([3, 3], label="Two_In2_D")

    g.set_outcome(in1_node.children["U"], one_u)
    g.set_outcome(in1_node.children["M"], one_m)
    g.set_outcome(in1_node.children["D"], one_d)

    g.set_outcome(in2_node.children["U"], two_u)
    g.set_outcome(in2_node.children["M"], two_m)
    g.set_outcome(in2_node.children["D"], two_d)

    return g


if __name__ == "__main__":
    game = build_fig4_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



