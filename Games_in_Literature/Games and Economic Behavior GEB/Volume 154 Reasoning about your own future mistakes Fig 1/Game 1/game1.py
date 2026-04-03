from pathlib import Path
import pygambit as gbt


def build_geb_fig1_game1() -> gbt.Game:
    """Construct Fig. 1, Game Γ1 from the GEB article."""
    g = gbt.Game.new_tree(
        players=["Player 1"],
        title="GEB Fig. 1 Game 1"
    )

    # Player 1 first chooses between a and b.
    g.append_move(g.root, player="Player 1", actions=["a", "b"])

    node_a = g.root.children["a"]
    node_b = g.root.children["b"]

    # If b is chosen, the game ends immediately.
    out_b = g.add_outcome([1], label="b")
    g.set_outcome(node_b, out_b)

    # If a is chosen, Player 1 moves again and chooses between c and d.
    g.append_move(node_a, player="Player 1", actions=["c", "d"])

    node_ac = node_a.children["c"]
    node_ad = node_a.children["d"]

    # Distinct terminal outcomes for the continuation after a.
    out_ac = g.add_outcome([1], label="a_c")
    out_ad = g.add_outcome([0], label="a_d")

    g.set_outcome(node_ac, out_ac)
    g.set_outcome(node_ad, out_ad)

    return g


if __name__ == "__main__":
    g = build_geb_fig1_game1()

    out_path = Path(__file__).with_name("game1_v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
