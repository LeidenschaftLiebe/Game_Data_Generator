from pathlib import Path
import pygambit as gbt


def build_fig5_fig6_bargaining_v0():
    rho = gbt.Rational(4, 5)

    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 5-6 Bargaining V0"
    )

    # Stage 1: Player 1 demands a share
    g.append_move(g.root, "Player 1", actions=["Quarter", "Half", "ThreeQuarters"])

    q1 = g.root.children["Quarter"]
    h1 = g.root.children["Half"]
    t1 = g.root.children["ThreeQuarters"]

    # Stage 1 responses by Player 2
    g.append_move(q1, "Player 2", actions=["Accept", "Reject"])
    g.append_move(h1, "Player 2", actions=["Accept", "Reject"])
    g.append_move(t1, "Player 2", actions=["Accept", "Reject"])

    # Reached stage 2 after rejection
    q1_r = q1.children["Reject"]
    h1_r = h1.children["Reject"]
    t1_r = t1.children["Reject"]

    # Stage 2: Player 2 offers a share to Player 1
    g.append_move(q1_r, "Player 2", actions=["Quarter", "Half", "ThreeQuarters"])
    g.append_move(h1_r, "Player 2", actions=["Quarter", "Half", "ThreeQuarters"])
    g.append_move(t1_r, "Player 2", actions=["Quarter", "Half", "ThreeQuarters"])

    # Player 1 responds in stage 2 after each offer
    stage2_offer_nodes = [
        ("Q_R_Q", q1_r.children["Quarter"]),
        ("Q_R_H", q1_r.children["Half"]),
        ("Q_R_T", q1_r.children["ThreeQuarters"]),
        ("H_R_Q", h1_r.children["Quarter"]),
        ("H_R_H", h1_r.children["Half"]),
        ("H_R_T", h1_r.children["ThreeQuarters"]),
        ("T_R_Q", t1_r.children["Quarter"]),
        ("T_R_H", t1_r.children["Half"]),
        ("T_R_T", t1_r.children["ThreeQuarters"]),
    ]

    for _, node in stage2_offer_nodes:
        g.append_move(node, "Player 1", actions=["Accept", "Reject"])

    # Distinct outcomes for every terminal history

    # Stage 1 accepted outcomes
    out_s1_q_a = g.add_outcome([gbt.Rational(1, 4), gbt.Rational(3, 4)], label="S1_Quarter_Accept")
    out_s1_h_a = g.add_outcome([gbt.Rational(1, 2), gbt.Rational(1, 2)], label="S1_Half_Accept")
    out_s1_t_a = g.add_outcome([gbt.Rational(3, 4), gbt.Rational(1, 4)], label="S1_ThreeQuarters_Accept")

    # Stage 2 accepted outcomes (discounted by rho = 4/5)
    # Quarter offer -> (1/5, 3/5)
    s2_q_p1 = rho * gbt.Rational(1, 4)
    s2_q_p2 = rho * gbt.Rational(3, 4)

    # Half offer -> (2/5, 2/5)
    s2_h_p1 = rho * gbt.Rational(1, 2)
    s2_h_p2 = rho * gbt.Rational(1, 2)

    # Three-quarters offer -> (3/5, 1/5)
    s2_t_p1 = rho * gbt.Rational(3, 4)
    s2_t_p2 = rho * gbt.Rational(1, 4)

    # Zero outcome after stage 2 rejection
    zero_p1 = gbt.Rational(0, 1)
    zero_p2 = gbt.Rational(0, 1)

    # Stage 2 distinct outcomes for every terminal node
    outcome_map = {}

    for prefix, _ in stage2_offer_nodes:
        if prefix.endswith("_Q"):
            outcome_map[f"{prefix}_A"] = g.add_outcome([s2_q_p1, s2_q_p2], label=f"{prefix}_Accept")
        elif prefix.endswith("_H"):
            outcome_map[f"{prefix}_A"] = g.add_outcome([s2_h_p1, s2_h_p2], label=f"{prefix}_Accept")
        else:
            outcome_map[f"{prefix}_A"] = g.add_outcome([s2_t_p1, s2_t_p2], label=f"{prefix}_Accept")

        outcome_map[f"{prefix}_R"] = g.add_outcome([zero_p1, zero_p2], label=f"{prefix}_Reject")

    # Assign stage 1 accepted outcomes
    g.set_outcome(q1.children["Accept"], out_s1_q_a)
    g.set_outcome(h1.children["Accept"], out_s1_h_a)
    g.set_outcome(t1.children["Accept"], out_s1_t_a)

    # Assign stage 2 outcomes
    for prefix, node in stage2_offer_nodes:
        g.set_outcome(node.children["Accept"], outcome_map[f"{prefix}_A"])
        g.set_outcome(node.children["Reject"], outcome_map[f"{prefix}_R"])

    return g


if __name__ == "__main__":
    g = build_fig5_fig6_bargaining_v0()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
