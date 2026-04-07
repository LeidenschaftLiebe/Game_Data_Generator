from pathlib import Path
import pygambit as gbt


def build_fig2_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2", "Player 3"],
        title="GEB Fig. 2 Perfect-Information Game V0"
    )

    # Player 1 moves first
    g.append_move(g.root, "Player 1", actions=["a1", "b1"])
    node_a1 = g.root.children["a1"]
    node_b1 = g.root.children["b1"]

    # If a1, Player 2 moves
    g.append_move(node_a1, "Player 2", actions=["a2", "b2"])
    node_a2 = node_a1.children["a2"]
    node_b2 = node_a1.children["b2"]

    # If a1 -> a2, Player 3 moves
    g.append_move(node_a2, "Player 3", actions=["a3", "b3"])

    # If a1 -> b2, Player 3 moves
    g.append_move(node_b2, "Player 3", actions=["c3", "d3"])

    # Distinct outcomes for each terminal history
    out_a1_a2_a3 = g.add_outcome([1, 1, 0], label="a1_a2_a3")
    out_a1_a2_b3 = g.add_outcome([3, 3, 1], label="a1_a2_b3")
    out_a1_b2_c3 = g.add_outcome([1, 2, 1], label="a1_b2_c3")
    out_a1_b2_d3 = g.add_outcome([4, 0, 0], label="a1_b2_d3")
    out_b1 = g.add_outcome([2, 2, 0], label="b1")

    # Assign outcomes
    g.set_outcome(node_a2.children["a3"], out_a1_a2_a3)
    g.set_outcome(node_a2.children["b3"], out_a1_a2_b3)
    g.set_outcome(node_b2.children["c3"], out_a1_b2_c3)
    g.set_outcome(node_b2.children["d3"], out_a1_b2_d3)
    g.set_outcome(node_b1, out_b1)

    return g


if __name__ == "__main__":
    game = build_fig2_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


