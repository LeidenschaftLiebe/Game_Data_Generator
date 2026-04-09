from pathlib import Path
import pygambit as gbt


def build_strategic_knowledge_sharing_example1_v0():
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Strategic Knowledge Sharing Example 1 V0"
    )

    # Nature chooses the state with equal probability
    g.append_move(g.root, g.players.chance, actions=["omega1", "omega2"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    state_omega1 = g.root.children["omega1"]
    state_omega2 = g.root.children["omega2"]

    # Player 1 observes the state and sends a truthful public message
    g.append_move(state_omega1, "1", actions=["{omega1}", "Omega"])
    g.append_move(state_omega2, "1", actions=["{omega2}", "Omega"])

    # Player 2 after exact revelation of omega1
    g.append_move(state_omega1.children["{omega1}"], "2", actions=["A", "B", "C", "D"])

    # Player 2 after exact revelation of omega2
    g.append_move(state_omega2.children["{omega2}"], "2", actions=["A", "B", "C", "D"])

    # Player 2 after message Omega from either state: same information set
    g.append_move(state_omega1.children["Omega"], "2", actions=["A", "B", "C", "D"])
    omega_infoset = state_omega1.children["Omega"].infoset
    g.append_infoset(state_omega2.children["Omega"], omega_infoset)

    # Distinct outcomes under state omega1 after message {omega1}
    out_omega1_reveal_A = g.add_outcome([0, 6], label="omega1_reveal_choose_A")
    out_omega1_reveal_B = g.add_outcome([1, 5], label="omega1_reveal_choose_B")
    out_omega1_reveal_C = g.add_outcome([-2, 0], label="omega1_reveal_choose_C")
    out_omega1_reveal_D = g.add_outcome([1, -6], label="omega1_reveal_choose_D")

    # Distinct outcomes under state omega2 after message {omega2}
    out_omega2_reveal_A = g.add_outcome([1, -6], label="omega2_reveal_choose_A")
    out_omega2_reveal_B = g.add_outcome([1, 1], label="omega2_reveal_choose_B")
    out_omega2_reveal_C = g.add_outcome([-2, 2], label="omega2_reveal_choose_C")
    out_omega2_reveal_D = g.add_outcome([0, 3], label="omega2_reveal_choose_D")

    # Distinct outcomes under state omega1 after message Omega
    out_omega1_Omega_A = g.add_outcome([0, 6], label="omega1_Omega_choose_A")
    out_omega1_Omega_B = g.add_outcome([1, 5], label="omega1_Omega_choose_B")
    out_omega1_Omega_C = g.add_outcome([-2, 0], label="omega1_Omega_choose_C")
    out_omega1_Omega_D = g.add_outcome([1, -6], label="omega1_Omega_choose_D")

    # Distinct outcomes under state omega2 after message Omega
    out_omega2_Omega_A = g.add_outcome([1, -6], label="omega2_Omega_choose_A")
    out_omega2_Omega_B = g.add_outcome([1, 1], label="omega2_Omega_choose_B")
    out_omega2_Omega_C = g.add_outcome([-2, 2], label="omega2_Omega_choose_C")
    out_omega2_Omega_D = g.add_outcome([0, 3], label="omega2_Omega_choose_D")

    # Assign outcomes after message {omega1}
    p2_after_omega1_reveal = state_omega1.children["{omega1}"]
    g.set_outcome(p2_after_omega1_reveal.children["A"], out_omega1_reveal_A)
    g.set_outcome(p2_after_omega1_reveal.children["B"], out_omega1_reveal_B)
    g.set_outcome(p2_after_omega1_reveal.children["C"], out_omega1_reveal_C)
    g.set_outcome(p2_after_omega1_reveal.children["D"], out_omega1_reveal_D)

    # Assign outcomes after message {omega2}
    p2_after_omega2_reveal = state_omega2.children["{omega2}"]
    g.set_outcome(p2_after_omega2_reveal.children["A"], out_omega2_reveal_A)
    g.set_outcome(p2_after_omega2_reveal.children["B"], out_omega2_reveal_B)
    g.set_outcome(p2_after_omega2_reveal.children["C"], out_omega2_reveal_C)
    g.set_outcome(p2_after_omega2_reveal.children["D"], out_omega2_reveal_D)

    # Assign outcomes after message Omega in state omega1
    p2_after_omega1_Omega = state_omega1.children["Omega"]
    g.set_outcome(p2_after_omega1_Omega.children["A"], out_omega1_Omega_A)
    g.set_outcome(p2_after_omega1_Omega.children["B"], out_omega1_Omega_B)
    g.set_outcome(p2_after_omega1_Omega.children["C"], out_omega1_Omega_C)
    g.set_outcome(p2_after_omega1_Omega.children["D"], out_omega1_Omega_D)

    # Assign outcomes after message Omega in state omega2
    p2_after_omega2_Omega = state_omega2.children["Omega"]
    g.set_outcome(p2_after_omega2_Omega.children["A"], out_omega2_Omega_A)
    g.set_outcome(p2_after_omega2_Omega.children["B"], out_omega2_Omega_B)
    g.set_outcome(p2_after_omega2_Omega.children["C"], out_omega2_Omega_C)
    g.set_outcome(p2_after_omega2_Omega.children["D"], out_omega2_Omega_D)

    return g


if __name__ == "__main__":
    game = build_strategic_knowledge_sharing_example1_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

    