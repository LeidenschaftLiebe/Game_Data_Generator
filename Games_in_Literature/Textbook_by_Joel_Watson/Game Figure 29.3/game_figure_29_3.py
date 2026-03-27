from pathlib import Path
import pygambit as gbt


def build_figure_29_3() -> gbt.Game:
    """Construct Watson Figure 29.3: investment game with incomplete information."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 29.3 - Investment Game with Incomplete Information"
    )

    # Chance selects Player 1's type.
    g.append_move(g.root, g.players.chance, actions=["Ordinary", "Cooperative"])
    g.set_chance_probs(
        g.root.infoset,
        [gbt.Rational("3/4"), gbt.Rational("1/4")]
    )

    node_O = g.root.children["Ordinary"]
    node_C = g.root.children["Cooperative"]

    # Player 1 observes type and decides whether to invest.
    g.append_move(node_O, player="1", actions=["N", "I"])
    g.append_move(node_C, player="1", actions=["N_prime", "I_prime"])

    node_ON = node_O.children["N"]
    node_OI = node_O.children["I"]
    node_CN = node_C.children["N_prime"]
    node_CI = node_C.children["I_prime"]

    # If Player 1 does not invest, game ends immediately.
    out_ON = g.add_outcome([0, 0], label="Ordinary_NoInvest")
    out_CN = g.add_outcome([0, 0], label="Cooperative_NoInvest")

    g.set_outcome(node_ON, out_ON)
    g.set_outcome(node_CN, out_CN)

    # Player 2 moves after investment, without observing Player 1's type.
    g.append_move(node_OI, player="2", actions=["N", "I"])
    g.append_infoset(node_CI, node_OI.infoset)

    node_OIN = node_OI.children["N"]
    node_OII = node_OI.children["I"]
    node_CIN = node_CI.children["N"]
    node_CII = node_CI.children["I"]

    # If Player 2 does not invest.
    out_OIN = g.add_outcome([-2, 0], label="Ordinary_Invest_P2_NoInvest")
    out_CIN = g.add_outcome([1, 0], label="Cooperative_Invest_P2_NoInvest")

    g.set_outcome(node_OIN, out_OIN)
    g.set_outcome(node_CIN, out_CIN)

    # If both invest, Player 1 chooses selfish or benevolent.
    g.append_move(node_OII, player="1", actions=["S", "B"])
    g.append_move(node_CII, player="1", actions=["S_prime", "B_prime"])

    node_OIIS = node_OII.children["S"]
    node_OIIB = node_OII.children["B"]
    node_CIIS = node_CII.children["S_prime"]
    node_CIIB = node_CII.children["B_prime"]

    out_OIIS = g.add_outcome([6, -2], label="Ordinary_BothInvest_Selfish")
    out_OIIB = g.add_outcome([2, 2], label="Ordinary_BothInvest_Benevolent")

    out_CIIS = g.add_outcome([1, -2], label="Cooperative_BothInvest_Selfish")
    out_CIIB = g.add_outcome([2, 2], label="Cooperative_BothInvest_Benevolent")

    g.set_outcome(node_OIIS, out_OIIS)
    g.set_outcome(node_OIIB, out_OIIB)

    g.set_outcome(node_CIIS, out_CIIS)
    g.set_outcome(node_CIIB, out_CIIB)

    return g


if __name__ == "__main__":
    g = build_figure_29_3()

    out_path = Path(__file__).with_name("game_figure_29_3.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")