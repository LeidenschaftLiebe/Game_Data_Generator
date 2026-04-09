from pathlib import Path
import pygambit as gbt


def build_kreps_ramey_example_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 1 Kreps-Ramey Example V0"
    )

    # Nature chooses a or b
    g.append_move(g.root, g.players.chance, actions=["a", "b"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    a_root = g.root.children["a"]
    b_root = g.root.children["b"]

    # Early Player 1 choices
    g.append_move(a_root, "Player 1", actions=["Ea", "Ca"])
    g.append_move(b_root, "Player 1", actions=["Eb", "Cb"])

    # Make the two early Player 1 positions separate information sets by default
    # and keep handles for later reuse
    early_a = a_root
    early_b = b_root

    # Immediate exits
    out_a_ea = g.add_outcome([1, 0], label="a_Ea")
    out_b_eb = g.add_outcome([1, 0], label="b_Eb")
    g.set_outcome(early_a.children["Ea"], out_a_ea)
    g.set_outcome(early_b.children["Eb"], out_b_eb)

    # Player 2 after continuation
    p2_after_a = early_a.children["Ca"]
    p2_after_b = early_b.children["Cb"]

    g.append_move(p2_after_a, "Player 2", actions=["L", "R", "C2"])
    g.append_infoset(p2_after_b, p2_after_a.infoset)

    # Terminal outcomes at Player 2
    out_2a_L = g.add_outcome([0, 3], label="a_Ca_L")
    out_2a_R = g.add_outcome([3, 0], label="a_Ca_R")
    out_2b_R = g.add_outcome([0, 3], label="b_Cb_R")
    out_2b_L = g.add_outcome([3, 0], label="b_Cb_L")

    g.set_outcome(p2_after_a.children["L"], out_2a_L)
    g.set_outcome(p2_after_a.children["R"], out_2a_R)
    g.set_outcome(p2_after_b.children["R"], out_2b_R)
    g.set_outcome(p2_after_b.children["L"], out_2b_L)

    # Cross-over continuations after C2
    later_b = p2_after_a.children["C2"]   # from a branch, Player 1 returns in b-type situation
    later_a = p2_after_b.children["C2"]   # from b branch, Player 1 returns in a-type situation

    # Later positions share the same hidden situations as the earlier same-type choices
    g.append_infoset(later_b, early_b.infoset)
    g.append_infoset(later_a, early_a.infoset)

    # Outcomes after the later Player 1 choices
    out_later_b_eb = g.add_outcome([0, 2], label="later_b_Eb")
    out_later_b_cb = g.add_outcome([0, 2], label="later_b_Cb")
    out_later_a_ea = g.add_outcome([0, 2], label="later_a_Ea")
    out_later_a_ca = g.add_outcome([0, 2], label="later_a_Ca")

    g.set_outcome(later_b.children["Eb"], out_later_b_eb)
    g.set_outcome(later_b.children["Cb"], out_later_b_cb)
    g.set_outcome(later_a.children["Ea"], out_later_a_ea)
    g.set_outcome(later_a.children["Ca"], out_later_a_ca)

    return g


if __name__ == "__main__":
    game = build_kreps_ramey_example_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



