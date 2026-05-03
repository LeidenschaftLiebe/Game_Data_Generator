from pathlib import Path
import pygambit as gbt


def build_rationalizability_priority_example():
    g = gbt.Game.new_tree(
        players=["Ann", "Bob"],
        title="GEB Rationalizability and Epistemic Priority Order Fig. 1"
    )

    # Ann moves first
    g.append_move(g.root, player="Ann", actions=["N", "B"])
    node_N = g.root.children["N"]
    node_B = g.root.children["B"]

    # If Ann chooses N, game ends
    out_N = g.add_outcome([0, 0], label="N")
    g.set_outcome(node_N, out_N)

    # If Ann chooses B, Bob chooses R or A
    g.append_move(node_B, player="Bob", actions=["R", "A"])
    node_BR = node_B.children["R"]
    node_BA = node_B.children["A"]

    # If Bob chooses R, game ends
    out_BR = g.add_outcome([-2, 0], label="B_R")
    g.set_outcome(node_BR, out_BR)

    # If Bob chooses A, Ann chooses P or I
    g.append_move(node_BA, player="Ann", actions=["P", "I"])
    node_BAP = node_BA.children["P"]
    node_BAI = node_BA.children["I"]

    out_BAP = g.add_outcome([-1, -3], label="B_A_P")
    out_BAI = g.add_outcome([1, 1], label="B_A_I")

    g.set_outcome(node_BAP, out_BAP)
    g.set_outcome(node_BAI, out_BAI)

    return g


if __name__ == "__main__":
    g = build_rationalizability_priority_example()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



