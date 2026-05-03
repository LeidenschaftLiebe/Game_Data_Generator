from pathlib import Path
import pygambit as gbt


def build_fig5_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2", "Player 3"],
        title="GEB Fig. 5 Three-Person Outside Option Game V0"
    )

    # Player 1 moves first
    g.append_move(g.root, "Player 1", actions=["Out", "T", "B"])
    out_node = g.root.children["Out"]
    t_node = g.root.children["T"]
    b_node = g.root.children["B"]

    # Out ends the game immediately
    out_outcome = g.add_outcome([2, 2, 2], label="Out")
    g.set_outcome(out_node, out_outcome)

    # Player 2 moves after T, with the node after B in the same infoset
    g.append_move(t_node, "Player 2", actions=["L", "R"])
    p2_infoset = t_node.infoset
    g.append_infoset(b_node, p2_infoset)

    t_l = t_node.children["L"]
    t_r = t_node.children["R"]
    b_l = b_node.children["L"]
    b_r = b_node.children["R"]

    # Player 3 moves after T-L, and the other three nodes are in the same infoset
    g.append_move(t_l, "Player 3", actions=["U", "M", "D"])
    p3_infoset = t_l.infoset
    g.append_infoset(t_r, p3_infoset)
    g.append_infoset(b_l, p3_infoset)
    g.append_infoset(b_r, p3_infoset)

    # Distinct outcomes for every terminal history
    out_t_l_u = g.add_outcome([3, 1, 1], label="T_L_U")
    out_t_l_m = g.add_outcome([0, 0, -1], label="T_L_M")
    out_t_l_d = g.add_outcome([0, 2, 0], label="T_L_D")

    out_t_r_u = g.add_outcome([0, 0, 1], label="T_R_U")
    out_t_r_m = g.add_outcome([0, 1, -1], label="T_R_M")
    out_t_r_d = g.add_outcome([0, 3, 0], label="T_R_D")

    out_b_l_u = g.add_outcome([0, 1, 0], label="B_L_U")
    out_b_l_m = g.add_outcome([0, 0, -1], label="B_L_M")
    out_b_l_d = g.add_outcome([0, 2, 1], label="B_L_D")

    out_b_r_u = g.add_outcome([0, 0, 0], label="B_R_U")
    out_b_r_m = g.add_outcome([0, 1, -1], label="B_R_M")
    out_b_r_d = g.add_outcome([3, 1, 1], label="B_R_D")

    # Assign outcomes
    g.set_outcome(t_l.children["U"], out_t_l_u)
    g.set_outcome(t_l.children["M"], out_t_l_m)
    g.set_outcome(t_l.children["D"], out_t_l_d)

    g.set_outcome(t_r.children["U"], out_t_r_u)
    g.set_outcome(t_r.children["M"], out_t_r_m)
    g.set_outcome(t_r.children["D"], out_t_r_d)

    g.set_outcome(b_l.children["U"], out_b_l_u)
    g.set_outcome(b_l.children["M"], out_b_l_m)
    g.set_outcome(b_l.children["D"], out_b_l_d)

    g.set_outcome(b_r.children["U"], out_b_r_u)
    g.set_outcome(b_r.children["M"], out_b_r_m)
    g.set_outcome(b_r.children["D"], out_b_r_d)

    return g


if __name__ == "__main__":
    game = build_fig5_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

