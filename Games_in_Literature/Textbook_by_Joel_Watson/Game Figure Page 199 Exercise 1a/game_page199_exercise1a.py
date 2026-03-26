from pathlib import Path
import pygambit as gbt


def build_exercise_1_a() -> gbt.Game:
    """Construct Page 199, Exercise 1(a)."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Page 199 Exercise 1(a)"
    )

    # Player 1 first chooses A or B.
    g.append_move(g.root, player="1", actions=["A", "B"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]

    # If Player 1 chooses A, the game ends immediately.
    outcome_A = g.add_outcome([2, 6], label="A")
    g.set_outcome(node_A, outcome_A)

    # If Player 1 chooses B, Player 2 chooses C or D.
    g.append_move(node_B, player="2", actions=["C", "D"])

    node_BC = node_B.children["C"]
    node_BD = node_B.children["D"]

    # If Player 2 chooses C, the game ends.
    outcome_BC = g.add_outcome([1, 4], label="BC")
    g.set_outcome(node_BC, outcome_BC)

    # If Player 2 chooses D, Player 1 chooses E or F.
    g.append_move(node_BD, player="1", actions=["E", "F"])

    node_BDE = node_BD.children["E"]
    node_BDF = node_BD.children["F"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_BDE = g.add_outcome([1, 5], label="BDE")
    outcome_BDF = g.add_outcome([2, 3], label="BDF")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_BDE, outcome_BDE)
    g.set_outcome(node_BDF, outcome_BDF)

    return g


if __name__ == "__main__":
    g = build_exercise_1_a()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_1_a.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")