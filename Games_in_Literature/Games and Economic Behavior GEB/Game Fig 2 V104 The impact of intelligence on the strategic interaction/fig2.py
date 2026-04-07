from pathlib import Path
import pygambit as gbt


def build_fig22_v0():
    # Parameter values chosen to satisfy the article's restrictions:
    # 0 < r1 < w1 < 1
    # 0 < cL < w1 - r1 < cH
    # 0 < r2 < w2 < 1
    beta = gbt.Rational(2, 5)   # 0.4, so Pr(L)=0.6 and Pr(H)=0.4
    w1 = 0.6
    r1 = 0.2
    cL = 0.1
    cH = 0.5
    w2 = 0.8
    r2 = 0.3

    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 2.2 Inspections V0"
    )

    # Nature chooses Player 1's type
    g.append_move(g.root, g.players.chance, actions=["L", "H"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(3, 5), beta])

    low = g.root.children["L"]
    high = g.root.children["H"]

    # Player 1 moves after type is known
    g.append_move(low, "Player 1", actions=["NBO", "NB", "B"])
    g.append_move(high, "Player 1", actions=["NBO", "NB", "B"])

    low_nbo = low.children["NBO"]
    low_nb = low.children["NB"]
    low_b = low.children["B"]

    high_nbo = high.children["NBO"]
    high_nb = high.children["NB"]
    high_b = high.children["B"]

    # Player 2 moves after any non-opening choice, in one shared information set
    g.append_move(low_nb, "Player 2", actions=["NA", "A"])
    shared_infoset = low_nb.infoset
    g.append_infoset(low_b, shared_infoset)
    g.append_infoset(high_nb, shared_infoset)
    g.append_infoset(high_b, shared_infoset)

    # Distinct outcomes for every terminal history

    # L branch
    out_l_nbo = g.add_outcome([w1 - cL, 1.0], label="L_NBO")
    out_l_nb_na = g.add_outcome([w1, 1.0], label="L_NB_NA")
    out_l_nb_a = g.add_outcome([r1, r2], label="L_NB_A")
    out_l_b_na = g.add_outcome([1.0, 0.0], label="L_B_NA")
    out_l_b_a = g.add_outcome([0.0, w2], label="L_B_A")

    # H branch
    out_h_nbo = g.add_outcome([w1 - cH, 1.0], label="H_NBO")
    out_h_nb_na = g.add_outcome([w1, 1.0], label="H_NB_NA")
    out_h_nb_a = g.add_outcome([r1, r2], label="H_NB_A")
    out_h_b_na = g.add_outcome([1.0, 0.0], label="H_B_NA")
    out_h_b_a = g.add_outcome([0.0, w2], label="H_B_A")

    # Assign outcomes
    g.set_outcome(low_nbo, out_l_nbo)
    g.set_outcome(low_nb.children["NA"], out_l_nb_na)
    g.set_outcome(low_nb.children["A"], out_l_nb_a)
    g.set_outcome(low_b.children["NA"], out_l_b_na)
    g.set_outcome(low_b.children["A"], out_l_b_a)

    g.set_outcome(high_nbo, out_h_nbo)
    g.set_outcome(high_nb.children["NA"], out_h_nb_na)
    g.set_outcome(high_nb.children["A"], out_h_nb_a)
    g.set_outcome(high_b.children["NA"], out_h_b_na)
    g.set_outcome(high_b.children["A"], out_h_b_a)

    return g


if __name__ == "__main__":
    g = build_fig22_v0()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


