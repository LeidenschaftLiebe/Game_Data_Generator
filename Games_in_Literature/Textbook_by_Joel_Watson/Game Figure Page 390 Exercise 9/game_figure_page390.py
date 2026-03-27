from pathlib import Path
import pygambit as gbt


def build_hidden_state_2_3_game() -> gbt.Game:
    """Construct the hidden-state game with probabilities 2/3 and 1/3."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Hidden State Game with 2/3 and 1/3"
    )

    # Chance selects H or L.
    g.append_move(g.root, g.players.chance, actions=["H", "L"])

    # Use exact rational probabilities to avoid the 2/3, 1/3 float-sum issue.
    g.set_chance_probs(
        g.root.infoset,
        [gbt.Rational("2/3"), gbt.Rational("1/3")]
    )

    node_H = g.root.children["H"]
    node_L = g.root.children["L"]

    # Player 1 observes the state and chooses.
    g.append_move(node_H, player="1", actions=["X", "Y"])
    g.append_move(node_L, player="1", actions=["X_prime", "Y_prime"])

    node_HX = node_H.children["X"]
    node_HY = node_H.children["Y"]
    node_LX = node_L.children["X_prime"]
    node_LY = node_L.children["Y_prime"]

    # Player 2 moves after Y or Y' without knowing H or L.
    g.append_move(node_HY, player="2", actions=["L", "M"])
    g.append_infoset(node_LY, node_HY.infoset)

    node_HYL = node_HY.children["L"]
    node_HYM = node_HY.children["M"]
    node_LYL = node_LY.children["L"]
    node_LYM = node_LY.children["M"]

    # Distinct outcomes.
    out_HX = g.add_outcome([3, 0], label="H_X")
    out_HYL = g.add_outcome([0, 6], label="H_Y_L")
    out_HYM = g.add_outcome([6, 0], label="H_Y_M")

    out_LX = g.add_outcome([0, 0], label="L_Xprime")
    out_LYL = g.add_outcome([3, 0], label="L_Yprime_L")
    out_LYM = g.add_outcome([3, 6], label="L_Yprime_M")

    # Attach outcomes.
    g.set_outcome(node_HX, out_HX)
    g.set_outcome(node_HYL, out_HYL)
    g.set_outcome(node_HYM, out_HYM)

    g.set_outcome(node_LX, out_LX)
    g.set_outcome(node_LYL, out_LYL)
    g.set_outcome(node_LYM, out_LYM)

    return g


if __name__ == "__main__":
    g = build_hidden_state_2_3_game()

    out_path = Path(__file__).with_name("game_figure_page390.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")

