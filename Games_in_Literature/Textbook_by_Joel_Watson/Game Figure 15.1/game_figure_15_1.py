from pathlib import Path
import pygambit as gbt


def build_figure_15_1() -> gbt.Game:
    """Construct Watson Figure 15.1: entry and predation."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 15.1 - Entry and Predation"
    )

    # Player 1 first chooses whether to stay out or enter.
    g.append_move(g.root, player="1", actions=["Out", "In"])

    node_out = g.root.children["Out"]
    node_in = g.root.children["In"]

    # If Player 1 enters, Player 2 chooses whether to accommodate or start a price war.
    g.append_move(node_in, player="2", actions=["Accommodate", "Price war"])

    node_accommodate = node_in.children["Accommodate"]
    node_price_war = node_in.children["Price war"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_out = g.add_outcome([0, 4], label="Out")
    outcome_accommodate = g.add_outcome([2, 2], label="Accommodate")
    outcome_price_war = g.add_outcome([-1, -1], label="Price war")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_out, outcome_out)
    g.set_outcome(node_accommodate, outcome_accommodate)
    g.set_outcome(node_price_war, outcome_price_war)

    return g


if __name__ == "__main__":
    g = build_figure_15_1()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("figure_15_1.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    