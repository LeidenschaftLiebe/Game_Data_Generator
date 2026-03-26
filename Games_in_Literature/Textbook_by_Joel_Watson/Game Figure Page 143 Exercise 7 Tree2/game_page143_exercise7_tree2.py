from pathlib import Path
import pygambit as gbt


def build_exercise_7_tree2() -> gbt.Game:
    """Construct Page 143, Exercise 7, Tree 2."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Exercise 7 Tree 2"
    )

    # Player 1 first chooses I or O.
    g.append_move(g.root, player="1", actions=["I", "O"])

    node_I = g.root.children["I"]
    node_O = g.root.children["O"]

    # If Player 1 chooses O, the game ends immediately.
    outcome_O = g.add_outcome([1, 1], label="O")
    g.set_outcome(node_O, outcome_O)

    # If Player 1 chooses I, Player 2 chooses I or O.
    g.append_move(node_I, player="2", actions=["I", "O"])

    node_II = node_I.children["I"]
    node_IO = node_I.children["O"]

    # If Player 2 chooses O, the game ends.
    outcome_IO = g.add_outcome([-1, 0], label="IO")
    g.set_outcome(node_IO, outcome_IO)

    # If Player 2 also chooses I, Player 1 chooses U or D.
    g.append_move(node_II, player="1", actions=["U", "D"])

    node_IIU = node_II.children["U"]
    node_IID = node_II.children["D"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_IIU = g.add_outcome([4, -1], label="IIU")
    outcome_IID = g.add_outcome([3, 2], label="IID")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_IIU, outcome_IIU)
    g.set_outcome(node_IID, outcome_IID)

    return g


if __name__ == "__main__":
    g = build_exercise_7_tree2()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_7_tree2.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")

    