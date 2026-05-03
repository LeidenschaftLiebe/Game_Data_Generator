from pathlib import Path
import pygambit as gbt


def build_exercise_3_f() -> gbt.Game:
    """Construct Exercise 3(f)."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Exercise 3(f)"
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

    # After U then A or U then B, Player 1 chooses X or Y at the same information set.
    g.append_move([node_UA, node_UB], player="1", actions=["X", "Y"])

    node_UAX = node_UA.children["X"]
    node_UAY = node_UA.children["Y"]
    node_UBX = node_UB.children["X"]
    node_UBY = node_UB.children["Y"]

    # After D then B, Player 1 chooses P or Q.
    g.append_move(node_DB, player="1", actions=["P", "Q"])

    node_DBP = node_DB.children["P"]
    node_DBQ = node_DB.children["Q"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_DA = g.add_outcome([6, 6], label="DA")
    outcome_UAX = g.add_outcome([3, 8], label="UAX")
    outcome_UAY = g.add_outcome([8, 1], label="UAY")
    outcome_UBX = g.add_outcome([1, 2], label="UBX")
    outcome_UBY = g.add_outcome([2, 1], label="UBY")
    outcome_DBP = g.add_outcome([5, 5], label="DBP")
    outcome_DBQ = g.add_outcome([0, 0], label="DBQ")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_DA, outcome_DA)
    g.set_outcome(node_UAX, outcome_UAX)
    g.set_outcome(node_UAY, outcome_UAY)
    g.set_outcome(node_UBX, outcome_UBX)
    g.set_outcome(node_UBY, outcome_UBY)
    g.set_outcome(node_DBP, outcome_DBP)
    g.set_outcome(node_DBQ, outcome_DBQ)

    return g


if __name__ == "__main__":
    g = build_exercise_3_f()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_3_f.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")


    