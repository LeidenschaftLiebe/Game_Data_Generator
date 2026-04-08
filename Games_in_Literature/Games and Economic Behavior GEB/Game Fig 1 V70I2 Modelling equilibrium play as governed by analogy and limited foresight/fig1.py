from pathlib import Path
import pygambit as gbt


def build_fig1_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 1 Analogy Example V0"
    )

    # Nature chooses between h1 and h2 with equal probability
    g.append_move(g.root, g.players.chance, actions=["h1", "h2"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    h1 = g.root.children["h1"]
    h2 = g.root.children["h2"]

    # Player 1 moves after each nature branch
    g.append_move(h1, "Player 1", actions=["L", "R"])
    g.append_move(h2, "Player 1", actions=["L", "R"])

    h1_L = h1.children["L"]
    h1_R = h1.children["R"]
    h2_L = h2.children["L"]
    h2_R = h2.children["R"]

    # Player 2 moves
    g.append_move(h1_L, "Player 2", actions=["l", "r"])
    g.append_move(h1_R, "Player 2", actions=["l", "r"])
    g.append_move(h2_L, "Player 2", actions=["l", "r"])
    g.append_move(h2_R, "Player 2", actions=["u", "d"])

    # Distinct outcomes
    out_h1_L_l = g.add_outcome([4, 2], label="h1_L_l")
    out_h1_L_r = g.add_outcome([0, 0], label="h1_L_r")
    out_h1_R_l = g.add_outcome([0, 2], label="h1_R_l")
    out_h1_R_r = g.add_outcome([0, 0], label="h1_R_r")

    out_h2_L_l = g.add_outcome([0, 2], label="h2_L_l")
    out_h2_L_r = g.add_outcome([0, 0], label="h2_L_r")
    out_h2_R_u = g.add_outcome([0, 0], label="h2_R_u")
    out_h2_R_d = g.add_outcome([3, 2], label="h2_R_d")

    # Assign outcomes
    g.set_outcome(h1_L.children["l"], out_h1_L_l)
    g.set_outcome(h1_L.children["r"], out_h1_L_r)
    g.set_outcome(h1_R.children["l"], out_h1_R_l)
    g.set_outcome(h1_R.children["r"], out_h1_R_r)

    g.set_outcome(h2_L.children["l"], out_h2_L_l)
    g.set_outcome(h2_L.children["r"], out_h2_L_r)
    g.set_outcome(h2_R.children["u"], out_h2_R_u)
    g.set_outcome(h2_R.children["d"], out_h2_R_d)

    return g


if __name__ == "__main__":
    game = build_fig1_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
