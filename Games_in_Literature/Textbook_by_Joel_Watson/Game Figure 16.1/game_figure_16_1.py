from pathlib import Path
import pygambit as gbt


def build_figure_16_1() -> gbt.Game:
    """Construct Watson Figure 16.1: abbreviated entry game."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 16.1 - Abbreviated Entry Game"
    )

    # Player 1 first chooses N, S, or L.
    g.append_move(g.root, player="1", actions=["N", "S", "L"])

    node_N = g.root.children["N"]
    node_S = g.root.children["S"]
    node_L = g.root.children["L"]

    # After each of Player 1's choices, Player 2 chooses N / S / L.
    g.append_move(node_N, player="2", actions=["N", "S", "L"])
    g.append_move(node_S, player="2", actions=["N'", "S'", "L'"])
    g.append_move(node_L, player="2", actions=['N"', 'S"', 'L"'])

    node_NN = node_N.children["N"]
    node_NS = node_N.children["S"]
    node_NL = node_N.children["L"]

    node_SN = node_S.children["N'"]
    node_SS = node_S.children["S'"]
    node_SL = node_S.children["L'"]

    node_LN = node_L.children['N"']
    node_LS = node_L.children['S"']
    node_LL = node_L.children['L"']

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_NN = g.add_outcome([0, 0], label="NN")
    outcome_NS = g.add_outcome([0, 30], label="NS")
    outcome_NL = g.add_outcome([0, 27.5], label="NL")

    outcome_SN = g.add_outcome([30, 0], label="SN")
    outcome_SS = g.add_outcome([20, 20], label="SS")
    outcome_SL = g.add_outcome([-10, -15], label="SL")

    outcome_LN = g.add_outcome([27.5, 0], label="LN")
    outcome_LS = g.add_outcome([-15, -10], label="LS")
    outcome_LL = g.add_outcome([-85, -85], label="LL")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_NN, outcome_NN)
    g.set_outcome(node_NS, outcome_NS)
    g.set_outcome(node_NL, outcome_NL)

    g.set_outcome(node_SN, outcome_SN)
    g.set_outcome(node_SS, outcome_SS)
    g.set_outcome(node_SL, outcome_SL)

    g.set_outcome(node_LN, outcome_LN)
    g.set_outcome(node_LS, outcome_LS)
    g.set_outcome(node_LL, outcome_LL)

    return g


if __name__ == "__main__":
    g = build_figure_16_1()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("figure_16_1.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")