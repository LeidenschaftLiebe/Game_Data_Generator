from pathlib import Path
import pygambit as gbt


def build_exercise_2_b() -> gbt.Game:
    """Construct Page 200, Exercise 2(b)."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Page 200 Exercise 2(b)"
    )

    # Player 1 first chooses U or D.
    g.append_move(g.root, player="1", actions=["U", "D"])

    node_U = g.root.children["U"]
    node_D = g.root.children["D"]

    # After U, Player 2 chooses A or B.
    g.append_move(node_U, player="2", actions=["A", "B"])
    node_UA = node_U.children["A"]
    node_UB = node_U.children["B"]

    # After D, Player 2 chooses C or D.
    g.append_move(node_D, player="2", actions=["C", "D"])
    node_DC = node_D.children["C"]
    node_DD = node_D.children["D"]

    # After D then C, Player 1 chooses E or F.
    g.append_move(node_DC, player="1", actions=["E", "F"])
    node_DCE = node_DC.children["E"]
    node_DCF = node_DC.children["F"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_UA = g.add_outcome([2, 3], label="UA")
    outcome_UB = g.add_outcome([5, 4], label="UB")
    outcome_DD = g.add_outcome([0, 2], label="DD")
    outcome_DCE = g.add_outcome([6, 2], label="DCE")
    outcome_DCF = g.add_outcome([2, 6], label="DCF")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_UA, outcome_UA)
    g.set_outcome(node_UB, outcome_UB)
    g.set_outcome(node_DD, outcome_DD)
    g.set_outcome(node_DCE, outcome_DCE)
    g.set_outcome(node_DCF, outcome_DCF)

    return g


if __name__ == "__main__":
    g = build_exercise_2_b()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_2_b.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    