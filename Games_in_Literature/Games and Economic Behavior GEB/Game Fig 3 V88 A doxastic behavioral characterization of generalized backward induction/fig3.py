from pathlib import Path
import pygambit as gbt


def build_fig3_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2", "Player 3"],
        title="GEB Fig. 3 Perfect-Information Example V0"
    )

    # Player 1 at the root
    g.append_move(g.root, "Player 1", actions=["a1", "b1"])
    node_a1 = g.root.children["a1"]
    node_b1 = g.root.children["b1"]

    # Player 2 after a1
    g.append_move(node_a1, "Player 2", actions=["a2", "b2"])
    node_a2 = node_a1.children["a2"]
    node_b2 = node_a1.children["b2"]

    # Player 3 after a2
    g.append_move(node_a2, "Player 3", actions=["a3", "b3"])
    node_a3 = node_a2.children["a3"]
    node_b3 = node_a2.children["b3"]

    # Player 3 after b2
    g.append_move(node_b2, "Player 3", actions=["c3", "d3"])
    node_c3 = node_b2.children["c3"]
    node_d3 = node_b2.children["d3"]

    # Distinct outcomes for each terminal history
    out_b1 = g.add_outcome([2, 2, 0], label="b1")
    out_a1_a2_a3 = g.add_outcome([1, 1, 0], label="a1_a2_a3")
    out_a1_a2_b3 = g.add_outcome([3, 3, 1], label="a1_a2_b3")
    out_a1_b2_c3 = g.add_outcome([1, 2, 1], label="a1_b2_c3")
    out_a1_b2_d3 = g.add_outcome([4, 0, 0], label="a1_b2_d3")

    # Assign outcomes
    g.set_outcome(node_b1, out_b1)
    g.set_outcome(node_a3, out_a1_a2_a3)
    g.set_outcome(node_b3, out_a1_a2_b3)
    g.set_outcome(node_c3, out_a1_b2_c3)
    g.set_outcome(node_d3, out_a1_b2_d3)

    return g


if __name__ == "__main__":
    game = build_fig3_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")