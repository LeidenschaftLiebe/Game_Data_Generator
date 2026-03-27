from pathlib import Path
import pygambit as gbt


def build_market_signaling_game(q: float = 0.5) -> gbt.Game:
    """Construct the guided-exercise market signaling game."""
    if not (0.0 <= q <= 1.0):
        raise ValueError("q must be between 0 and 1")

    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Guided Exercise - Incumbent and Entrant"
    )

    # Chance selects the incumbent's cost type.
    g.append_move(g.root, g.players.chance, actions=["HighCost", "LowCost"])
    g.set_chance_probs(g.root.infoset, [q, 1 - q])

    high_node = g.root.children["HighCost"]
    low_node = g.root.children["LowCost"]

    # Player 1 (the incumbent) observes its type and chooses between two price options.
    g.append_move(high_node, player="1", actions=["Price1_H", "Price2_H"])
    g.append_move(low_node, player="1", actions=["Price1_L", "Price2_L"])

    high_price1 = high_node.children["Price1_H"]
    high_price2 = high_node.children["Price2_H"]
    low_price1 = low_node.children["Price1_L"]
    low_price2 = low_node.children["Price2_L"]

    # Player 2 (the entrant) sees the price option but not the incumbent's type.
    # One information set after observing price option 1.
    g.append_move(high_price1, player="2", actions=["Enter", "StayOut"])
    g.append_infoset(low_price1, high_price1.infoset)

    # One information set after observing price option 2.
    g.append_move(high_price2, player="2", actions=["Enter", "StayOut"])
    g.append_infoset(low_price2, high_price2.infoset)

    # Terminal nodes after price option 1.
    h1_enter = high_price1.children["Enter"]
    h1_out = high_price1.children["StayOut"]
    l1_enter = low_price1.children["Enter"]
    l1_out = low_price1.children["StayOut"]

    # Terminal nodes after price option 2.
    h2_enter = high_price2.children["Enter"]
    h2_out = high_price2.children["StayOut"]
    l2_enter = low_price2.children["Enter"]
    l2_out = low_price2.children["StayOut"]

    # Create one distinct outcome per terminal node.
    # Payoffs are in the order: (incumbent, entrant).
    out_h1_enter = g.add_outcome([0, 1], label="HighCost_Price1_Enter")
    out_h1_out = g.add_outcome([0, 0], label="HighCost_Price1_StayOut")

    out_h2_enter = g.add_outcome([0, 1], label="HighCost_Price2_Enter")
    out_h2_out = g.add_outcome([2, 0], label="HighCost_Price2_StayOut")

    out_l1_enter = g.add_outcome([0, -1], label="LowCost_Price1_Enter")
    out_l1_out = g.add_outcome([2, 0], label="LowCost_Price1_StayOut")

    out_l2_enter = g.add_outcome([0, -1], label="LowCost_Price2_Enter")
    out_l2_out = g.add_outcome([4, 0], label="LowCost_Price2_StayOut")

    # Attach outcomes to terminal nodes.
    g.set_outcome(h1_enter, out_h1_enter)
    g.set_outcome(h1_out, out_h1_out)

    g.set_outcome(h2_enter, out_h2_enter)
    g.set_outcome(h2_out, out_h2_out)

    g.set_outcome(l1_enter, out_l1_enter)
    g.set_outcome(l1_out, out_l1_out)

    g.set_outcome(l2_enter, out_l2_enter)
    g.set_outcome(l2_out, out_l2_out)

    return g


if __name__ == "__main__":
    g = build_market_signaling_game(q=0.5)

    out_path = Path(__file__).with_name("page331_market_game.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")