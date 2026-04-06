from pathlib import Path
import pygambit as gbt


def build_geb_sequential_prisoners_dilemma_fig2() -> gbt.Game:
    """Construct Fig. 2 Sequential Prisoners' Dilemma."""
    g = gbt.Game.new_tree(
        players=["P1", "P2"],
        title="GEB Sequential Prisoners' Dilemma Fig. 2"
    )

    # Player 1 moves first.
    g.append_move(g.root, player="P1", actions=["C", "D"])

    node_C = g.root.children["C"]
    node_D = g.root.children["D"]

    # Player 2 observes Player 1's action and then responds.
    g.append_move(node_C, player="P2", actions=["c", "d"])
    g.append_move(node_D, player="P2", actions=["c", "d"])

    node_Cc = node_C.children["c"]
    node_Cd = node_C.children["d"]
    node_Dc = node_D.children["c"]
    node_Dd = node_D.children["d"]

    # Terminal outcomes.
    out_Cc = g.add_outcome([2, 2], label="C_c")
    out_Cd = g.add_outcome([0, 3], label="C_d")
    out_Dc = g.add_outcome([3, 0], label="D_c")
    out_Dd = g.add_outcome([1, 1], label="D_d")

    g.set_outcome(node_Cc, out_Cc)
    g.set_outcome(node_Cd, out_Cd)
    g.set_outcome(node_Dc, out_Dc)
    g.set_outcome(node_Dd, out_Dd)

    return g


if __name__ == "__main__":
    g = build_geb_sequential_prisoners_dilemma_fig2()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")



