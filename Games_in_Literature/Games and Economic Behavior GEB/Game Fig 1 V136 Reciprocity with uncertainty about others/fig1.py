from pathlib import Path
import pygambit as gbt


def build_geb_centipede_fig1() -> gbt.Game:
    """Construct the 3-node centipede game in Fig. 1."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Centipede Game Fig. 1"
    )

    # Node 1: Player 1 chooses whether to stay in the game or end it.
    g.append_move(g.root, player="Player 1", actions=["y_1", "d_1"])

    node_y1 = g.root.children["y_1"]
    node_d1 = g.root.children["d_1"]

    out_d1 = g.add_outcome([3, 0], label="d_1")
    g.set_outcome(node_d1, out_d1)

    # Node 2: Player 2 chooses whether to stay in the game or end it.
    g.append_move(node_y1, player="Player 2", actions=["y_2", "d_2"])

    node_y2 = node_y1.children["y_2"]
    node_d2 = node_y1.children["d_2"]

    out_d2 = g.add_outcome([0, 3], label="d_2")
    g.set_outcome(node_d2, out_d2)

    # Node 3: Player 1 chooses whether to stay or end.
    # In this figure, both actions end the game.
    g.append_move(node_y2, player="Player 1", actions=["y_3", "d_3"])

    node_y3 = node_y2.children["y_3"]
    node_d3 = node_y2.children["d_3"]

    out_d3 = g.add_outcome([5, 2], label="d_3")
    out_y3 = g.add_outcome([4, 4], label="y_3")

    g.set_outcome(node_d3, out_d3)
    g.set_outcome(node_y3, out_y3)

    return g


if __name__ == "__main__":
    g = build_geb_centipede_fig1()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")