from pathlib import Path
import pygambit as gbt


def build_exercise_6() -> gbt.Game:
    """Construct Page 64, Exercise 6."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Exercise 6"
    )

    # Player 1 first chooses A, B, or C.
    g.append_move(g.root, player="1", actions=["A", "B", "C"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]
    node_C = g.root.children["C"]

    # Player 2 chooses X or Y without knowing whether Player 1 chose A or B.
    g.append_move([node_A, node_B], player="2", actions=["X", "Y"])

    node_AX = node_A.children["X"]
    node_AY = node_A.children["Y"]
    node_BX = node_B.children["X"]
    node_BY = node_B.children["Y"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_C = g.add_outcome([1, 1], label="C")
    outcome_AX = g.add_outcome([3, 0], label="AX")
    outcome_AY = g.add_outcome([0, 3], label="AY")
    outcome_BX = g.add_outcome([0, 3], label="BX")
    outcome_BY = g.add_outcome([3, 0], label="BY")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_C, outcome_C)
    g.set_outcome(node_AX, outcome_AX)
    g.set_outcome(node_AY, outcome_AY)
    g.set_outcome(node_BX, outcome_BX)
    g.set_outcome(node_BY, outcome_BY)

    return g


if __name__ == "__main__":
    g = build_exercise_6()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_6.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    