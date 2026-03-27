from pathlib import Path
import pygambit as gbt


def build_page_454_exercise_5a() -> gbt.Game:
    """Construct Page 454 Exercise 5(a): five-move envelope game."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Page 454 Exercise 5(a)"
    )

    # Move 1: Player 1 chooses Stop or Continue.
    g.append_move(g.root, player="1", actions=["S", "C"])
    n1_stop = g.root.children["S"]
    n1_cont = g.root.children["C"]

    # If Player 1 continues, move 2: Player 2 chooses Stop or Continue.
    g.append_move(n1_cont, player="2", actions=["S", "C"])
    n2_stop = n1_cont.children["S"]
    n2_cont = n1_cont.children["C"]

    # If Player 2 continues, move 3: Player 1 chooses Stop or Continue.
    g.append_move(n2_cont, player="1", actions=["S", "C"])
    n3_stop = n2_cont.children["S"]
    n3_cont = n2_cont.children["C"]

    # If Player 1 continues, move 4: Player 2 chooses Stop or Continue.
    g.append_move(n3_cont, player="2", actions=["S", "C"])
    n4_stop = n3_cont.children["S"]
    n4_cont = n3_cont.children["C"]

    # If Player 2 continues, move 5: Player 1 chooses Stop or Continue.
    g.append_move(n4_cont, player="1", actions=["S", "C"])
    n5_stop = n4_cont.children["S"]
    n5_cont = n4_cont.children["C"]

    # Distinct outcomes for each terminal node.
    out_1_stop = g.add_outcome([1, 1], label="Move1_Stop")
    out_2_stop = g.add_outcome([0, 3], label="Move2_Stop")
    out_3_stop = g.add_outcome([2, 2], label="Move3_Stop")
    out_4_stop = g.add_outcome([1, 4], label="Move4_Stop")
    out_5_stop = g.add_outcome([3, 3], label="Move5_Stop")
    out_timeout = g.add_outcome([0, 0], label="Move5_Continue_Timeout")

    # Attach outcomes.
    g.set_outcome(n1_stop, out_1_stop)
    g.set_outcome(n2_stop, out_2_stop)
    g.set_outcome(n3_stop, out_3_stop)
    g.set_outcome(n4_stop, out_4_stop)
    g.set_outcome(n5_stop, out_5_stop)
    g.set_outcome(n5_cont, out_timeout)

    return g


if __name__ == "__main__":
    g = build_page_454_exercise_5a()

    out_path = Path(__file__).with_name("game_page454_exercise5.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")