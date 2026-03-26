from pathlib import Path
import pygambit as gbt


def build_exercise_3_a() -> gbt.Game:
    """Construct Exercise 3(a)."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Exercise 3(a)"
    )

    # Player 1 chooses A or B.
    g.append_move(g.root, player="1", actions=["A", "B"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]

    # After A, Player 2 chooses C or D.
    g.append_move(node_A, player="2", actions=["C", "D"])

    node_AC = node_A.children["C"]
    node_AD = node_A.children["D"]

    # After B, Player 2 chooses E or F.
    g.append_move(node_B, player="2", actions=["E", "F"])

    node_BE = node_B.children["E"]
    node_BF = node_B.children["F"]

    # Terminal results in the order (Player 1, Player 2).
    outcome_AC = g.add_outcome([0, 0], label="AC")
    outcome_AD = g.add_outcome([1, 1], label="AD")
    outcome_BE = g.add_outcome([2, 2], label="BE")
    outcome_BF = g.add_outcome([3, 4], label="BF")

    # Attach results to terminal nodes.
    g.set_outcome(node_AC, outcome_AC)
    g.set_outcome(node_AD, outcome_AD)
    g.set_outcome(node_BE, outcome_BE)
    g.set_outcome(node_BF, outcome_BF)

    return g


if __name__ == "__main__":
    g = build_exercise_3_a()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_3_a.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    