from pathlib import Path
import pygambit as gbt


def build_hidden_state_game() -> gbt.Game:
    """Construct the hidden-state game shown in the image."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Hidden State Game"
    )

    # Chance selects the upper or lower state with equal probability.
    g.append_move(g.root, g.players.chance, actions=["Upper", "Lower"])
    g.set_chance_probs(g.root.infoset, [0.5, 0.5])

    upper_node = g.root.children["Upper"]
    lower_node = g.root.children["Lower"]

    # Player 1 observes the state and chooses L/R or L'/R'.
    g.append_move(upper_node, player="1", actions=["L", "R"])
    g.append_move(lower_node, player="1", actions=["L_prime", "R_prime"])

    upper_L = upper_node.children["L"]
    upper_R = upper_node.children["R"]
    lower_L = lower_node.children["L_prime"]
    lower_R = lower_node.children["R_prime"]

    # Player 2 chooses U or D without knowing whether the path came from upper or lower R-branch.
    g.append_move(upper_R, player="2", actions=["U", "D"])
    g.append_infoset(lower_R, upper_R.infoset)

    upper_RU = upper_R.children["U"]
    upper_RD = upper_R.children["D"]
    lower_RU = lower_R.children["U"]
    lower_RD = lower_R.children["D"]

    # One distinct outcome per terminal node.
    outcome_upper_L = g.add_outcome([2, 0], label="Upper_L")
    outcome_upper_RU = g.add_outcome([0, 4], label="Upper_R_U")
    outcome_upper_RD = g.add_outcome([4, 0], label="Upper_R_D")

    outcome_lower_L = g.add_outcome([2, 0], label="Lower_L")
    outcome_lower_RU = g.add_outcome([0, 0], label="Lower_R_U")
    outcome_lower_RD = g.add_outcome([4, 2], label="Lower_R_D")

    # Attach outcomes.
    g.set_outcome(upper_L, outcome_upper_L)
    g.set_outcome(upper_RU, outcome_upper_RU)
    g.set_outcome(upper_RD, outcome_upper_RD)

    g.set_outcome(lower_L, outcome_lower_L)
    g.set_outcome(lower_RU, outcome_lower_RU)
    g.set_outcome(lower_RD, outcome_lower_RD)

    return g


if __name__ == "__main__":
    g = build_hidden_state_game()

    out_path = Path(__file__).with_name("game_page333_exercise3.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")