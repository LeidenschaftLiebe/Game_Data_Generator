from pathlib import Path
import pygambit as gbt


def build_geb_no_one_deviation_fig3() -> gbt.Game:
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB No One-Deviation Property Fig. 3"
    )

    # Player 1 moves first
    g.append_move(g.root, player="Player 1", actions=["T", "B"])

    node_T = g.root.children["T"]
    node_B = g.root.children["B"]

    # Immediate terminal after T
    out_T = g.add_outcome([2, 6], label="T")
    g.set_outcome(node_T, out_T)

    # Player 2 moves at lower node after B
    g.append_move(node_B, player="Player 2", actions=["U", "D"])
    node_U = node_B.children["U"]
    node_D = node_B.children["D"]

    # Player 2 moves again at upper infoset, without distinguishing U from D
    g.append_move(node_U, player="Player 2", actions=["L", "R"])
    g.append_infoset(node_D, node_U.infoset)

    # Distinct terminal outcomes
    out_UL = g.add_outcome([4, 4], label="U_L")
    out_UR = g.add_outcome([0, 0], label="U_R")
    out_DL = g.add_outcome([0, 0], label="D_L")
    out_DR = g.add_outcome([1, 1], label="D_R")

    g.set_outcome(node_U.children["L"], out_UL)
    g.set_outcome(node_U.children["R"], out_UR)
    g.set_outcome(node_D.children["L"], out_DL)
    g.set_outcome(node_D.children["R"], out_DR)

    return g


if __name__ == "__main__":
    g = build_geb_no_one_deviation_fig3()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


