from pathlib import Path
import pygambit as gbt


def build_figure_3_5_top() -> gbt.Game:
    """Construct the top extensive-form tree in Watson Figure 3.5."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 3.5 Top Tree"
    )

    # Player 1 chooses A or B.
    g.append_move(g.root, player="1", actions=["A", "B"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]

    # If Player 1 chooses B, Player 2 chooses C or D.
    g.append_move(node_B, player="2", actions=["C", "D"])

    node_BC = node_B.children["C"]
    node_BD = node_B.children["D"]

    # Terminal results in the order (Player 1, Player 2).
    outcome_A = g.add_outcome([1, 2], label="A")
    outcome_BC = g.add_outcome([3, 1], label="BC")
    outcome_BD = g.add_outcome([2, 4], label="BD")

    # Attach terminal results.
    g.set_outcome(node_A, outcome_A)
    g.set_outcome(node_BC, outcome_BC)
    g.set_outcome(node_BD, outcome_BD)

    return g


if __name__ == "__main__":
    g = build_figure_3_5_top()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("figure_3_5_top.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    