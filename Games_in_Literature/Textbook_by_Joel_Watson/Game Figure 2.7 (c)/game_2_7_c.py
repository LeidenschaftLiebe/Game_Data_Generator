from pathlib import Path
import pygambit as gbt


def build_price_competition_27c() -> gbt.Game:
    """Construct Watson Figure 2.7(c): sequential price competition with different payoffs."""
    # Create a two-player extensive-form tree.
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 2.7(c) - Price Competition"
    )

    # Player 1 chooses a high price or a low price.
    g.append_move(g.root, player="1", actions=["H", "L"])

    high_node = g.root.children["H"]
    low_node = g.root.children["L"]

    # If Player 1 chose H, Player 2 chooses at the top node.
    g.append_move(high_node, player="2", actions=["H", "L"])

    top_H = high_node.children["H"]
    top_L = high_node.children["L"]

    # If Player 1 chose L, Player 2 chooses at the bottom node.
    # Use H' and L' to match Watson's labels.
    g.append_move(low_node, player="2", actions=["H'", "L'"])

    bottom_H = low_node.children["H'"]
    bottom_L = low_node.children["L'"]

    # Terminal outcomes in the order (Player 1, Player 2), in millions.
    hh_outcome = g.add_outcome([10, 1], label="HH")
    hl_outcome = g.add_outcome([8, 2], label="HL")
    lh_outcome = g.add_outcome([11, 0], label="LH'")
    ll_outcome = g.add_outcome([9, 0.5], label="LL'")

    # Attach outcomes to the terminal nodes.
    g.set_outcome(top_H, hh_outcome)
    g.set_outcome(top_L, hl_outcome)
    g.set_outcome(bottom_H, lh_outcome)
    g.set_outcome(bottom_L, ll_outcome)

    return g


if __name__ == "__main__":
    g = build_price_competition_27c()

    # Save the .efg next to this script.
    out_path = Path(__file__).with_name("price_competition_2_7_c.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    