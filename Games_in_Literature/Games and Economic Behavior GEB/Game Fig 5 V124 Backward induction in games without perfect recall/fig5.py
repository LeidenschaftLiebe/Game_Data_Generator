from pathlib import Path
import pygambit as gbt


def build_geb_need_beliefs_about_strategies_fig5() -> gbt.Game:
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Need Beliefs About Strategies Fig. 5"
    )

    # Player 1 moves first
    g.append_move(g.root, player="Player 1", actions=["X", "T", "B"])
    node_X = g.root.children["X"]
    node_T = g.root.children["T"]
    node_B = g.root.children["B"]

    # Immediate terminal after X
    out_X = g.add_outcome([4, 4], label="X")
    g.set_outcome(node_X, out_X)

    # Player 2 moves after T and B; these two nodes are in one infoset
    g.append_move(node_T, player="Player 2", actions=["L", "R"])
    g.append_infoset(node_B, node_T.infoset)

    node_TL = node_T.children["L"]
    node_TR = node_T.children["R"]
    node_BL = node_B.children["L"]
    node_BR = node_B.children["R"]

    # Player 1 moves at the four upper nodes; all four are in one infoset
    g.append_move(node_TL, player="Player 1", actions=["U", "D"])
    g.append_infoset(node_TR, node_TL.infoset)
    g.append_infoset(node_BL, node_TL.infoset)
    g.append_infoset(node_BR, node_TL.infoset)

    # Terminal outcomes
    out_TL_U = g.add_outcome([5, 0], label="T_L_U")
    out_TL_D = g.add_outcome([2, 1], label="T_L_D")

    out_TR_U = g.add_outcome([2, 0], label="T_R_U")
    out_TR_D = g.add_outcome([0, 1], label="T_R_D")

    out_BL_U = g.add_outcome([0, 1], label="B_L_U")
    out_BL_D = g.add_outcome([2, 0], label="B_L_D")

    out_BR_U = g.add_outcome([2, 1], label="B_R_U")
    out_BR_D = g.add_outcome([5, 0], label="B_R_D")

    g.set_outcome(node_TL.children["U"], out_TL_U)
    g.set_outcome(node_TL.children["D"], out_TL_D)

    g.set_outcome(node_TR.children["U"], out_TR_U)
    g.set_outcome(node_TR.children["D"], out_TR_D)

    g.set_outcome(node_BL.children["U"], out_BL_U)
    g.set_outcome(node_BL.children["D"], out_BL_D)

    g.set_outcome(node_BR.children["U"], out_BR_U)
    g.set_outcome(node_BR.children["D"], out_BR_D)

    return g


if __name__ == "__main__":
    g = build_geb_need_beliefs_about_strategies_fig5()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


