from pathlib import Path
import pygambit as gbt


def build_exercise_3_d() -> gbt.Game:
    """Construct Exercise 3(d)."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Exercise 3(d)"
    )

    # Player 1 first chooses U or D.
    g.append_move(g.root, player="1", actions=["U", "D"])

    node_U = g.root.children["U"]
    node_D = g.root.children["D"]

    # Player 2 chooses A or B without knowing whether Player 1 chose U or D.
    g.append_move([node_U, node_D], player="2", actions=["A", "B"])

    node_UA = node_U.children["A"]
    node_UB = node_U.children["B"]
    node_DA = node_D.children["A"]
    node_DB = node_D.children["B"]

    # After U then B, Player 1 chooses X or Y.
    g.append_move(node_UB, player="1", actions=["X", "Y"])
    node_UBX = node_UB.children["X"]
    node_UBY = node_UB.children["Y"]

    # After D then A, Player 1 chooses W or Z.
    g.append_move(node_DA, player="1", actions=["W", "Z"])
    node_DAW = node_DA.children["W"]
    node_DAZ = node_DA.children["Z"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_UA = g.add_outcome([3, 3], label="UA")
    outcome_DB = g.add_outcome([2, 2], label="DB")
    outcome_UBX = g.add_outcome([5, 1], label="UBX")
    outcome_UBY = g.add_outcome([3, 6], label="UBY")
    outcome_DAW = g.add_outcome([4, 2], label="DAW")
    outcome_DAZ = g.add_outcome([9, 0], label="DAZ")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_UA, outcome_UA)
    g.set_outcome(node_DB, outcome_DB)
    g.set_outcome(node_UBX, outcome_UBX)
    g.set_outcome(node_UBY, outcome_UBY)
    g.set_outcome(node_DAW, outcome_DAW)
    g.set_outcome(node_DAZ, outcome_DAZ)

    return g


if __name__ == "__main__":
    g = build_exercise_3_d()

    out_path = Path(__file__).with_name("exercise_3_d.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")