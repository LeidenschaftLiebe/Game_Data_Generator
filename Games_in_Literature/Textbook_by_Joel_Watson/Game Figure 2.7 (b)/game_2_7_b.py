from pathlib import Path
import pygambit as gbt


def build_price_competition_27b() -> gbt.Game:
    """Construct Watson Figure 2.7(b): simultaneous price competition."""
    # Create a two-player extensive-form tree.
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 2.7(b) - Price Competition"
    )

    # Player 1 chooses a high price or a low price.
    g.append_move(g.root, player="1", actions=["H", "L"])

    high_node = g.root.children["H"]
    low_node = g.root.children["L"]

    # Player 2 chooses without observing Player 1's choice.
    # Passing both nodes together creates one infoset shared by the two nodes.
    g.append_move(
        [high_node, low_node],
        player="2",
        actions=["H", "L"]
    )

    # Outcomes after Player 1 chose H.
    hh_node = high_node.children["H"]
    hl_node = high_node.children["L"]

    # Outcomes after Player 1 chose L.
    lh_node = low_node.children["H"]
    ll_node = low_node.children["L"]

    # Terminal outcomes in the order (Player 1, Player 2), in millions.
    hh_outcome = g.add_outcome([1, 1], label="HH")
    hl_outcome = g.add_outcome([0, 2], label="HL")
    lh_outcome = g.add_outcome([2, 0], label="LH")
    ll_outcome = g.add_outcome([0.5, 0.5], label="LL")

    # Attach outcomes to the terminal nodes.
    g.set_outcome(hh_node, hh_outcome)
    g.set_outcome(hl_node, hl_outcome)
    g.set_outcome(lh_node, lh_outcome)
    g.set_outcome(ll_node, ll_outcome)

    return g


if __name__ == "__main__":
    g = build_price_competition_27b()

    # Save the .efg next to this script.
    out_path = Path(__file__).with_name("price_competition_2_7_b.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    