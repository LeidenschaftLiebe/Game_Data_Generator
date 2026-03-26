from pathlib import Path
import pygambit as gbt


def build_figure_3_5_lower() -> gbt.Game:
    """Construct the lower extensive-form tree in Watson Figure 3.5."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 3.5 Lower Tree"
    )

    # Player 1 chooses A or B.
    g.append_move(g.root, player="1", actions=["A", "B"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]

    # Player 2 chooses C or D without knowing whether Player 1 chose A or B.
    g.append_move([node_A, node_B], player="2", actions=["C", "D"])

    # Terminal nodes after A.
    node_AC = node_A.children["C"]
    node_AD = node_A.children["D"]

    # Terminal nodes after B.
    node_BC = node_B.children["C"]
    node_BD = node_B.children["D"]

    # Final rewards in the order (Player 1, Player 2).
    outcome_AC = g.add_outcome([1, 2], label="AC")
    outcome_AD = g.add_outcome([1, 2], label="AD")
    outcome_BC = g.add_outcome([3, 1], label="BC")
    outcome_BD = g.add_outcome([2, 4], label="BD")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_AC, outcome_AC)
    g.set_outcome(node_AD, outcome_AD)
    g.set_outcome(node_BC, outcome_BC)
    g.set_outcome(node_BD, outcome_BD)

    return g


if __name__ == "__main__":
    g = build_figure_3_5_lower()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("figure_3_5_lower.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    