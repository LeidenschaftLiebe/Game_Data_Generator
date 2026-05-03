from pathlib import Path
import pygambit as gbt


def build_fig4_g2_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 4 G2 V0"
    )

    # Player 1 moves first at h0
    g.append_move(g.root, "Player 1", actions=["L", "R"])
    h0_L = g.root.children["L"]
    h0_R = g.root.children["R"]

    # Immediate terminal outcome after h0 -> R
    out_h0_R = g.add_outcome([2, 2], label="h0_R")
    g.set_outcome(h0_R, out_h0_R)

    # Player 1 moves again after h0 -> L
    g.append_move(h0_L, "Player 1", actions=["L", "R"])
    h1_L = h0_L.children["L"]
    h1_R = h0_L.children["R"]

    # Player 2 moves after h1 -> L
    g.append_move(h1_L, "Player 2", actions=["l", "r"])

    # Player 2 moves after h1 -> R
    g.append_move(h1_R, "Player 2", actions=["l", "r"])

    # Distinct outcomes
    out_L_L_l = g.add_outcome([0, 1], label="L_L_l")
    out_L_L_r = g.add_outcome([0, 0], label="L_L_r")
    out_L_R_l = g.add_outcome([1, 0], label="L_R_l")
    out_L_R_r = g.add_outcome([4, 1], label="L_R_r")

    # Assign outcomes
    g.set_outcome(h1_L.children["l"], out_L_L_l)
    g.set_outcome(h1_L.children["r"], out_L_L_r)
    g.set_outcome(h1_R.children["l"], out_L_R_l)
    g.set_outcome(h1_R.children["r"], out_L_R_r)

    return g


if __name__ == "__main__":
    game = build_fig4_g2_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
