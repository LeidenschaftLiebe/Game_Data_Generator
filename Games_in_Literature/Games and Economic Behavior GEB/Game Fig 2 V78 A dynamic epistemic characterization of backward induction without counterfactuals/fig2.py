from pathlib import Path
import pygambit as gbt


def build_fig2_perfect_information_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2", "Player 3"],
        title="GEB Fig. 2 Perfect-Information Game V0"
    )

    # Player 1 moves first
    g.append_move(g.root, "Player 1", actions=["a1", "b1"])
    node_a1 = g.root.children["a1"]
    node_b1 = g.root.children["b1"]

    # Player 2 moves after a1
    g.append_move(node_a1, "Player 2", actions=["a2", "b2"])
    node_a2 = node_a1.children["a2"]
    node_b2 = node_a1.children["b2"]

    # Player 3 moves after a1 -> a2
    g.append_move(node_a2, "Player 3", actions=["a3", "b3"])
    node_a3 = node_a2.children["a3"]
    node_b3 = node_a2.children["b3"]

    # Player 3 moves after b1
    g.append_move(node_b1, "Player 3", actions=["c2", "d2", "e2"])
    node_c2 = node_b1.children["c2"]
    node_d2 = node_b1.children["d2"]
    node_e2 = node_b1.children["e2"]

    # Distinct outcomes for every terminal history
    out_a1_a2_a3 = g.add_outcome([2, 2, 2], label="a1_a2_a3")
    out_a1_a2_b3 = g.add_outcome([1, 1, 1], label="a1_a2_b3")
    out_a1_b2 = g.add_outcome([1, 0, 0], label="a1_b2")

    out_b1_c2 = g.add_outcome([3, 0, 1], label="b1_c2")
    out_b1_d2 = g.add_outcome([0, 0, 2], label="b1_d2")
    out_b1_e2 = g.add_outcome([0, 0, 0], label="b1_e2")

    # Assign outcomes
    g.set_outcome(node_a3, out_a1_a2_a3)
    g.set_outcome(node_b3, out_a1_a2_b3)
    g.set_outcome(node_b2, out_a1_b2)

    g.set_outcome(node_c2, out_b1_c2)
    g.set_outcome(node_d2, out_b1_d2)
    g.set_outcome(node_e2, out_b1_e2)

    return g


if __name__ == "__main__":
    game = build_fig2_perfect_information_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
