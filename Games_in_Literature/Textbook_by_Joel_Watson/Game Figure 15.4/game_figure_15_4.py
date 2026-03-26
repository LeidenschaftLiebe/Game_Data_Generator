from pathlib import Path
import pygambit as gbt


def build_figure_15_4() -> gbt.Game:
    """Construct Watson Figure 15.4: subgame perfection."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 15.4 - Subgame Perfection"
    )

    # Player 1 first chooses U or D.
    g.append_move(g.root, player="1", actions=["U", "D"])

    node_U = g.root.children["U"]
    node_D = g.root.children["D"]

    # If Player 1 chooses D, the game ends immediately.
    outcome_D = g.add_outcome([2, 6], label="D")
    g.set_outcome(node_D, outcome_D)

    # After U, Player 1 chooses A or B.
    g.append_move(node_U, player="1", actions=["A", "B"])

    node_UA = node_U.children["A"]
    node_UB = node_U.children["B"]

    # After A or B, Player 2 chooses X or Y without knowing whether A or B was chosen.
    g.append_move([node_UA, node_UB], player="2", actions=["X", "Y"])

    node_UAX = node_UA.children["X"]
    node_UAY = node_UA.children["Y"]
    node_UBX = node_UB.children["X"]
    node_UBY = node_UB.children["Y"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_UAX = g.add_outcome([3, 4], label="UAX")
    outcome_UAY = g.add_outcome([1, 4], label="UAY")
    outcome_UBX = g.add_outcome([2, 1], label="UBX")
    outcome_UBY = g.add_outcome([2, 0], label="UBY")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_UAX, outcome_UAX)
    g.set_outcome(node_UAY, outcome_UAY)
    g.set_outcome(node_UBX, outcome_UBX)
    g.set_outcome(node_UBY, outcome_UBY)

    return g


if __name__ == "__main__":
    g = build_figure_15_4()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("figure_15_4.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")