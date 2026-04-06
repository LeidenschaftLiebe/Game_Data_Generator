from pathlib import Path
import pygambit as gbt


def build_geb_fig1_extensive_game() -> gbt.Game:
    """Construct Fig. 1 extensive-form game G."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Extensive-form Game Fig. 1"
    )

    # Player 1 moves first.
    g.append_move(g.root, player="Player 1", actions=["L", "R"])

    node_L = g.root.children["L"]
    node_R = g.root.children["R"]

    # After L, Player 2 chooses between l_1 and r_1.
    g.append_move(node_L, player="Player 2", actions=["l_1", "r_1"])

    node_L_l1 = node_L.children["l_1"]
    node_L_r1 = node_L.children["r_1"]

    out_L_l1 = g.add_outcome([7, 11], label="L_l1")
    out_L_r1 = g.add_outcome([0, 3], label="L_r1")

    g.set_outcome(node_L_l1, out_L_l1)
    g.set_outcome(node_L_r1, out_L_r1)

    # After R, Player 2 chooses between l and r.
    g.append_move(node_R, player="Player 2", actions=["l", "r"])

    node_R_l = node_R.children["l"]
    node_R_r = node_R.children["r"]

    # Player 1 then moves without knowing whether Player 2 chose l or r.
    g.append_move(node_R_l, player="Player 1", actions=["L_1", "R_1"])
    g.append_infoset(node_R_r, node_R_l.infoset)

    node_R_l_L1 = node_R_l.children["L_1"]
    node_R_l_R1 = node_R_l.children["R_1"]

    node_R_r_L1 = node_R_r.children["L_1"]
    node_R_r_R1 = node_R_r.children["R_1"]

    out_R_l_L1 = g.add_outcome([10, 15], label="R_l_L1")
    out_R_l_R1 = g.add_outcome([2, 1], label="R_l_R1")
    out_R_r_L1 = g.add_outcome([1, 2], label="R_r_L1")
    out_R_r_R1 = g.add_outcome([8, 6], label="R_r_R1")

    g.set_outcome(node_R_l_L1, out_R_l_L1)
    g.set_outcome(node_R_l_R1, out_R_l_R1)
    g.set_outcome(node_R_r_L1, out_R_r_L1)
    g.set_outcome(node_R_r_R1, out_R_r_R1)

    return g


if __name__ == "__main__":
    g = build_geb_fig1_extensive_game()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
