from pathlib import Path
import pygambit as gbt


def build_fig3_procedural_reasoning_v0():
    g = gbt.Game.new_tree(
        players=["Alice", "Bob", "Emma"],
        title="GEB Fig. 3 Procedural Reasoning Order V0"
    )

    # Alice moves first
    g.append_move(g.root, "Alice", actions=["l", "m", "r"])

    alice_l = g.root.children["l"]
    alice_m = g.root.children["m"]
    alice_r = g.root.children["r"]

    # Bob moves after m
    g.append_move(alice_m, "Bob", actions=["L", "R"])
    bob_after_m = alice_m

    # Bob also moves after r, in the same information set as after m
    g.append_infoset(alice_r, bob_after_m.infoset)
    bob_after_r = alice_r

    # Emma moves after l
    g.append_move(alice_l, "Emma", actions=["p", "q"])
    emma_after_l = alice_l

    # Emma also moves after m then L, in the same information set as after l
    g.append_infoset(bob_after_m.children["L"], emma_after_l.infoset)
    emma_after_mL = bob_after_m.children["L"]

    # Outcomes after Emma
    out_l_p = g.add_outcome([0, 2, 0], label="l_p")
    out_l_q = g.add_outcome([0, 2, 0], label="l_q")
    out_mL_p = g.add_outcome([2, 0, 0], label="m_L_p")
    out_mL_q = g.add_outcome([2, 0, 0], label="m_L_q")

    g.set_outcome(emma_after_l.children["p"], out_l_p)
    g.set_outcome(emma_after_l.children["q"], out_l_q)
    g.set_outcome(emma_after_mL.children["p"], out_mL_p)
    g.set_outcome(emma_after_mL.children["q"], out_mL_q)

    # Outcomes after Bob
    out_m_R = g.add_outcome([1, 1, 0], label="m_R")
    out_r_L = g.add_outcome([-1, -1, 0], label="r_L")
    out_r_R = g.add_outcome([-1, 0, 0], label="r_R")

    g.set_outcome(bob_after_m.children["R"], out_m_R)
    g.set_outcome(bob_after_r.children["L"], out_r_L)
    g.set_outcome(bob_after_r.children["R"], out_r_R)

    return g


if __name__ == "__main__":
    game = build_fig3_procedural_reasoning_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")




    