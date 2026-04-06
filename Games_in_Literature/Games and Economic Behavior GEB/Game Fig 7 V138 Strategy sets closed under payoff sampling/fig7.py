from pathlib import Path
import pygambit as gbt


def build_geb_centipede_fig7() -> gbt.Game:
    """Construct Fig. 7 centipede game with d = 8 decision nodes."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Centipede Fig. 7"
    )

    # Decision node 1: Player 1 moves first.
    g.append_move(g.root, player="Player 1", actions=["Stop_1", "Continue_1"])

    node_stop_1 = g.root.children["Stop_1"]
    node_cont_1 = g.root.children["Continue_1"]

    out_stop_1 = g.add_outcome([0, 0], label="Stop_1")
    g.set_outcome(node_stop_1, out_stop_1)

    # Decision node 2: Player 2.
    g.append_move(node_cont_1, player="Player 2", actions=["Stop_2", "Continue_2"])

    node_stop_2 = node_cont_1.children["Stop_2"]
    node_cont_2 = node_cont_1.children["Continue_2"]

    out_stop_2 = g.add_outcome([-1, 3], label="Stop_2")
    g.set_outcome(node_stop_2, out_stop_2)

    # Decision node 3: Player 1.
    g.append_move(node_cont_2, player="Player 1", actions=["Stop_3", "Continue_3"])

    node_stop_3 = node_cont_2.children["Stop_3"]
    node_cont_3 = node_cont_2.children["Continue_3"]

    out_stop_3 = g.add_outcome([2, 2], label="Stop_3")
    g.set_outcome(node_stop_3, out_stop_3)

    # Decision node 4: Player 2.
    g.append_move(node_cont_3, player="Player 2", actions=["Stop_4", "Continue_4"])

    node_stop_4 = node_cont_3.children["Stop_4"]
    node_cont_4 = node_cont_3.children["Continue_4"]

    out_stop_4 = g.add_outcome([1, 5], label="Stop_4")
    g.set_outcome(node_stop_4, out_stop_4)

    # Decision node 5: Player 1.
    g.append_move(node_cont_4, player="Player 1", actions=["Stop_5", "Continue_5"])

    node_stop_5 = node_cont_4.children["Stop_5"]
    node_cont_5 = node_cont_4.children["Continue_5"]

    out_stop_5 = g.add_outcome([4, 4], label="Stop_5")
    g.set_outcome(node_stop_5, out_stop_5)

    # Decision node 6: Player 2.
    g.append_move(node_cont_5, player="Player 2", actions=["Stop_6", "Continue_6"])

    node_stop_6 = node_cont_5.children["Stop_6"]
    node_cont_6 = node_cont_5.children["Continue_6"]

    out_stop_6 = g.add_outcome([3, 7], label="Stop_6")
    g.set_outcome(node_stop_6, out_stop_6)

    # Decision node 7: Player 1.
    g.append_move(node_cont_6, player="Player 1", actions=["Stop_7", "Continue_7"])

    node_stop_7 = node_cont_6.children["Stop_7"]
    node_cont_7 = node_cont_6.children["Continue_7"]

    out_stop_7 = g.add_outcome([6, 6], label="Stop_7")
    g.set_outcome(node_stop_7, out_stop_7)

    # Decision node 8: Player 2.
    g.append_move(node_cont_7, player="Player 2", actions=["Stop_8", "Continue_8"])

    node_stop_8 = node_cont_7.children["Stop_8"]
    node_cont_8 = node_cont_7.children["Continue_8"]

    out_stop_8 = g.add_outcome([5, 9], label="Stop_8")
    out_continue_8 = g.add_outcome([8, 8], label="Continue_8")

    g.set_outcome(node_stop_8, out_stop_8)
    g.set_outcome(node_cont_8, out_continue_8)

    return g


if __name__ == "__main__":
    g = build_geb_centipede_fig7()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")




