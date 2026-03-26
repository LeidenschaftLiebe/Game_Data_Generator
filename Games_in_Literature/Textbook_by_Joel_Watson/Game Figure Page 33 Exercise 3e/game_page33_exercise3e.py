from pathlib import Path
import pygambit as gbt


def build_exercise_3_e() -> gbt.Game:
    """Construct Exercise 3(e)."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Exercise 3(e)"
    )

    # Player 1 first chooses A, B, or C.
    g.append_move(g.root, player="1", actions=["A", "B", "C"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]
    node_C = g.root.children["C"]

    # Player 2 chooses U or D without knowing whether Player 1 chose A, B, or C.
    g.append_move([node_A, node_B, node_C], player="2", actions=["U", "D"])

    node_AU = node_A.children["U"]
    node_AD = node_A.children["D"]
    node_BU = node_B.children["U"]
    node_BD = node_B.children["D"]
    node_CU = node_C.children["U"]
    node_CD = node_C.children["D"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_AU = g.add_outcome([2, 1], label="AU")
    outcome_AD = g.add_outcome([1, 2], label="AD")
    outcome_BU = g.add_outcome([6, 8], label="BU")
    outcome_BD = g.add_outcome([4, 3], label="BD")
    outcome_CU = g.add_outcome([2, 1], label="CU")
    outcome_CD = g.add_outcome([8, 7], label="CD")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_AU, outcome_AU)
    g.set_outcome(node_AD, outcome_AD)
    g.set_outcome(node_BU, outcome_BU)
    g.set_outcome(node_BD, outcome_BD)
    g.set_outcome(node_CU, outcome_CU)
    g.set_outcome(node_CD, outcome_CD)

    return g


if __name__ == "__main__":
    g = build_exercise_3_e()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_3_e.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    