from pathlib import Path
import pygambit as gbt


def build_uncertainty_averse_fig3_v0():
    g = gbt.Game.new_tree(
        players=["1", "2", "3"],
        title="Uncertainty-Averse Coordination Example V0"
    )

    # Player 1 moves first
    g.append_move(g.root, "1", actions=["C", "D"])
    root_C = g.root.children["C"]
    root_D = g.root.children["D"]

    # Player 2 moves after C
    g.append_move(root_C, "2", actions=["c", "d"])
    p2_after_C = root_C

    # Player 3 moves after D
    g.append_move(root_D, "3", actions=["L", "R"])
    p3_after_D = root_D

    # Player 3 also moves after C then d, in the same information set
    g.append_infoset(p2_after_C.children["d"], p3_after_D.infoset)
    p3_after_Cd = p2_after_C.children["d"]

    # Distinct outcomes
    out_C_c = g.add_outcome([1, 1, 1], label="C_then_c")
    out_D_L = g.add_outcome([3, 0, 0], label="D_then_L")
    out_D_R = g.add_outcome([0, 3, 0], label="D_then_R")
    out_Cd_L = g.add_outcome([3, 0, 0], label="C_then_d_then_L")
    out_Cd_R = g.add_outcome([0, 3, 0], label="C_then_d_then_R")

    # Assign outcomes
    g.set_outcome(p2_after_C.children["c"], out_C_c)

    g.set_outcome(p3_after_D.children["L"], out_D_L)
    g.set_outcome(p3_after_D.children["R"], out_D_R)

    g.set_outcome(p3_after_Cd.children["L"], out_Cd_L)
    g.set_outcome(p3_after_Cd.children["R"], out_Cd_R)

    return g


if __name__ == "__main__":
    game = build_uncertainty_averse_fig3_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
    