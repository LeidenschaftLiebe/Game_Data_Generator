from pathlib import Path
import pygambit as gbt


def build_exercise_386_2() -> gbt.Game:
    """Construct Page 386 Exercise 2."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Page 386 Exercise 2"
    )

    # Chance selects H or L with equal probability.
    g.append_move(g.root, g.players.chance, actions=["H", "L"])
    g.set_chance_probs(g.root.infoset, [0.5, 0.5])

    node_H = g.root.children["H"]
    node_L = g.root.children["L"]

    # Player 1 observes the state and chooses.
    g.append_move(node_H, player="1", actions=["A", "B"])
    g.append_move(node_L, player="1", actions=["A_prime", "B_prime"])

    node_HA = node_H.children["A"]
    node_HB = node_H.children["B"]
    node_LA = node_L.children["A_prime"]
    node_LB = node_L.children["B_prime"]

    # If Player 1 chooses B or B', Player 2 moves without knowing H or L.
    g.append_move(node_HB, player="2", actions=["X", "Y"])
    g.append_infoset(node_LB, node_HB.infoset)

    node_HBX = node_HB.children["X"]
    node_HBY = node_HB.children["Y"]
    node_LBX = node_LB.children["X"]
    node_LBY = node_LB.children["Y"]

    # Distinct outcomes.
    out_HA = g.add_outcome([4, 4], label="H_A")
    out_HBX = g.add_outcome([6, 4], label="H_B_X")
    out_HBY = g.add_outcome([0, 0], label="H_B_Y")

    out_LA = g.add_outcome([4, 2], label="L_Aprime")
    out_LBX = g.add_outcome([6, 0], label="L_Bprime_X")
    out_LBY = g.add_outcome([0, 6], label="L_Bprime_Y")

    # Attach outcomes.
    g.set_outcome(node_HA, out_HA)
    g.set_outcome(node_HBX, out_HBX)
    g.set_outcome(node_HBY, out_HBY)

    g.set_outcome(node_LA, out_LA)
    g.set_outcome(node_LBX, out_LBX)
    g.set_outcome(node_LBY, out_LBY)

    return g


if __name__ == "__main__":
    g = build_exercise_386_2()

    out_path = Path(__file__).with_name("exercise_386_2.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")