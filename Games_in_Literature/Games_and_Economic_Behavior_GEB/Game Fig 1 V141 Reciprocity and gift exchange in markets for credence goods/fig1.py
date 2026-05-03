from pathlib import Path
import pygambit as gbt


def build_geb_credence_goods_base() -> gbt.Game:
    """Construct Fig. 1 BASE treatment with instantiated prices."""
    g = gbt.Game.new_tree(
        players=["Expert", "Consumer"],
        title="GEB Credence Goods BASE Fig. 1"
    )

    # Fixed parameter values used for this dataset instance.
    p_h = 8
    p_l = 4
    c_h = 6
    c_l = 2
    h = gbt.Rational("1/2")
    outside = gbt.Rational("8/5")  # 1.6
    v = 10

    # Decision 1: expert posts the two prices.
    # In the paper these prices are chosen by the expert; here we instantiate p_l=4 and p_h=8.
    g.append_move(g.root, player="Expert", actions=["PostPrices"])

    node_post = g.root.children["PostPrices"]

    # Decision 2: consumer decides whether to interact.
    g.append_move(node_post, player="Consumer", actions=["out", "in"])

    node_out = node_post.children["out"]
    node_in = node_post.children["in"]

    out_out = g.add_outcome([outside, outside], label="out")
    g.set_outcome(node_out, out_out)

    # Nature determines whether the problem is high or low severity.
    g.append_move(node_in, player=g.players.chance, actions=["high", "low"])
    g.set_chance_probs(node_in.infoset, [h, 1 - h])

    node_high = node_in.children["high"]
    node_low = node_in.children["low"]

    # After diagnosis, the expert knows the severity and chooses the service.
    g.append_move(node_high, player="Expert", actions=["q_h", "q_l"])
    g.append_move(node_low, player="Expert", actions=["q_h", "q_l"])

    node_high_qh = node_high.children["q_h"]
    node_high_ql = node_high.children["q_l"]
    node_low_qh = node_low.children["q_h"]
    node_low_ql = node_low.children["q_l"]

    # Decision 4: after choosing the service, the expert chooses which posted price to charge.
    for node in [node_high_qh, node_high_ql, node_low_qh, node_low_ql]:
        g.append_move(node, player="Expert", actions=["p_h", "p_l"])

    # High severity, supply q_h.
    out_high_qh_ph = g.add_outcome([p_h - c_h, v - p_h], label="high_qh_ph")
    out_high_qh_pl = g.add_outcome([p_l - c_h, v - p_l], label="high_qh_pl")
    g.set_outcome(node_high_qh.children["p_h"], out_high_qh_ph)
    g.set_outcome(node_high_qh.children["p_l"], out_high_qh_pl)

    # High severity, supply q_l (problem not solved).
    out_high_ql_ph = g.add_outcome([p_h - c_l, -p_h], label="high_ql_ph")
    out_high_ql_pl = g.add_outcome([p_l - c_l, -p_l], label="high_ql_pl")
    g.set_outcome(node_high_ql.children["p_h"], out_high_ql_ph)
    g.set_outcome(node_high_ql.children["p_l"], out_high_ql_pl)

    # Low severity, supply q_h.
    out_low_qh_ph = g.add_outcome([p_h - c_h, v - p_h], label="low_qh_ph")
    out_low_qh_pl = g.add_outcome([p_l - c_h, v - p_l], label="low_qh_pl")
    g.set_outcome(node_low_qh.children["p_h"], out_low_qh_ph)
    g.set_outcome(node_low_qh.children["p_l"], out_low_qh_pl)

    # Low severity, supply q_l.
    out_low_ql_ph = g.add_outcome([p_h - c_l, v - p_h], label="low_ql_ph")
    out_low_ql_pl = g.add_outcome([p_l - c_l, v - p_l], label="low_ql_pl")
    g.set_outcome(node_low_ql.children["p_h"], out_low_ql_ph)
    g.set_outcome(node_low_ql.children["p_l"], out_low_ql_pl)

    return g


if __name__ == "__main__":
    g = build_geb_credence_goods_base()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")

