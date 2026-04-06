from pathlib import Path
import pygambit as gbt


def build_geb_gradual_game_fig1() -> gbt.Game:
    """Construct Fig. 1 baseline gradual game."""
    g = gbt.Game.new_tree(
        players=["Sender", "Receiver"],
        title="GEB Gradual Game Fig. 1"
    )

    # Sender chooses a trust level.
    g.append_move(g.root, player="Sender", actions=["N", "L", "M", "H"])

    node_N = g.root.children["N"]
    node_L = g.root.children["L"]
    node_M = g.root.children["M"]
    node_H = g.root.children["H"]

    # No trust ends the interaction immediately.
    out_N = g.add_outcome([24, 15], label="N")
    g.set_outcome(node_N, out_N)

    # Receiver responds after low trust.
    g.append_move(node_L, player="Receiver", actions=["R", "D"])
    out_LR = g.add_outcome([32, 22], label="L_R")
    out_LD = g.add_outcome([20, 42], label="L_D")
    g.set_outcome(node_L.children["R"], out_LR)
    g.set_outcome(node_L.children["D"], out_LD)

    # Receiver responds after medium trust.
    g.append_move(node_M, player="Receiver", actions=["R", "D"])
    out_MR = g.add_outcome([44, 36], label="M_R")
    out_MD = g.add_outcome([12, 72], label="M_D")
    g.set_outcome(node_M.children["R"], out_MR)
    g.set_outcome(node_M.children["D"], out_MD)

    # Receiver responds after high trust.
    g.append_move(node_H, player="Receiver", actions=["R", "D"])
    out_HR = g.add_outcome([56, 42], label="H_R")
    out_HD = g.add_outcome([0, 80], label="H_D")
    g.set_outcome(node_H.children["R"], out_HR)
    g.set_outcome(node_H.children["D"], out_HD)

    return g


if __name__ == "__main__":
    g = build_geb_gradual_game_fig1()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")

