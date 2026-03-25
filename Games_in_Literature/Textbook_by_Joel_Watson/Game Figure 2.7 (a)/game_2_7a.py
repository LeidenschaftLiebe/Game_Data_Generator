from pathlib import Path
import pygambit as gbt


def build_price_competition_27a() -> gbt.Game:
    """Construct Watson Figure 2.7(a): sequential price competition."""
    # Create a two-player extensive-form tree.
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 2.7(a) - Price Competition"
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
    # We use H' and L' to match Watson's labels.
    g.append_move(low_node, player="2", actions=["H'", "L'"])

    bottom_H = low_node.children["H'"]
    bottom_L = low_node.children["L'"]

    # Terminal outcomes in the order (Player 1, Player 2), in millions.
    HH = g.add_outcome([1, 1], label="HH")
    HL = g.add_outcome([0, 2], label="HL")
    LH = g.add_outcome([2, 0], label="LH'")
    LL = g.add_outcome([0.5, 0.5], label="LL'")

    # Attach outcomes to the terminal nodes.
    g.set_outcome(top_H, HH)
    g.set_outcome(top_L, HL)
    g.set_outcome(bottom_H, LH)
    g.set_outcome(bottom_L, LL)

    return g


if __name__ == "__main__":
    g = build_price_competition_27a()

    # Save the .efg next to this script.
    out_path = Path(__file__).with_name("price_competition_2_7_a.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    