from pathlib import Path
import pygambit as gbt


def build_geb_fig3() -> gbt.Game:
    """Construct Fig. 3 from the GEB article."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 3"
    )

    # Player 1 moves first and chooses between a and b.
    g.append_move(g.root, player="Player 1", actions=["a", "b"])

    node_a = g.root.children["a"]
    node_b = g.root.children["b"]

    # After a, Player 1 chooses between c and d.
    g.append_move(node_a, player="Player 1", actions=["c", "d"])

    node_ac = node_a.children["c"]
    node_ad = node_a.children["d"]

    # After a then c, Player 1 chooses between e and f.
    g.append_move(node_ac, player="Player 1", actions=["e", "f"])

    node_ace = node_ac.children["e"]
    node_acf = node_ac.children["f"]

    # If e is chosen, the game ends immediately.
    out_ace = g.add_outcome([0, 0], label="a_c_e")
    g.set_outcome(node_ace, out_ace)

    # Player 2 moves after f, after d, and after b,
    # and these three decision nodes are in the same information set.
    g.append_move(node_acf, player="Player 2", actions=["g", "h", "i"])
    g.append_infoset(node_ad, node_acf.infoset)
    g.append_infoset(node_b, node_acf.infoset)

    # Terminal nodes after a then c then f.
    node_acfg = node_acf.children["g"]
    node_acfh = node_acf.children["h"]
    node_acfi = node_acf.children["i"]

    out_acfg = g.add_outcome([1, 1], label="a_c_f_g")
    out_acfh = g.add_outcome([1, 0], label="a_c_f_h")
    out_acfi = g.add_outcome([1, -1], label="a_c_f_i")

    g.set_outcome(node_acfg, out_acfg)
    g.set_outcome(node_acfh, out_acfh)
    g.set_outcome(node_acfi, out_acfi)

    # Terminal nodes after a then d.
    node_adg = node_ad.children["g"]
    node_adh = node_ad.children["h"]
    node_adi = node_ad.children["i"]

    out_adg = g.add_outcome([1, 0], label="a_d_g")
    out_adh = g.add_outcome([1, 1], label="a_d_h")
    out_adi = g.add_outcome([1, -1], label="a_d_i")

    g.set_outcome(node_adg, out_adg)
    g.set_outcome(node_adh, out_adh)
    g.set_outcome(node_adi, out_adi)

    # Terminal nodes after b.
    node_bg = node_b.children["g"]
    node_bh = node_b.children["h"]
    node_bi = node_b.children["i"]

    out_bg = g.add_outcome([1, 1], label="b_g")
    out_bh = g.add_outcome([1, 0], label="b_h")
    out_bi = g.add_outcome([0, -1], label="b_i")

    g.set_outcome(node_bg, out_bg)
    g.set_outcome(node_bh, out_bh)
    g.set_outcome(node_bi, out_bi)

    return g


if __name__ == "__main__":
    g = build_geb_fig3()

    out_path = Path(__file__).with_name("game_fig3_v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")


