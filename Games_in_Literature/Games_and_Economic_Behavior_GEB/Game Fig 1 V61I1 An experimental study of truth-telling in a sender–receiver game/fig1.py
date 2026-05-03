from pathlib import Path
import pygambit as gbt


def build_benchmark_game_v0():
    g = gbt.Game.new_tree(
        players=["Sender", "Receiver"],
        title="GEB Fig. 1 Benchmark Game V0"
    )

    # Use the article's main benchmark parameter
    x = 2

    # Chance chooses the true payoff table
    g.append_move(g.root, g.players.chance, actions=["A", "B"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    state_a = g.root.children["A"]
    state_b = g.root.children["B"]

    # Sender observes the state and sends message A or B
    g.append_move(state_a, "Sender", actions=["A", "B"])
    g.append_move(state_b, "Sender", actions=["A", "B"])

    a_msg_a = state_a.children["A"]
    a_msg_b = state_a.children["B"]
    b_msg_a = state_b.children["A"]
    b_msg_b = state_b.children["B"]

    # Receiver moves after message A, without observing the true state
    g.append_move(a_msg_a, "Receiver", actions=["U", "D"])
    recv_A_infoset = a_msg_a.infoset
    g.append_infoset(b_msg_a, recv_A_infoset)

    # Receiver moves after message B, without observing the true state
    g.append_move(a_msg_b, "Receiver", actions=["U", "D"])
    recv_B_infoset = a_msg_b.infoset
    g.append_infoset(b_msg_b, recv_B_infoset)

    # Distinct outcomes for each terminal history
    out_A_A_U = g.add_outcome([x, 1], label="stateA_msgA_U")
    out_A_A_D = g.add_outcome([1, x], label="stateA_msgA_D")

    out_A_B_U = g.add_outcome([x, 1], label="stateA_msgB_U")
    out_A_B_D = g.add_outcome([1, x], label="stateA_msgB_D")

    out_B_A_U = g.add_outcome([1, x], label="stateB_msgA_U")
    out_B_A_D = g.add_outcome([x, 1], label="stateB_msgA_D")

    out_B_B_U = g.add_outcome([1, x], label="stateB_msgB_U")
    out_B_B_D = g.add_outcome([x, 1], label="stateB_msgB_D")

    # Assign outcomes
    g.set_outcome(a_msg_a.children["U"], out_A_A_U)
    g.set_outcome(a_msg_a.children["D"], out_A_A_D)

    g.set_outcome(a_msg_b.children["U"], out_A_B_U)
    g.set_outcome(a_msg_b.children["D"], out_A_B_D)

    g.set_outcome(b_msg_a.children["U"], out_B_A_U)
    g.set_outcome(b_msg_a.children["D"], out_B_A_D)

    g.set_outcome(b_msg_b.children["U"], out_B_B_U)
    g.set_outcome(b_msg_b.children["D"], out_B_B_D)

    return g


if __name__ == "__main__":
    game = build_benchmark_game_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

