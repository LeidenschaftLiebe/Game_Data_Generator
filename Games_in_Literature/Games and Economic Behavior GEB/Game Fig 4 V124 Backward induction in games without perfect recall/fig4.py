from pathlib import Path
import pygambit as gbt


def build_geb_cannot_always_deviate_fig4() -> gbt.Game:
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Cannot Always Deviate at Multiple Information Sets Fig. 4"
    )

    # Player 1 moves first
    g.append_move(g.root, player="Player 1", actions=["T", "B"])
    node_T = g.root.children["T"]
    node_B = g.root.children["B"]

    # After T, Player 2 moves at the upper-left node
    g.append_move(node_T, player="Player 2", actions=["U", "D"])

    # After B, Player 2 moves at the lower node
    g.append_move(node_B, player="Player 2", actions=["L", "R"])
    node_BL = node_B.children["L"]
    node_BR = node_B.children["R"]

    # If Player 2 chose R after B, game ends immediately
    out_BR = g.add_outcome([1, 1], label="B_R")
    g.set_outcome(node_BR, out_BR)

    # If Player 2 chose L after B, Player 2 moves again at the upper-right node
    # This upper-right node is in the same infoset as the upper-left node after T
    g.append_infoset(node_BL, node_T.infoset)

    # Terminal outcomes after the upper-left node (reached after T)
    out_TU = g.add_outcome([2, 2], label="T_U")
    out_TD = g.add_outcome([0, 0], label="T_D")
    g.set_outcome(node_T.children["U"], out_TU)
    g.set_outcome(node_T.children["D"], out_TD)

    # Terminal outcomes after the upper-right node (reached after B then L)
    out_BLU = g.add_outcome([0, 0], label="B_L_U")
    out_BLD = g.add_outcome([3, 3], label="B_L_D")
    g.set_outcome(node_BL.children["U"], out_BLU)
    g.set_outcome(node_BL.children["D"], out_BLD)

    return g


if __name__ == "__main__":
    g = build_geb_cannot_always_deviate_fig4()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
