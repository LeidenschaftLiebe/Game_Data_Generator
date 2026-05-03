from pathlib import Path
import pygambit as gbt


def build_guided_exercise_p180() -> gbt.Game:
    """Construct the page 180 guided exercise tree."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Page 180 Guided Exercise"
    )

    # Player 1 first chooses A or B.
    g.append_move(g.root, player="1", actions=["A", "B"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]

    # After A, Player 2 chooses a or b.
    g.append_move(node_A, player="2", actions=["a", "b"])

    node_Aa = node_A.children["a"]
    node_Ab = node_A.children["b"]

    # After B, Player 2 chooses c or d.
    g.append_move(node_B, player="2", actions=["c", "d"])

    node_Bc = node_B.children["c"]
    node_Bd = node_B.children["d"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_Aa = g.add_outcome([3, 3], label="Aa")
    outcome_Ab = g.add_outcome([3, 3], label="Ab")
    outcome_Bc = g.add_outcome([0, 4], label="Bc")
    outcome_Bd = g.add_outcome([0, 3.5], label="Bd")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_Aa, outcome_Aa)
    g.set_outcome(node_Ab, outcome_Ab)
    g.set_outcome(node_Bc, outcome_Bc)
    g.set_outcome(node_Bd, outcome_Bd)

    return g


if __name__ == "__main__":
    g = build_guided_exercise_p180()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("guided_exercise_p180.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")