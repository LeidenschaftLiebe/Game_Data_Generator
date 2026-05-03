from pathlib import Path
import pygambit as gbt


def build_payoff_information_example2():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Payoff Information Example 2"
    )

    # Nature chooses Player 1's type
    g.append_move(g.root, g.players.chance, actions=["Strong", "Weak"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(9, 10), gbt.Rational(1, 10)])

    node_strong = g.root.children["Strong"]
    node_weak = g.root.children["Weak"]

    # Player 1 moves after learning type
    g.append_move(node_strong, player="Player 1", actions=["Out", "In"])
    g.append_move(node_weak, player="Player 1", actions=["Out", "In"])

    strong_out = node_strong.children["Out"]
    strong_in = node_strong.children["In"]
    weak_out = node_weak.children["Out"]
    weak_in = node_weak.children["In"]

    # Out outcomes
    out_strong_out = g.add_outcome([0, 0], label="Strong_Out")
    out_weak_out = g.add_outcome([0, 0], label="Weak_Out")
    g.set_outcome(strong_out, out_strong_out)
    g.set_outcome(weak_out, out_weak_out)

    # Player 2 responds after In, without knowing type
    g.append_move(strong_in, player="Player 2", actions=["Up", "Down", "X"])
    g.append_infoset(weak_in, strong_in.infoset)

    # Outcomes after Strong and In
    out_strong_up = g.add_outcome([2, 1], label="Strong_In_Up")
    out_strong_down = g.add_outcome([-1, 0], label="Strong_In_Down")
    out_strong_x = g.add_outcome([1, -1], label="Strong_In_X")

    g.set_outcome(strong_in.children["Up"], out_strong_up)
    g.set_outcome(strong_in.children["Down"], out_strong_down)
    g.set_outcome(strong_in.children["X"], out_strong_x)

    # Outcomes after Weak and In
    out_weak_up = g.add_outcome([1, 0], label="Weak_In_Up")
    out_weak_down = g.add_outcome([-1, 1], label="Weak_In_Down")
    out_weak_x = g.add_outcome([3, -1], label="Weak_In_X")

    g.set_outcome(weak_in.children["Up"], out_weak_up)
    g.set_outcome(weak_in.children["Down"], out_weak_down)
    g.set_outcome(weak_in.children["X"], out_weak_x)

    return g


if __name__ == "__main__":
    g = build_payoff_information_example2()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



