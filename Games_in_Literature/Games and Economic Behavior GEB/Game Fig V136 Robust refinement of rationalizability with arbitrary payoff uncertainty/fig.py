from pathlib import Path
import pygambit as gbt


def build_geb_twins_example(theta: str = "0") -> gbt.Game:
    """Construct the extensive-form example with theta fixed."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Twins Example"
    )

    theta_val = gbt.Rational(theta)

    # Player 1 moves first.
    g.append_move(g.root, player="Player 1", actions=["U", "D"])

    node_U = g.root.children["U"]
    node_D = g.root.children["D"]

    # Player 2 moves next without observing whether Player 1 chose U or D.
    g.append_move(node_U, player="Player 2", actions=["L", "R", "X"])
    g.append_infoset(node_D, node_U.infoset)

    node_UL = node_U.children["L"]
    node_UR = node_U.children["R"]
    node_UX = node_U.children["X"]

    node_DL = node_D.children["L"]
    node_DR = node_D.children["R"]
    node_DX = node_D.children["X"]

    # Outcomes after U.
    out_UL = g.add_outcome([1, 3], label="U_L")
    out_UR = g.add_outcome([0, 2], label="U_R")
    out_UX = g.add_outcome([1, 1], label="U_X")

    g.set_outcome(node_UL, out_UL)
    g.set_outcome(node_UR, out_UR)
    g.set_outcome(node_UX, out_UX)

    # Outcomes after D with L or R.
    out_DL = g.add_outcome([theta_val, 2], label="D_L")
    out_DR = g.add_outcome([1, 3], label="D_R")

    g.set_outcome(node_DL, out_DL)
    g.set_outcome(node_DR, out_DR)

    # After D then X, Player 1 moves again.
    g.append_move(node_DX, player="Player 1", actions=["u", "d"])

    node_DXu = node_DX.children["u"]
    node_DXd = node_DX.children["d"]

    out_DXu = g.add_outcome([2, 1], label="D_X_u")
    out_DXd = g.add_outcome([0, 1], label="D_X_d")

    g.set_outcome(node_DXu, out_DXu)
    g.set_outcome(node_DXd, out_DXd)

    return g


if __name__ == "__main__":
    # The article's discussion focuses on the complete-information type with theta = 0.
    g = build_geb_twins_example(theta="0")

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
