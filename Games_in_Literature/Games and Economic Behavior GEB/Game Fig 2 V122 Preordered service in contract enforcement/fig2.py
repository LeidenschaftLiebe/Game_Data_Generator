from pathlib import Path
import pygambit as gbt


def build_geb_exogenous_breach_fig2():
    g = gbt.Game.new_tree(
        players=["Investor", "Entrepreneur"],
        title="GEB Exogenous Breach Fig. 2"
    )

    # Parameter values for one concrete instance
    w = gbt.Rational("2")
    c = gbt.Rational("1/5")      # 0.2
    alpha = gbt.Rational("3/4")
    p = gbt.Rational("1/2")

    # Investor move
    g.append_move(g.root, player="Investor", actions=["NotEnter", "Enter"])
    node_not_enter = g.root.children["NotEnter"]
    node_enter = g.root.children["Enter"]

    out_not_enter = g.add_outcome([1, 1], label="NotEnter")
    g.set_outcome(node_not_enter, out_not_enter)

    # Nature after Enter
    g.append_move(node_enter, g.players.chance, actions=["BreachedExogenously", "NotBreached"])
    g.set_chance_probs(node_enter.infoset, [1 - alpha, alpha])

    node_breached = node_enter.children["BreachedExogenously"]
    node_not_breached = node_enter.children["NotBreached"]

    # Entrepreneur move after no exogenous breach
    g.append_move(node_not_breached, player="Entrepreneur", actions=["Honor", "NotHonor"])
    node_honor = node_not_breached.children["Honor"]
    node_not_honor = node_not_breached.children["NotHonor"]

    out_honor = g.add_outcome([w, w], label="Honor")
    g.set_outcome(node_honor, out_honor)

    # Judiciary after exogenous breach
    g.append_move(node_breached, g.players.chance, actions=["Enforce", "NotEnforce"])
    g.set_chance_probs(node_breached.infoset, [p, 1 - p])

    # Judiciary after chosen breach
    g.append_move(node_not_honor, g.players.chance, actions=["Enforce", "NotEnforce"])
    g.set_chance_probs(node_not_honor.infoset, [p, 1 - p])

    enforce_payoff = [w, w - c]
    not_enforce_payoff = [0, 2 * w]

    out_breach_enforce = g.add_outcome(enforce_payoff, label="Breached_Enforce")
    out_breach_not = g.add_outcome(not_enforce_payoff, label="Breached_NotEnforce")
    out_choice_enforce = g.add_outcome(enforce_payoff, label="NotHonor_Enforce")
    out_choice_not = g.add_outcome(not_enforce_payoff, label="NotHonor_NotEnforce")

    g.set_outcome(node_breached.children["Enforce"], out_breach_enforce)
    g.set_outcome(node_breached.children["NotEnforce"], out_breach_not)

    g.set_outcome(node_not_honor.children["Enforce"], out_choice_enforce)
    g.set_outcome(node_not_honor.children["NotEnforce"], out_choice_not)

    return g


if __name__ == "__main__":
    g = build_geb_exogenous_breach_fig2()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to {out_path}")

