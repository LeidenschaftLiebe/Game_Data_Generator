from pathlib import Path
import pygambit as gbt


def build_fig1_v0(p_num=1, p_den=4):
    g = gbt.Game.new_tree(
        players=["Sender", "Receiver"],
        title="GEB Fig. 1 Signaling Game V0"
    )

    # Nature chooses the sender's type
    g.append_move(g.root, g.players.chance, actions=["t1", "t2"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(p_num, p_den), 1 - gbt.Rational(p_num, p_den)])

    t1_node = g.root.children["t1"]
    t2_node = g.root.children["t2"]

    # Sender moves after each type
    g.append_move(t1_node, "Sender", actions=["m1", "m2"])
    g.append_move(t2_node, "Sender", actions=["m1", "m2"])

    t1_m1 = t1_node.children["m1"]
    t1_m2 = t1_node.children["m2"]
    t2_m1 = t2_node.children["m1"]
    t2_m2 = t2_node.children["m2"]

    # Receiver after m1: same infoset across t1 and t2
    g.append_move(t1_m1, "Receiver", actions=["a1", "a2"])
    recv_m1_infoset = t1_m1.infoset
    g.append_infoset(t2_m1, recv_m1_infoset)

    # Receiver after m2: same infoset across t1 and t2
    g.append_move(t1_m2, "Receiver", actions=["a1", "a2"])
    recv_m2_infoset = t1_m2.infoset
    g.append_infoset(t2_m2, recv_m2_infoset)

    # Distinct outcomes for every terminal history
    out_t1_m1_a1 = g.add_outcome([15, 10], label="t1_m1_a1")
    out_t1_m1_a2 = g.add_outcome([80, 80], label="t1_m1_a2")
    out_t1_m2_a1 = g.add_outcome([25, 10], label="t1_m2_a1")
    out_t1_m2_a2 = g.add_outcome([50, 50], label="t1_m2_a2")

    out_t2_m1_a1 = g.add_outcome([80, 80], label="t2_m1_a1")
    out_t2_m1_a2 = g.add_outcome([15, 30], label="t2_m1_a2")
    out_t2_m2_a1 = g.add_outcome([50, 50], label="t2_m2_a1")
    out_t2_m2_a2 = g.add_outcome([25, 30], label="t2_m2_a2")

    # Assign outcomes
    g.set_outcome(t1_m1.children["a1"], out_t1_m1_a1)
    g.set_outcome(t1_m1.children["a2"], out_t1_m1_a2)
    g.set_outcome(t1_m2.children["a1"], out_t1_m2_a1)
    g.set_outcome(t1_m2.children["a2"], out_t1_m2_a2)

    g.set_outcome(t2_m1.children["a1"], out_t2_m1_a1)
    g.set_outcome(t2_m1.children["a2"], out_t2_m1_a2)
    g.set_outcome(t2_m2.children["a1"], out_t2_m2_a1)
    g.set_outcome(t2_m2.children["a2"], out_t2_m2_a2)

    return g


if __name__ == "__main__":
    game = build_fig1_v0(p_num=1, p_den=4)
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")