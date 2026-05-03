from pathlib import Path
import pygambit as gbt


def build_fig4_v0():
    g = gbt.Game.new_tree(
        players=["I", "II", "III"],
        title="Fig. 4 from the article V0"
    )

    # Player I moves first
    g.append_move(g.root, "I", actions=["L", "R"])
    root = g.root

    # Player II moves after L
    after_L = root.children["L"]
    g.append_move(after_L, "II", actions=["l", "r"])
    p2_infoset = after_L.infoset

    # Player II also moves after R, same infoset
    after_R = root.children["R"]
    g.append_infoset(after_R, p2_infoset)

    # Immediate terminal after R then r
    out_R_r = g.add_outcome([0, 0, 0], label="R_then_r")
    g.set_outcome(after_R.children["r"], out_R_r)

    # Player III moves after L then l
    after_L_l = after_L.children["l"]
    g.append_move(after_L_l, "III", actions=["a", "b", "c"])
    p3_infoset = after_L_l.infoset

    # Player III also moves after L then r
    after_L_r = after_L.children["r"]
    g.append_infoset(after_L_r, p3_infoset)

    # Player III also moves after R then l
    after_R_l = after_R.children["l"]
    g.append_infoset(after_R_l, p3_infoset)

    # Outcomes after L then l
    out_L_l_a = g.add_outcome([1, 1, 0], label="L_then_l_then_a")
    out_L_l_b = g.add_outcome([-1, -1, -1], label="L_then_l_then_b")
    out_L_l_c = g.add_outcome([1, 1, 0], label="L_then_l_then_c")

    g.set_outcome(after_L_l.children["a"], out_L_l_a)
    g.set_outcome(after_L_l.children["b"], out_L_l_b)
    g.set_outcome(after_L_l.children["c"], out_L_l_c)

    # Outcomes after L then r
    out_L_r_a = g.add_outcome([1, 0, 0], label="L_then_r_then_a")
    out_L_r_b = g.add_outcome([-1, -1, 1], label="L_then_r_then_b")
    out_L_r_c = g.add_outcome([1, 0, 2], label="L_then_r_then_c")

    g.set_outcome(after_L_r.children["a"], out_L_r_a)
    g.set_outcome(after_L_r.children["b"], out_L_r_b)
    g.set_outcome(after_L_r.children["c"], out_L_r_c)

    # Outcomes after R then l
    out_R_l_a = g.add_outcome([0, 1, 2], label="R_then_l_then_a")
    out_R_l_b = g.add_outcome([-1, -1, 1], label="R_then_l_then_b")
    out_R_l_c = g.add_outcome([0, 1, 0], label="R_then_l_then_c")

    g.set_outcome(after_R_l.children["a"], out_R_l_a)
    g.set_outcome(after_R_l.children["b"], out_R_l_b)
    g.set_outcome(after_R_l.children["c"], out_R_l_c)

    return g


if __name__ == "__main__":
    game = build_fig4_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

    