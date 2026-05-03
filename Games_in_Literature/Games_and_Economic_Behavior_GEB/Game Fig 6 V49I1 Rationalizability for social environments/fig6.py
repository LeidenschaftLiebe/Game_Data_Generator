from pathlib import Path
import pygambit as gbt


def build_social_environment_example3_v0():
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Social Environment Example 3 V0"
    )

    # Nature chooses the ordering
    g.append_move(g.root, g.players.chance, actions=["(x1,x2)", "(x2,x1)"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    order_x1_first = g.root.children["(x1,x2)"]
    order_x2_first = g.root.children["(x2,x1)"]

    # Player 1 moves without knowing Nature's ordering
    g.append_move(order_x1_first, "1", actions=["1", "0"])
    g.append_infoset(order_x2_first, order_x1_first.infoset)

    p1_after_x1_first = order_x1_first
    p1_after_x2_first = order_x2_first

    # Player 2 moves without knowing Nature's ordering or Player 1's move
    g.append_move(p1_after_x1_first.children["1"], "2", actions=["1", "0"])
    p2_infoset = p1_after_x1_first.children["1"].infoset

    g.append_infoset(p1_after_x1_first.children["0"], p2_infoset)
    g.append_infoset(p1_after_x2_first.children["1"], p2_infoset)
    g.append_infoset(p1_after_x2_first.children["0"], p2_infoset)

    # Distinct outcomes for every terminal node
    out_order_x1_both_support = g.add_outcome([2, 1], label="order_x1_first_both_support")
    out_order_x1_only_p1 = g.add_outcome([2, 1], label="order_x1_first_only_p1_supports")
    out_order_x1_only_p2 = g.add_outcome([1, 2], label="order_x1_first_only_p2_supports")
    out_order_x1_no_one = g.add_outcome([0, 0], label="order_x1_first_no_one_supports")

    out_order_x2_both_support = g.add_outcome([1, 2], label="order_x2_first_both_support")
    out_order_x2_only_p1 = g.add_outcome([2, 1], label="order_x2_first_only_p1_supports")
    out_order_x2_only_p2 = g.add_outcome([1, 2], label="order_x2_first_only_p2_supports")
    out_order_x2_no_one = g.add_outcome([0, 0], label="order_x2_first_no_one_supports")

    # If Nature chose (x1,x2)
    g.set_outcome(p1_after_x1_first.children["1"].children["1"], out_order_x1_both_support)
    g.set_outcome(p1_after_x1_first.children["1"].children["0"], out_order_x1_only_p1)
    g.set_outcome(p1_after_x1_first.children["0"].children["1"], out_order_x1_only_p2)
    g.set_outcome(p1_after_x1_first.children["0"].children["0"], out_order_x1_no_one)

    # If Nature chose (x2,x1)
    g.set_outcome(p1_after_x2_first.children["1"].children["1"], out_order_x2_both_support)
    g.set_outcome(p1_after_x2_first.children["1"].children["0"], out_order_x2_only_p1)
    g.set_outcome(p1_after_x2_first.children["0"].children["1"], out_order_x2_only_p2)
    g.set_outcome(p1_after_x2_first.children["0"].children["0"], out_order_x2_no_one)

    return g


if __name__ == "__main__":
    game = build_social_environment_example3_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


    