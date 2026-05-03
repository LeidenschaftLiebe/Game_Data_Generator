from pathlib import Path
import pygambit as gbt


def build_page_401_exercise_3(p: str = "1/2") -> gbt.Game:
    """Construct Page 401 Exercise 3."""
    g = gbt.Game.new_tree(
        players=["Firm", "Worker"],
        title="Page 401 Exercise 3"
    )

    # Chance selects the firm's type.
    g.append_move(g.root, g.players.chance, actions=["High", "Low"])
    g.set_chance_probs(
        g.root.infoset,
        [gbt.Rational(p), 1 - gbt.Rational(p)]
    )

    node_H = g.root.children["High"]
    node_L = g.root.children["Low"]

    # Firm observes type and chooses whether to make an offer.
    g.append_move(node_H, player="Firm", actions=["NoOffer_H", "Offer_H"])
    g.append_move(node_L, player="Firm", actions=["NoOffer_L", "Offer_L"])

    node_HN = node_H.children["NoOffer_H"]
    node_HO = node_H.children["Offer_H"]
    node_LN = node_L.children["NoOffer_L"]
    node_LO = node_L.children["Offer_L"]

    # If no offer is made, the game ends immediately.
    out_HN = g.add_outcome([0, 0], label="High_NoOffer")
    out_LN = g.add_outcome([0, 0], label="Low_NoOffer")
    g.set_outcome(node_HN, out_HN)
    g.set_outcome(node_LN, out_LN)

    # Worker moves after an offer without observing firm quality.
    g.append_move(node_HO, player="Worker", actions=["Accept", "Reject"])
    g.append_infoset(node_LO, node_HO.infoset)

    node_HOA = node_HO.children["Accept"]
    node_HOR = node_HO.children["Reject"]
    node_LOA = node_LO.children["Accept"]
    node_LOR = node_LO.children["Reject"]

    # Distinct outcomes for each terminal node.
    out_HOA = g.add_outcome([2, 2], label="High_Offer_Accept")
    out_HOR = g.add_outcome([-1, 0], label="High_Offer_Reject")

    out_LOA = g.add_outcome([2, -1], label="Low_Offer_Accept")
    out_LOR = g.add_outcome([-1, 0], label="Low_Offer_Reject")

    g.set_outcome(node_HOA, out_HOA)
    g.set_outcome(node_HOR, out_HOR)
    g.set_outcome(node_LOA, out_LOA)
    g.set_outcome(node_LOR, out_LOR)

    return g


if __name__ == "__main__":
    g = build_page_401_exercise_3(p="1/2")

    out_path = Path(__file__).with_name("game_page401_exercise3.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")



