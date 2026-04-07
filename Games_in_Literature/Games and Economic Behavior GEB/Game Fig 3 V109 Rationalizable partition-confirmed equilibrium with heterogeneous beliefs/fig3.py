from pathlib import Path
import pygambit as gbt


def build_tax_return_v0():
    g = gbt.Game.new_tree(
        players=["Tax Attorney", "IRS Agent", "Tax Evader"],
        title="GEB Fig. 3 Tax Return V0"
    )

    # Nature moves first
    g.append_move(g.root, g.players.chance, actions=["Good", "Bad"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    good = g.root.children["Good"]
    bad = g.root.children["Bad"]

    # IRS agent after Good
    g.append_move(good, "IRS Agent", actions=["N", "E"])
    good_n = good.children["N"]
    good_e = good.children["E"]

    # Tax attorney after Bad
    g.append_move(bad, "Tax Attorney", actions=["Risky", "Safe"])
    bad_risky = bad.children["Risky"]
    bad_safe = bad.children["Safe"]

    # IRS agent after Bad-Risky; same infoset as after Good
    g.append_infoset(bad_risky, good.infoset)
    bad_risky_n = bad_risky.children["N"]
    bad_risky_e = bad_risky.children["E"]

    # Tax evader after Bad-Safe
    g.append_move(bad_safe, "Tax Evader", actions=["Stay", "Fire"])
    safe_stay = bad_safe.children["Stay"]
    safe_fire = bad_safe.children["Fire"]

    # Outcomes
    out_good_n = g.add_outcome([0, 1, 0], label="Good_N")
    out_good_e = g.add_outcome([0, 0, 0], label="Good_E")
    out_bad_risky_n = g.add_outcome([2, 0, 0], label="Bad_Risky_N")
    out_bad_risky_e = g.add_outcome([0, 2, 0], label="Bad_Risky_E")
    out_bad_safe_stay = g.add_outcome([1, 0, 0], label="Bad_Safe_Stay")
    out_bad_safe_fire = g.add_outcome([-1, 0, 0], label="Bad_Safe_Fire")

    # Assign outcomes
    g.set_outcome(good_n, out_good_n)
    g.set_outcome(good_e, out_good_e)
    g.set_outcome(bad_risky_n, out_bad_risky_n)
    g.set_outcome(bad_risky_e, out_bad_risky_e)
    g.set_outcome(safe_stay, out_bad_safe_stay)
    g.set_outcome(safe_fire, out_bad_safe_fire)

    return g


if __name__ == "__main__":
    g = build_tax_return_v0()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")




