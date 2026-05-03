from pathlib import Path
import pygambit as gbt


def build_fig10_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 10 Example 6 V0"
    )

    # Player 1 moves first
    g.append_move(g.root, "Player 1", actions=["O", "L", "R"])
    o_node = g.root.children["O"]
    l_node = g.root.children["L"]
    r_node = g.root.children["R"]

    # Player 2 moves after L, and the node after R is in the same infoset
    g.append_move(l_node, "Player 2", actions=["A", "B"])
    shared_infoset = l_node.infoset
    g.append_infoset(r_node, shared_infoset)

    # Distinct outcomes for every terminal history
    out_o = g.add_outcome([2, 6], label="O")
    out_l_a = g.add_outcome([0, 1], label="L_A")
    out_l_b = g.add_outcome([3, 2], label="L_B")
    out_r_a = g.add_outcome([-1, 3], label="R_A")
    out_r_b = g.add_outcome([1, 2], label="R_B")

    # Assign outcomes
    g.set_outcome(o_node, out_o)
    g.set_outcome(l_node.children["A"], out_l_a)
    g.set_outcome(l_node.children["B"], out_l_b)
    g.set_outcome(r_node.children["A"], out_r_a)
    g.set_outcome(r_node.children["B"], out_r_b)

    return g


if __name__ == "__main__":
    g = build_fig10_v0()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

