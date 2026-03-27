from pathlib import Path
import pygambit as gbt


def build_job_market_signaling() -> gbt.Game:
    """Construct Watson Figure 29.1: job-market signaling."""
    g = gbt.Game.new_tree(
        players=["Worker", "Firm"],
        title="Watson Figure 29.1 - Job Market Signaling"
    )

    # Chance selects worker type.
    g.append_move(g.root, g.players.chance, actions=["High", "Low"])
    g.set_chance_probs(
        g.root.infoset,
        [gbt.Rational("1/3"), gbt.Rational("2/3")]
    )

    node_H = g.root.children["High"]
    node_L = g.root.children["Low"]

    # Worker observes type and chooses education or not.
    g.append_move(node_H, player="Worker", actions=["NoEdu_H", "Edu_H"])
    g.append_move(node_L, player="Worker", actions=["NoEdu_L", "Edu_L"])

    node_HN = node_H.children["NoEdu_H"]
    node_HE = node_H.children["Edu_H"]
    node_LN = node_L.children["NoEdu_L"]
    node_LE = node_L.children["Edu_L"]

    # Firm observes education status but not type.
    # One infoset after no education.
    g.append_move(node_HN, player="Firm", actions=["Manager", "Clerical"])
    g.append_infoset(node_LN, node_HN.infoset)

    # One infoset after education.
    g.append_move(node_HE, player="Firm", actions=["Manager", "Clerical"])
    g.append_infoset(node_LE, node_HE.infoset)

    # Terminal nodes after no education.
    hn_m = node_HN.children["Manager"]
    hn_c = node_HN.children["Clerical"]
    ln_m = node_LN.children["Manager"]
    ln_c = node_LN.children["Clerical"]

    # Terminal nodes after education.
    he_m = node_HE.children["Manager"]
    he_c = node_HE.children["Clerical"]
    le_m = node_LE.children["Manager"]
    le_c = node_LE.children["Clerical"]

    # Distinct outcomes.
    out_hn_m = g.add_outcome([10, 10], label="High_NoEdu_Manager")
    out_hn_c = g.add_outcome([4, 4], label="High_NoEdu_Clerical")

    out_ln_m = g.add_outcome([10, 0], label="Low_NoEdu_Manager")
    out_ln_c = g.add_outcome([4, 4], label="Low_NoEdu_Clerical")

    out_he_m = g.add_outcome([6, 10], label="High_Edu_Manager")
    out_he_c = g.add_outcome([0, 4], label="High_Edu_Clerical")

    out_le_m = g.add_outcome([3, 0], label="Low_Edu_Manager")
    out_le_c = g.add_outcome([-3, 4], label="Low_Edu_Clerical")

    # Attach outcomes.
    g.set_outcome(hn_m, out_hn_m)
    g.set_outcome(hn_c, out_hn_c)

    g.set_outcome(ln_m, out_ln_m)
    g.set_outcome(ln_c, out_ln_c)

    g.set_outcome(he_m, out_he_m)
    g.set_outcome(he_c, out_he_c)

    g.set_outcome(le_m, out_le_m)
    g.set_outcome(le_c, out_le_c)

    return g


if __name__ == "__main__":
    g = build_job_market_signaling()

    out_path = Path(__file__).with_name("game_figure_29_1.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
