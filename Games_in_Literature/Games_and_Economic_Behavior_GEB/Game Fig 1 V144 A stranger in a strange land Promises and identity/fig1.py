from pathlib import Path
import pygambit as gbt


def build_geb_random_dictator_fig1() -> gbt.Game:
    """Construct Fig. 1 random-dictator game from the article."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Random Dictator Fig. 1"
    )

    # Chance first selects which player becomes the decision-maker.
    g.append_move(g.root, player=g.players.chance, actions=["Player1Selected", "Player2Selected"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational("1/2"), gbt.Rational("1/2")])

    node_p1 = g.root.children["Player1Selected"]
    node_p2 = g.root.children["Player2Selected"]

    # If Player 1 is selected, Player 1 chooses whether to roll.
    g.append_move(node_p1, player="Player 1", actions=["Don't Roll", "Roll"])

    node_p1_dont = node_p1.children["Don't Roll"]
    node_p1_roll = node_p1.children["Roll"]

    out_p1_dont = g.add_outcome([14, 0], label="P1_DontRoll")
    g.set_outcome(node_p1_dont, out_p1_dont)

    g.append_move(node_p1_roll, player=g.players.chance, actions=["OneSixth", "FiveSixths"])
    g.set_chance_probs(node_p1_roll.infoset, [gbt.Rational("1/6"), gbt.Rational("5/6")])

    out_p1_roll_bad = g.add_outcome([10, 0], label="P1_Roll_OneSixth")
    out_p1_roll_good = g.add_outcome([10, 12], label="P1_Roll_FiveSixths")

    g.set_outcome(node_p1_roll.children["OneSixth"], out_p1_roll_bad)
    g.set_outcome(node_p1_roll.children["FiveSixths"], out_p1_roll_good)

    # If Player 2 is selected, Player 2 chooses whether to roll.
    g.append_move(node_p2, player="Player 2", actions=["Don't Roll", "Roll"])

    node_p2_dont = node_p2.children["Don't Roll"]
    node_p2_roll = node_p2.children["Roll"]

    out_p2_dont = g.add_outcome([0, 14], label="P2_DontRoll")
    g.set_outcome(node_p2_dont, out_p2_dont)

    g.append_move(node_p2_roll, player=g.players.chance, actions=["OneSixth", "FiveSixths"])
    g.set_chance_probs(node_p2_roll.infoset, [gbt.Rational("1/6"), gbt.Rational("5/6")])

    out_p2_roll_bad = g.add_outcome([0, 10], label="P2_Roll_OneSixth")
    out_p2_roll_good = g.add_outcome([12, 10], label="P2_Roll_FiveSixths")

    g.set_outcome(node_p2_roll.children["OneSixth"], out_p2_roll_bad)
    g.set_outcome(node_p2_roll.children["FiveSixths"], out_p2_roll_good)

    return g


if __name__ == "__main__":
    g = build_geb_random_dictator_fig1()

    out_path = Path(__file__).with_name("game_fig1_v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")

