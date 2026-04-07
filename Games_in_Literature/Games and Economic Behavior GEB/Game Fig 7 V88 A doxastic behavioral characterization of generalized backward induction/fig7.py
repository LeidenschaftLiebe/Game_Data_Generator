from pathlib import Path
import pygambit as gbt


def build_fig7_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 7 Forward and Backward Belief V0"
    )

    # Player 1 at the root
    g.append_move(g.root, "Player 1", actions=["a", "b", "c"])
    node_a = g.root.children["a"]
    node_b = g.root.children["b"]
    node_c = g.root.children["c"]

    # Player 2 after a, with same infoset after b and c
    g.append_move(node_a, "Player 2", actions=["d", "e"])
    shared_infoset = node_a.infoset
    g.append_infoset(node_b, shared_infoset)
    g.append_infoset(node_c, shared_infoset)

    # Distinct outcomes for every terminal history
    out_a_d = g.add_outcome([2, 1], label="a_d")
    out_a_e = g.add_outcome([1, 0], label="a_e")

    out_b_d = g.add_outcome([1, 1], label="b_d")
    out_b_e = g.add_outcome([2, 0], label="b_e")

    out_c_d = g.add_outcome([0, 0], label="c_d")
    out_c_e = g.add_outcome([0, 1], label="c_e")

    # Assign outcomes
    g.set_outcome(node_a.children["d"], out_a_d)
    g.set_outcome(node_a.children["e"], out_a_e)

    g.set_outcome(node_b.children["d"], out_b_d)
    g.set_outcome(node_b.children["e"], out_b_e)

    g.set_outcome(node_c.children["d"], out_c_d)
    g.set_outcome(node_c.children["e"], out_c_e)

    return g


if __name__ == "__main__":
    game = build_fig7_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
