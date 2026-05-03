from pathlib import Path
import pygambit as gbt


def build_one_player_one_move_example_fig3_v0():
    g = gbt.Game.new_tree(
        players=["1", "2", "3"],
        title="One-Player-One-Move Example from the Article V0"
    )

    # Player 1 moves first
    g.append_move(g.root, "1", actions=["A", "D"])
    p1 = g.root

    # Player 2 moves after A
    after_A = p1.children["A"]
    g.append_move(after_A, "2", actions=["a", "d"])

    # Immediate terminal after A then a
    out_A_a = g.add_outcome([1, 1, 1], label="A_then_a")
    g.set_outcome(after_A.children["a"], out_A_a)

    # Player 3 moves after D
    after_D = p1.children["D"]
    g.append_move(after_D, "3", actions=["l", "r"])
    p3_infoset = after_D.infoset

    # Player 3 also moves after A then d, in same infoset
    after_A_d = after_A.children["d"]
    g.append_infoset(after_A_d, p3_infoset)

    # Terminal outcomes after D
    out_D_l = g.add_outcome([3, 2, 2], label="D_then_l")
    out_D_r = g.add_outcome([0, 0, 0], label="D_then_r")
    g.set_outcome(after_D.children["l"], out_D_l)
    g.set_outcome(after_D.children["r"], out_D_r)

    # Terminal outcomes after A then d
    out_A_d_l = g.add_outcome([4, 4, 0], label="A_then_d_then_l")
    out_A_d_r = g.add_outcome([0, 0, 1], label="A_then_d_then_r")
    g.set_outcome(after_A_d.children["l"], out_A_d_l)
    g.set_outcome(after_A_d.children["r"], out_A_d_r)

    return g


if __name__ == "__main__":
    game = build_one_player_one_move_example_fig3_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
    