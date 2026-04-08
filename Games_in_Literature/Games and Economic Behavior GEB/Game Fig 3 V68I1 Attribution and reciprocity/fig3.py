from pathlib import Path
import pygambit as gbt


def build_gamma3_v0():
    g = gbt.Game.new_tree(
        players=["Principal", "Agent"],
        title="GEB Fig. 3 Gamma3 V0"
    )

    # Principal chooses nominal wage
    g.append_move(g.root, "Principal", actions=["Low", "High"])
    low_node = g.root.children["Low"]
    high_node = g.root.children["High"]

    # Chance determines the economic condition after each wage choice
    g.append_move(low_node, g.players.chance, actions=["NoInflation", "Inflation"])
    g.set_chance_probs(low_node.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    g.append_move(high_node, g.players.chance, actions=["NoInflation", "Inflation"])
    g.set_chance_probs(high_node.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    low_noinf = low_node.children["NoInflation"]
    low_inf = low_node.children["Inflation"]
    high_noinf = high_node.children["NoInflation"]
    high_inf = high_node.children["Inflation"]

    # Agent chooses effort after each state is revealed
    g.append_move(low_noinf, "Agent", actions=["low", "high"])
    g.append_move(low_inf, "Agent", actions=["low", "high"])
    g.append_move(high_noinf, "Agent", actions=["low", "high"])
    g.append_move(high_inf, "Agent", actions=["low", "high"])

    # Distinct outcomes
    out_low_noinf_low = g.add_outcome([4, 4], label="Low_NoInflation_low")
    out_low_noinf_high = g.add_outcome([12, 3], label="Low_NoInflation_high")

    out_low_inf_low = g.add_outcome([4, 2], label="Low_Inflation_low")
    out_low_inf_high = g.add_outcome([12, 1], label="Low_Inflation_high")

    out_high_noinf_low = g.add_outcome([2, 6], label="High_NoInflation_low")
    out_high_noinf_high = g.add_outcome([10, 5], label="High_NoInflation_high")

    out_high_inf_low = g.add_outcome([2, 4], label="High_Inflation_low")
    out_high_inf_high = g.add_outcome([10, 3], label="High_Inflation_high")

    # Assign outcomes
    g.set_outcome(low_noinf.children["low"], out_low_noinf_low)
    g.set_outcome(low_noinf.children["high"], out_low_noinf_high)

    g.set_outcome(low_inf.children["low"], out_low_inf_low)
    g.set_outcome(low_inf.children["high"], out_low_inf_high)

    g.set_outcome(high_noinf.children["low"], out_high_noinf_low)
    g.set_outcome(high_noinf.children["high"], out_high_noinf_high)

    g.set_outcome(high_inf.children["low"], out_high_inf_low)
    g.set_outcome(high_inf.children["high"], out_high_inf_high)

    return g


if __name__ == "__main__":
    game = build_gamma3_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



