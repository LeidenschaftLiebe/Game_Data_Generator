from pathlib import Path
import pygambit as gbt


def build_figure_15_5() -> gbt.Game:
    """Construct Watson Figure 15.5: iterated conditional dominance."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 15.5 - Iterated Conditional Dominance"
    )

    # Player 1 first chooses W or Z.
    g.append_move(g.root, player="1", actions=["W", "Z"])

    node_W = g.root.children["W"]
    node_Z = g.root.children["Z"]

    # If Player 1 chooses Z, the game ends immediately.
    outcome_Z = g.add_outcome([4, 4], label="Z")
    g.set_outcome(node_Z, outcome_Z)

    # After W, Player 2 chooses A or B.
    g.append_move(node_W, player="2", actions=["A", "B"])

    node_WA = node_W.children["A"]
    node_WB = node_W.children["B"]

    # After A or B, Player 1 chooses X or Y without knowing whether A or B was chosen.
    g.append_move([node_WA, node_WB], player="1", actions=["X", "Y"])

    node_WAX = node_WA.children["X"]
    node_WAY = node_WA.children["Y"]
    node_WBX = node_WB.children["X"]
    node_WBY = node_WB.children["Y"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_WAX = g.add_outcome([3, 3], label="WAX")
    outcome_WAY = g.add_outcome([0, 0], label="WAY")
    outcome_WBX = g.add_outcome([0, 0], label="WBX")
    outcome_WBY = g.add_outcome([6, 2], label="WBY")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_WAX, outcome_WAX)
    g.set_outcome(node_WAY, outcome_WAY)
    g.set_outcome(node_WBX, outcome_WBX)
    g.set_outcome(node_WBY, outcome_WBY)

    return g


if __name__ == "__main__":
    g = build_figure_15_5()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("figure_15_5.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")