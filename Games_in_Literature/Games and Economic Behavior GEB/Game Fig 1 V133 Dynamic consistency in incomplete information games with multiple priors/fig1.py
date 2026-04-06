from pathlib import Path
import pygambit as gbt


def build_geb_aryal_stauber_fig1() -> gbt.Game:
    """Construct the 2-player adapted Aryal-Stauber example."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Aryal-Stauber Inspired Fig. 1"
    )

    # Fixed parameter values for this dataset instance.
    epsilon = gbt.Rational("1/10")
    prob_L = epsilon / 3          # 1/30
    prob_R = 1 - 2 * epsilon / 3  # 14/15
    prob_O = epsilon / 3          # 1/30

    x = 0
    y = 0

    # Nature chooses the state.
    g.append_move(g.root, g.players.chance, actions=["L", "R", "O"])
    g.set_chance_probs(
        g.root.infoset,
        [prob_L, prob_R, prob_O]
    )

    node_L = g.root.children["L"]
    node_R = g.root.children["R"]
    node_O = g.root.children["O"]

    # Player 1 observes only whether the state is O or not.
    # So the L and R nodes are in the same infoset.
    g.append_move(node_L, player="Player 1", actions=["M", "N"])
    g.append_infoset(node_R, node_L.infoset)

    node_LM = node_L.children["M"]
    node_LN = node_L.children["N"]
    node_RM = node_R.children["M"]
    node_RN = node_R.children["N"]

    # Outcomes after L and after R-M.
    out_LM = g.add_outcome([0, y], label="L_M")
    out_LN = g.add_outcome([101, y], label="L_N")
    out_RM = g.add_outcome([101, y], label="R_M")

    g.set_outcome(node_LM, out_LM)
    g.set_outcome(node_LN, out_LN)
    g.set_outcome(node_RM, out_RM)

    # Player 2 moves after R-N or O, without knowing which one occurred.
    g.append_move(node_RN, player="Player 2", actions=["S", "T"])
    g.append_infoset(node_O, node_RN.infoset)

    node_RNS = node_RN.children["S"]
    node_RNT = node_RN.children["T"]
    node_OS = node_O.children["S"]
    node_OT = node_O.children["T"]

    out_RNS = g.add_outcome([100, x], label="R_N_S")
    out_RNT = g.add_outcome([100, x], label="R_N_T")
    out_OS = g.add_outcome([-1, x], label="O_S")
    out_OT = g.add_outcome([-1, x], label="O_T")

    g.set_outcome(node_RNS, out_RNS)
    g.set_outcome(node_RNT, out_RNT)
    g.set_outcome(node_OS, out_OS)
    g.set_outcome(node_OT, out_OT)

    return g


if __name__ == "__main__":
    g = build_geb_aryal_stauber_fig1()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")

