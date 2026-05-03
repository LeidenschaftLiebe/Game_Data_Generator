from pathlib import Path
import pygambit as gbt


def build_geb_beer_quiche():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Beer-Quiche Example"
    )

    # Nature chooses Player 1's type
    g.append_move(g.root, g.players.chance, actions=["Strong", "Weak"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(9, 10), gbt.Rational(1, 10)])

    node_strong = g.root.children["Strong"]
    node_weak = g.root.children["Weak"]

    # Player 1 chooses message/meal
    g.append_move(node_strong, player="Player 1", actions=["Quiche", "Beer"])
    g.append_move(node_weak, player="Player 1", actions=["Quiche", "Beer"])

    strong_quiche = node_strong.children["Quiche"]
    strong_beer = node_strong.children["Beer"]
    weak_quiche = node_weak.children["Quiche"]
    weak_beer = node_weak.children["Beer"]

    # Player 2 responds after Quiche; cannot observe type
    g.append_move(strong_quiche, player="Player 2", actions=["Fight", "NotFight"])
    g.append_infoset(weak_quiche, strong_quiche.infoset)

    # Player 2 responds after Beer; cannot observe type
    g.append_move(strong_beer, player="Player 2", actions=["Fight", "NotFight"])
    g.append_infoset(weak_beer, strong_beer.infoset)

    # Outcomes after Strong, Quiche
    out_sq_f = g.add_outcome([0, 0], label="Strong_Quiche_Fight")
    out_sq_n = g.add_outcome([2, 1], label="Strong_Quiche_NotFight")
    g.set_outcome(strong_quiche.children["Fight"], out_sq_f)
    g.set_outcome(strong_quiche.children["NotFight"], out_sq_n)

    # Outcomes after Weak, Quiche
    out_wq_f = g.add_outcome([1, 1], label="Weak_Quiche_Fight")
    out_wq_n = g.add_outcome([3, 0], label="Weak_Quiche_NotFight")
    g.set_outcome(weak_quiche.children["Fight"], out_wq_f)
    g.set_outcome(weak_quiche.children["NotFight"], out_wq_n)

    # Outcomes after Strong, Beer
    out_sb_f = g.add_outcome([1, 0], label="Strong_Beer_Fight")
    out_sb_n = g.add_outcome([3, 1], label="Strong_Beer_NotFight")
    g.set_outcome(strong_beer.children["Fight"], out_sb_f)
    g.set_outcome(strong_beer.children["NotFight"], out_sb_n)

    # Outcomes after Weak, Beer
    out_wb_f = g.add_outcome([0, 1], label="Weak_Beer_Fight")
    out_wb_n = g.add_outcome([2, 0], label="Weak_Beer_NotFight")
    g.set_outcome(weak_beer.children["Fight"], out_wb_f)
    g.set_outcome(weak_beer.children["NotFight"], out_wb_n)

    return g


if __name__ == "__main__":
    g = build_geb_beer_quiche()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")