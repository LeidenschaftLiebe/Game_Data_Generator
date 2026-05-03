from pathlib import Path
import pygambit as gbt


def build_example6_v0():
    g = gbt.Game.new_tree(
        players=["1"],
        title="Imperfect Recall Example 6 V0"
    )

    # Chance moves first
    g.append_move(g.root, g.players.chance, actions=["L", "R"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    left_branch = g.root.children["L"]
    right_branch = g.root.children["R"]

    # After L, the player first faces d2
    g.append_move(left_branch, "1", actions=["S", "B"])
    first_d2 = left_branch

    # After R, the player first faces d1
    g.append_move(right_branch, "1", actions=["S", "B"])
    first_d1 = right_branch

    # Immediate outcomes after choosing S at the first decision points
    out_first_d2_S = g.add_outcome([3], label="first_d2_then_S")
    out_first_d1_S = g.add_outcome([3], label="first_d1_then_S")
    g.set_outcome(first_d2.children["S"], out_first_d2_S)
    g.set_outcome(first_d1.children["S"], out_first_d1_S)

    # If B is chosen, the player moves to the other type of decision point
    later_d1 = first_d2.children["B"]   # after L then B
    later_d2 = first_d1.children["B"]   # after R then B

    # first_d1 and later_d1 are the same infoset
    g.append_infoset(later_d1, first_d1.infoset)

    # first_d2 and later_d2 are the same infoset
    g.append_infoset(later_d2, first_d2.infoset)

    # Outcomes after later d1
    out_later_d1_S = g.add_outcome([0], label="later_d1_then_S")
    out_later_d1_B = g.add_outcome([2], label="later_d1_then_B")
    g.set_outcome(later_d1.children["S"], out_later_d1_S)
    g.set_outcome(later_d1.children["B"], out_later_d1_B)

    # Outcomes after later d2
    out_later_d2_S = g.add_outcome([0], label="later_d2_then_S")
    out_later_d2_B = g.add_outcome([2], label="later_d2_then_B")
    g.set_outcome(later_d2.children["S"], out_later_d2_S)
    g.set_outcome(later_d2.children["B"], out_later_d2_B)

    return g


if __name__ == "__main__":
    game = build_example6_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
    