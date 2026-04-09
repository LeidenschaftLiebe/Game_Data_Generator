from pathlib import Path
import pygambit as gbt


def build_gamma2_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 2 Gamma2 V0"
    )

    # Player 1 moves first
    g.append_move(g.root, "Player 1", actions=["L", "M", "R"])
    node_L = g.root.children["L"]
    node_M = g.root.children["M"]
    node_R = g.root.children["R"]

    # L ends immediately
    out_L = g.add_outcome([2, 2], label="L")
    g.set_outcome(node_L, out_L)

    # After M, Player 2 moves
    g.append_move(node_M, "Player 2", actions=["l", "r"])
    p2_infoset = node_M.infoset

    # After R, Player 2 moves at the same infoset
    g.append_infoset(node_R, p2_infoset)

    # Distinct outcomes
    out_M_l = g.add_outcome([4, 1], label="M_l")
    out_M_r = g.add_outcome([1, 0], label="M_r")
    out_R_l = g.add_outcome([3, 0], label="R_l")
    out_R_r = g.add_outcome([0, 3], label="R_r")

    # Assign outcomes
    g.set_outcome(node_M.children["l"], out_M_l)
    g.set_outcome(node_M.children["r"], out_M_r)
    g.set_outcome(node_R.children["l"], out_R_l)
    g.set_outcome(node_R.children["r"], out_R_r)

    return g


if __name__ == "__main__":
    game = build_gamma2_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



