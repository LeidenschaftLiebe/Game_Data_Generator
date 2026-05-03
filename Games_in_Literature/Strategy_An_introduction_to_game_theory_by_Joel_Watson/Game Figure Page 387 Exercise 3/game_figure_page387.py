from pathlib import Path
import pygambit as gbt


def build_exercise_387_3() -> gbt.Game:
    """Construct Page 387 Exercise 3."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Page 387 Exercise 3"
    )

    # Chance selects H or L with equal probability.
    g.append_move(g.root, g.players.chance, actions=["H", "L"])
    g.set_chance_probs(g.root.infoset, [0.5, 0.5])

    node_H = g.root.children["H"]
    node_L = g.root.children["L"]

    # Player 1 observes the state and chooses.
    g.append_move(node_H, player="1", actions=["L", "R"])
    g.append_move(node_L, player="1", actions=["L_prime", "R_prime"])

    node_HL = node_H.children["L"]
    node_HR = node_H.children["R"]
    node_LL = node_L.children["L_prime"]
    node_LR = node_L.children["R_prime"]

    # Player 2 moves after R or R' without knowing H or L.
    g.append_move(node_HR, player="2", actions=["U", "D"])
    g.append_infoset(node_LR, node_HR.infoset)

    node_HRU = node_HR.children["U"]
    node_HRD = node_HR.children["D"]
    node_LRU = node_LR.children["U"]
    node_LRD = node_LR.children["D"]

    # Distinct outcomes.
    out_HL = g.add_outcome([2, 0], label="H_L")
    out_HRU = g.add_outcome([3, 2], label="H_R_U")
    out_HRD = g.add_outcome([1, 0], label="H_R_D")

    out_LL = g.add_outcome([2, 0], label="L_Lprime")
    out_LRU = g.add_outcome([1, 0], label="L_Rprime_U")
    out_LRD = g.add_outcome([1, 1], label="L_Rprime_D")

    # Attach outcomes.
    g.set_outcome(node_HL, out_HL)
    g.set_outcome(node_HRU, out_HRU)
    g.set_outcome(node_HRD, out_HRD)

    g.set_outcome(node_LL, out_LL)
    g.set_outcome(node_LRU, out_LRU)
    g.set_outcome(node_LRD, out_LRD)

    return g


if __name__ == "__main__":
    g = build_exercise_387_3()

    out_path = Path(__file__).with_name("game_figure_page387.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")