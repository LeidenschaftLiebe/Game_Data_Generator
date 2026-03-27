from pathlib import Path
import pygambit as gbt


def build_figure_29_2() -> gbt.Game:
    """Construct Watson Figure 29.2: an investment game."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 29.2 - Investment Game"
    )

    # Player 1 first chooses whether to invest.
    g.append_move(g.root, player="1", actions=["N", "I"])

    node_N1 = g.root.children["N"]
    node_I1 = g.root.children["I"]

    # If Player 1 does not invest, the game ends immediately.
    out_N1 = g.add_outcome([0, 0], label="P1_NoInvest")
    g.set_outcome(node_N1, out_N1)

    # If Player 1 invests, Player 2 chooses whether to invest.
    g.append_move(node_I1, player="2", actions=["N", "I"])

    node_N2 = node_I1.children["N"]
    node_I2 = node_I1.children["I"]

    # If Player 2 does not invest, Player 1's investment is wasted.
    out_N2 = g.add_outcome([-2, 0], label="P1_Invest_P2_NoInvest")
    g.set_outcome(node_N2, out_N2)

    # If both invest, Player 1 chooses selfish or benevolent use.
    g.append_move(node_I2, player="1", actions=["S", "B"])

    node_S = node_I2.children["S"]
    node_B = node_I2.children["B"]

    out_S = g.add_outcome([6, -2], label="BothInvest_Selfish")
    out_B = g.add_outcome([2, 2], label="BothInvest_Benevolent")

    g.set_outcome(node_S, out_S)
    g.set_outcome(node_B, out_B)

    return g


if __name__ == "__main__":
    g = build_figure_29_2()

    out_path = Path(__file__).with_name("game_figure_29_2.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")