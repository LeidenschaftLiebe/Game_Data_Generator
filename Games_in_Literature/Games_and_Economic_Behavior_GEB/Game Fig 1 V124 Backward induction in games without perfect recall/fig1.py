from pathlib import Path
import pygambit as gbt


def build_geb_without_perfect_recall_fig1() -> gbt.Game:
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Game Without Perfect Recall Fig. 1"
    )

    # Nature moves first
    g.append_move(g.root, g.players.chance, actions=["Left", "Right"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    node_left = g.root.children["Left"]
    node_right = g.root.children["Right"]

    # Left branch: Player 2 chooses OUT / IN
    g.append_move(node_left, player="Player 2", actions=["OUT", "IN"])
    left_out = node_left.children["OUT"]
    left_in = node_left.children["IN"]

    # Right branch: Player 1 chooses Out / In
    g.append_move(node_right, player="Player 1", actions=["Out", "In"])
    right_out = node_right.children["Out"]
    right_in = node_right.children["In"]

    # Immediate terminals
    out_left_out = g.add_outcome([1, -1], label="Left_OUT")
    out_right_out = g.add_outcome([-1, 1], label="Right_Out")
    g.set_outcome(left_out, out_left_out)
    g.set_outcome(right_out, out_right_out)

    # Upper Player 1 nodes share one infoset
    g.append_move(left_in, player="Player 1", actions=["S", "D"])
    g.append_infoset(right_in, left_in.infoset)

    # Terminals after upper choice
    out_left_in_s = g.add_outcome([-2, 2], label="Left_IN_S")
    out_left_in_d = g.add_outcome([2, -2], label="Left_IN_D")
    out_right_in_s = g.add_outcome([2, -2], label="Right_In_S")
    out_right_in_d = g.add_outcome([-2, 2], label="Right_In_D")

    g.set_outcome(left_in.children["S"], out_left_in_s)
    g.set_outcome(left_in.children["D"], out_left_in_d)
    g.set_outcome(right_in.children["S"], out_right_in_s)
    g.set_outcome(right_in.children["D"], out_right_in_d)

    return g


if __name__ == "__main__":
    g = build_geb_without_perfect_recall_fig1()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")