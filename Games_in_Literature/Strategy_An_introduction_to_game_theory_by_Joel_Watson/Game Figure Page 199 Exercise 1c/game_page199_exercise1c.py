from pathlib import Path
import pygambit as gbt


def build_exercise_1_c() -> gbt.Game:
    """Construct Page 199, Exercise 1(c)."""
    g = gbt.Game.new_tree(
        players=["1", "2", "3"],
        title="Page 199 Exercise 1(c)"
    )

    # Player 1 first chooses O or I.
    g.append_move(g.root, player="1", actions=["O", "I"])

    node_O = g.root.children["O"]
    node_I = g.root.children["I"]

    # If Player 1 chooses O, the game ends immediately.
    outcome_O = g.add_outcome([2, 2, 2], label="O")
    g.set_outcome(node_O, outcome_O)

    # If Player 1 chooses I, Player 2 chooses A, B, or C.
    g.append_move(node_I, player="2", actions=["A", "B", "C"])

    node_IA = node_I.children["A"]
    node_IB = node_I.children["B"]
    node_IC = node_I.children["C"]

    # If Player 2 chooses C, the game ends immediately.
    outcome_IC = g.add_outcome([4, 3, 1], label="IC")
    g.set_outcome(node_IC, outcome_IC)

    # After A or B, Player 3 chooses X or Y without knowing whether A or B was chosen.
    g.append_move([node_IA, node_IB], player="3", actions=["X", "Y"])

    node_IAX = node_IA.children["X"]
    node_IAY = node_IA.children["Y"]
    node_IBX = node_IB.children["X"]
    node_IBY = node_IB.children["Y"]

    # Terminal rewards in the order (Player 1, Player 2, Player 3).
    outcome_IAX = g.add_outcome([3, 2, 1], label="IAX")
    outcome_IAY = g.add_outcome([5, 0, 0], label="IAY")
    outcome_IBX = g.add_outcome([1, 2, 6], label="IBX")
    outcome_IBY = g.add_outcome([7, 5, 5], label="IBY")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_IAX, outcome_IAX)
    g.set_outcome(node_IAY, outcome_IAY)
    g.set_outcome(node_IBX, outcome_IBX)
    g.set_outcome(node_IBY, outcome_IBY)

    return g


if __name__ == "__main__":
    g = build_exercise_1_c()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_1_c.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    