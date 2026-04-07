from pathlib import Path
import pygambit as gbt


def build_fig2_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2", "Player 3", "Player 4"],
        title="GEB Fig. 2 Dynamic Choice V0"
    )

    # Player 1 at the root
    g.append_move(g.root, "Player 1", actions=["a", "b"])
    node_a = g.root.children["a"]
    node_b = g.root.children["b"]

    # Player 2 after a
    g.append_move(node_a, "Player 2", actions=["c", "d"])
    node_c = node_a.children["c"]
    node_d = node_a.children["d"]

    # Player 3 after b
    g.append_move(node_b, "Player 3", actions=["e", "f"])
    node_e = node_b.children["e"]
    node_f = node_b.children["f"]

    # Player 4 after a-d
    g.append_move(node_d, "Player 4", actions=["g", "h", "k"])

    # Player 4 after b-e shares the same infoset
    g.append_infoset(node_e, node_d.infoset)

    # Distinct outcomes for every terminal history
    out_c = g.add_outcome([2, 2, 1, 0], label="a_c")
    out_f = g.add_outcome([1, 0, 2, 0], label="b_f")

    out_d_g = g.add_outcome([3, 1, 0, 0], label="a_d_g")
    out_d_h = g.add_outcome([2, 3, 1, 2], label="a_d_h")
    out_d_k = g.add_outcome([4, 4, 0, 1], label="a_d_k")

    out_e_g = g.add_outcome([0, 2, 3, 2], label="b_e_g")
    out_e_h = g.add_outcome([3, 3, 1, 1], label="b_e_h")
    out_e_k = g.add_outcome([4, 3, 4, 0], label="b_e_k")

    # Assign outcomes
    g.set_outcome(node_c, out_c)
    g.set_outcome(node_f, out_f)

    g.set_outcome(node_d.children["g"], out_d_g)
    g.set_outcome(node_d.children["h"], out_d_h)
    g.set_outcome(node_d.children["k"], out_d_k)

    g.set_outcome(node_e.children["g"], out_e_g)
    g.set_outcome(node_e.children["h"], out_e_h)
    g.set_outcome(node_e.children["k"], out_e_k)

    return g


if __name__ == "__main__":
    game = build_fig2_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


