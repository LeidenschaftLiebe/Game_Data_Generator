from pathlib import Path
import pygambit as gbt


def build_geb_fig4() -> gbt.Game:
    """Construct Fig. 4 from the GEB article."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 4"
    )

    # Player 1 first chooses between a, b, and c.
    g.append_move(g.root, player="Player 1", actions=["a", "b", "c"])

    node_a = g.root.children["a"]
    node_b = g.root.children["b"]
    node_c = g.root.children["c"]

    # If c is chosen, the game ends immediately.
    out_c = g.add_outcome([1, 0], label="c")
    g.set_outcome(node_c, out_c)

    # After a or b, Player 2 chooses between d, e, and f
    # without knowing whether Player 1 chose a or b.
    g.append_move(node_a, player="Player 2", actions=["d", "e", "f"])
    g.append_infoset(node_b, node_a.infoset)

    node_ad = node_a.children["d"]
    node_ae = node_a.children["e"]
    node_af = node_a.children["f"]

    node_bd = node_b.children["d"]
    node_be = node_b.children["e"]
    node_bf = node_b.children["f"]

    # Immediate terminal outcomes after e and f.
    out_ae = g.add_outcome([0, 5], label="a_e")
    out_af = g.add_outcome([1, 4], label="a_f")
    out_be = g.add_outcome([0, 4], label="b_e")
    out_bf = g.add_outcome([1, 5], label="b_f")

    g.set_outcome(node_ae, out_ae)
    g.set_outcome(node_af, out_af)
    g.set_outcome(node_be, out_be)
    g.set_outcome(node_bf, out_bf)

    # After d, Player 2 chooses again between g and h
    # without knowing whether the path started with a or b.
    g.append_move(node_ad, player="Player 2", actions=["g", "h"])
    g.append_infoset(node_bd, node_ad.infoset)

    node_adg = node_ad.children["g"]
    node_adh = node_ad.children["h"]

    node_bdg = node_bd.children["g"]
    node_bdh = node_bd.children["h"]

    # Terminal outcomes after the second Player 2 move.
    out_adg = g.add_outcome([2, 1], label="a_d_g")
    out_adh = g.add_outcome([0, 0], label="a_d_h")
    out_bdg = g.add_outcome([2, 0], label="b_d_g")
    out_bdh = g.add_outcome([0, 3], label="b_d_h")

    g.set_outcome(node_adg, out_adg)
    g.set_outcome(node_adh, out_adh)
    g.set_outcome(node_bdg, out_bdg)
    g.set_outcome(node_bdh, out_bdh)

    return g


if __name__ == "__main__":
    g = build_geb_fig4()

    out_path = Path(__file__).with_name("game_fig4_v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")


