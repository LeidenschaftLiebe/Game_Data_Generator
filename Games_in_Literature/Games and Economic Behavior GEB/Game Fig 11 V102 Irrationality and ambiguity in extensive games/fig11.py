from pathlib import Path
import pygambit as gbt


def build_fig11_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 11 Example 5 V0"
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

    # Player 1 continuation moves
    g.append_move(l_node.children["A"], "Player 1", actions=["C", "D"])
    g.append_move(l_node.children["B"], "Player 1", actions=["E", "F"])
    g.append_move(r_node.children["A"], "Player 1", actions=["G", "H"])
    g.append_move(r_node.children["B"], "Player 1", actions=["J", "K"])

    # Distinct outcomes for every terminal history
    out_o = g.add_outcome([2, 1], label="O")
    out_l_a_c = g.add_outcome([2, 3], label="L_A_C")
    out_l_a_d = g.add_outcome([0, 2], label="L_A_D")
    out_l_b_e = g.add_outcome([1, 4], label="L_B_E")
    out_l_b_f = g.add_outcome([0, 0], label="L_B_F")
    out_r_a_g = g.add_outcome([3, 5], label="R_A_G")
    out_r_a_h = g.add_outcome([0, 1], label="R_A_H")
    out_r_b_j = g.add_outcome([1, 4], label="R_B_J")
    out_r_b_k = g.add_outcome([0, 0], label="R_B_K")

    # Assign outcomes
    g.set_outcome(o_node, out_o)
    g.set_outcome(l_node.children["A"].children["C"], out_l_a_c)
    g.set_outcome(l_node.children["A"].children["D"], out_l_a_d)
    g.set_outcome(l_node.children["B"].children["E"], out_l_b_e)
    g.set_outcome(l_node.children["B"].children["F"], out_l_b_f)
    g.set_outcome(r_node.children["A"].children["G"], out_r_a_g)
    g.set_outcome(r_node.children["A"].children["H"], out_r_a_h)
    g.set_outcome(r_node.children["B"].children["J"], out_r_b_j)
    g.set_outcome(r_node.children["B"].children["K"], out_r_b_k)

    return g


if __name__ == "__main__":
    g = build_fig11_v0()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



