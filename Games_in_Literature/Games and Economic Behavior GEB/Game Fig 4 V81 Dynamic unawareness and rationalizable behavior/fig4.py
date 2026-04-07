from pathlib import Path
import pygambit as gbt


def build_fig4_standard_game_v0():
    g = gbt.Game.new_tree(
        players=["Expert", "Decision Maker"],
        title="GEB Fig. 4 Standard Recommendation V0"
    )

    # Nature chooses the state
    g.append_move(g.root, g.players.chance, actions=["gamma0", "gamma1"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    gamma0 = g.root.children["gamma0"]
    gamma1 = g.root.children["gamma1"]

    # Expert moves after each state
    g.append_move(gamma0, "Expert", actions=["0", "1"])
    g.append_move(gamma1, "Expert", actions=["0", "1"])

    g0_0 = gamma0.children["0"]
    g0_1 = gamma0.children["1"]
    g1_0 = gamma1.children["0"]
    g1_1 = gamma1.children["1"]

    # Decision maker information sets
    g.append_move(g0_0, "Decision Maker", actions=["a0", "a1"])
    dm_info_0 = g0_0.infoset
    g.append_infoset(g1_0, dm_info_0)

    g.append_move(g0_1, "Decision Maker", actions=["a0", "a1"])
    dm_info_1 = g0_1.infoset
    g.append_infoset(g1_1, dm_info_1)

    # Distinct outcomes for every terminal history
    out_g0_0_a0 = g.add_outcome([0, 0], label="gamma0_0_a0")
    out_g0_0_a1 = g.add_outcome([-1, -1], label="gamma0_0_a1")

    out_g0_1_a0 = g.add_outcome([0, -10], label="gamma0_1_a0")
    out_g0_1_a1 = g.add_outcome([-1, -11], label="gamma0_1_a1")

    out_g1_0_a0 = g.add_outcome([-1, -11], label="gamma1_0_a0")
    out_g1_0_a1 = g.add_outcome([0, -10], label="gamma1_0_a1")

    out_g1_1_a0 = g.add_outcome([-1, -1], label="gamma1_1_a0")
    out_g1_1_a1 = g.add_outcome([0, 0], label="gamma1_1_a1")

    # Assign outcomes
    g.set_outcome(g0_0.children["a0"], out_g0_0_a0)
    g.set_outcome(g0_0.children["a1"], out_g0_0_a1)

    g.set_outcome(g0_1.children["a0"], out_g0_1_a0)
    g.set_outcome(g0_1.children["a1"], out_g0_1_a1)

    g.set_outcome(g1_0.children["a0"], out_g1_0_a0)
    g.set_outcome(g1_0.children["a1"], out_g1_0_a1)

    g.set_outcome(g1_1.children["a0"], out_g1_1_a0)
    g.set_outcome(g1_1.children["a1"], out_g1_1_a1)

    return g


if __name__ == "__main__":
    game = build_fig4_standard_game_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

