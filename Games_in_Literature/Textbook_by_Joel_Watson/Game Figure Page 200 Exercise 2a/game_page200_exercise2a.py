from pathlib import Path
import pygambit as gbt


def build_exercise_2_a() -> gbt.Game:
    """Construct Page 200, Exercise 2(a)."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Page 200 Exercise 2(a)"
    )

    # Player 1 first chooses W or Z.
    g.append_move(g.root, player="1", actions=["W", "Z"])

    node_W = g.root.children["W"]
    node_Z = g.root.children["Z"]

    # After W, Player 2 chooses A or B.
    g.append_move(node_W, player="2", actions=["A", "B"])
    node_WA = node_W.children["A"]
    node_WB = node_W.children["B"]

    # After Z, Player 2 chooses C or D.
    g.append_move(node_Z, player="2", actions=["C", "D"])
    node_ZC = node_Z.children["C"]
    node_ZD = node_Z.children["D"]

    # After W then A or W then B, Player 1 chooses X or Y at the same information set.
    g.append_move([node_WA, node_WB], player="1", actions=["X", "Y"])
    node_WAX = node_WA.children["X"]
    node_WAY = node_WA.children["Y"]
    node_WBX = node_WB.children["X"]
    node_WBY = node_WB.children["Y"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_WAX = g.add_outcome([3, 0], label="WAX")
    outcome_WAY = g.add_outcome([8, 5], label="WAY")
    outcome_WBX = g.add_outcome([4, 6], label="WBX")
    outcome_WBY = g.add_outcome([2, 1], label="WBY")
    outcome_ZC = g.add_outcome([6, 4], label="ZC")
    outcome_ZD = g.add_outcome([3, 2], label="ZD")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_WAX, outcome_WAX)
    g.set_outcome(node_WAY, outcome_WAY)
    g.set_outcome(node_WBX, outcome_WBX)
    g.set_outcome(node_WBY, outcome_WBY)
    g.set_outcome(node_ZC, outcome_ZC)
    g.set_outcome(node_ZD, outcome_ZD)

    return g


if __name__ == "__main__":
    g = build_exercise_2_a()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_2_a.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    