from pathlib import Path
import pygambit as gbt


def build_reciprocity_v0():
    g = gbt.Game.new_tree(
        players=["Player A", "Player B"],
        title="GEB Fig. 2 Reciprocity V0"
    )

    # Player A moves first
    g.append_move(g.root, "Player A", actions=["S", "H"])
    s_node = g.root.children["S"]
    h_node = g.root.children["H"]

    # Use Experiment 2, Treatment 2 values from the article:
    # p = 0.01, q = 0.01, so branch 2 has probability 0.98
    probs = [gbt.Rational(1, 100), gbt.Rational(98, 100), gbt.Rational(1, 100)]

    # Nature after S
    g.append_move(s_node, g.players.chance, actions=["1", "2", "3"])
    g.set_chance_probs(s_node.infoset, probs)

    s_1 = s_node.children["1"]
    s_2 = s_node.children["2"]
    s_3 = s_node.children["3"]

    # Nature after H
    g.append_move(h_node, g.players.chance, actions=["1", "2", "3"])
    g.set_chance_probs(h_node.infoset, probs)

    h_1 = h_node.children["1"]
    h_2 = h_node.children["2"]
    h_3 = h_node.children["3"]

    # Player B after S -> 1
    g.append_move(s_1, "Player B", actions=["N", "P"])

    # Player B after H -> 3
    g.append_move(h_3, "Player B", actions=["N", "R"])

    # Outcomes
    out_s_1_n = g.add_outcome([4.5, 2.5], label="S_1_N")
    out_s_1_p = g.add_outcome([3.0, 2.0], label="S_1_P")
    out_s_2 = g.add_outcome([4.5, 2.5], label="S_2")
    out_s_3 = g.add_outcome([4.5, 2.5], label="S_3")

    out_h_1 = g.add_outcome([4.0, 4.0], label="H_1")
    out_h_2 = g.add_outcome([4.0, 4.0], label="H_2")
    out_h_3_n = g.add_outcome([4.0, 4.0], label="H_3_N")
    out_h_3_r = g.add_outcome([5.5, 3.5], label="H_3_R")

    # Assign outcomes
    g.set_outcome(s_1.children["N"], out_s_1_n)
    g.set_outcome(s_1.children["P"], out_s_1_p)
    g.set_outcome(s_2, out_s_2)
    g.set_outcome(s_3, out_s_3)

    g.set_outcome(h_1, out_h_1)
    g.set_outcome(h_2, out_h_2)
    g.set_outcome(h_3.children["N"], out_h_3_n)
    g.set_outcome(h_3.children["R"], out_h_3_r)

    return g


if __name__ == "__main__":
    g = build_reciprocity_v0()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
