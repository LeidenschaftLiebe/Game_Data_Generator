from pathlib import Path
import pygambit as gbt


def build_appendix_tree_v0():
    g = gbt.Game.new_tree(
        players=["First Mover", "Second Mover"],
        title="GEB Appendix Instruction Tree V0"
    )

    # First Mover at the root
    g.append_move(g.root, "First Mover", actions=["A", "B", "C"])
    node_a = g.root.children["A"]
    node_b = g.root.children["B"]
    node_c = g.root.children["C"]

    # Second Mover responds after each branch
    g.append_move(node_a, "Second Mover", actions=["LA", "RA"])
    g.append_move(node_b, "Second Mover", actions=["LB", "RB"])
    g.append_move(node_c, "Second Mover", actions=["LC", "RC"])

    # Distinct outcomes for every terminal history
    out_a_la = g.add_outcome([20, 35], label="A_LA")
    out_a_ra = g.add_outcome([40, 15], label="A_RA")

    out_b_lb = g.add_outcome([10, 20], label="B_LB")
    out_b_rb = g.add_outcome([90, 75], label="B_RB")

    out_c_lc = g.add_outcome([70, 50], label="C_LC")
    out_c_rc = g.add_outcome([30, 50], label="C_RC")

    # Assign outcomes
    g.set_outcome(node_a.children["LA"], out_a_la)
    g.set_outcome(node_a.children["RA"], out_a_ra)

    g.set_outcome(node_b.children["LB"], out_b_lb)
    g.set_outcome(node_b.children["RB"], out_b_rb)

    g.set_outcome(node_c.children["LC"], out_c_lc)
    g.set_outcome(node_c.children["RC"], out_c_rc)

    return g


if __name__ == "__main__":
    game = build_appendix_tree_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

