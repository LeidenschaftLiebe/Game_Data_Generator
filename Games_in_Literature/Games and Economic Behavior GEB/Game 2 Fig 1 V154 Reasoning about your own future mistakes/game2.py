from pathlib import Path
import pygambit as gbt


def build_geb_fig1_game2() -> gbt.Game:
    """Construct Fig. 1, Game Γ2 from the GEB article."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 1 Game 2"
    )

    # Player 1 first chooses between a and b.
    g.append_move(g.root, player="Player 1", actions=["a", "b"])

    node_a = g.root.children["a"]
    node_b = g.root.children["b"]

    # If a is chosen, Player 1 moves again and chooses between c and d.
    g.append_move(node_a, player="Player 1", actions=["c", "d"])

    node_ac = node_a.children["c"]
    node_ad = node_a.children["d"]

    # If b is chosen, Player 2 chooses between e and f.
    g.append_move(node_b, player="Player 2", actions=["e", "f"])

    node_be = node_b.children["e"]
    node_bf = node_b.children["f"]

    # Distinct terminal outcomes.
    out_ac = g.add_outcome([1, 1], label="a_c")
    out_ad = g.add_outcome([0, 0], label="a_d")
    out_be = g.add_outcome([1, 1], label="b_e")
    out_bf = g.add_outcome([0, 0], label="b_f")

    g.set_outcome(node_ac, out_ac)
    g.set_outcome(node_ad, out_ad)
    g.set_outcome(node_be, out_be)
    g.set_outcome(node_bf, out_bf)

    return g


if __name__ == "__main__":
    g = build_geb_fig1_game2()

    out_path = Path(__file__).with_name("game2_v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
