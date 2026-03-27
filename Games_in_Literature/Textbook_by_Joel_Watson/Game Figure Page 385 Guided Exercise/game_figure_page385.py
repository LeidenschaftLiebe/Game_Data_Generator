from pathlib import Path
import pygambit as gbt


def build_amy_brenda_newspaper_game(p: float = 0.5) -> gbt.Game:
    """Construct the Amy-Brenda newspaper signaling game."""
    if not (0.0 <= p <= 1.0):
        raise ValueError("p must be between 0 and 1")

    g = gbt.Game.new_tree(
        players=["Amy", "Brenda"],
        title="Amy and Brenda Mall Game"
    )

    # Chance selects whether the shoes are on sale.
    g.append_move(g.root, g.players.chance, actions=["Sale", "NoSale"])
    g.set_chance_probs(g.root.infoset, [p, 1 - p])

    sale_node = g.root.children["Sale"]
    nosale_node = g.root.children["NoSale"]

    # Amy observes the state and decides whether to take the newspaper.
    g.append_move(sale_node, player="Amy", actions=["TakePaper_sale", "NoPaper_sale"])
    g.append_move(nosale_node, player="Amy", actions=["TakePaper_nosale", "NoPaper_nosale"])

    sale_take = sale_node.children["TakePaper_sale"]
    sale_no = sale_node.children["NoPaper_sale"]
    nosale_take = nosale_node.children["TakePaper_nosale"]
    nosale_no = nosale_node.children["NoPaper_nosale"]

    # Brenda observes whether Amy brought the paper.
    # If Amy takes the paper, Brenda learns whether there is a sale, so separate infosets.
    g.append_move(sale_take, player="Brenda", actions=["Go", "Refuse"])
    g.append_move(nosale_take, player="Brenda", actions=["Go", "Refuse"])

    # If Amy does not take the paper, Brenda cannot distinguish sale from no-sale.
    g.append_move(sale_no, player="Brenda", actions=["Go", "Refuse"])
    g.append_infoset(nosale_no, sale_no.infoset)

    # Terminal nodes after taking paper in sale case.
    st_go = sale_take.children["Go"]
    st_refuse = sale_take.children["Refuse"]

    # Terminal nodes after taking paper in no-sale case.
    nt_go = nosale_take.children["Go"]
    nt_refuse = nosale_take.children["Refuse"]

    # Terminal nodes after not taking paper.
    sn_go = sale_no.children["Go"]
    sn_refuse = sale_no.children["Refuse"]
    nn_go = nosale_no.children["Go"]
    nn_refuse = nosale_no.children["Refuse"]

    # Distinct outcomes for each terminal node.
    out_st_go = g.add_outcome([1, 1], label="Sale_Take_Go")
    out_st_refuse = g.add_outcome([-2, 0], label="Sale_Take_Refuse")

    out_nt_go = g.add_outcome([-1, -1], label="NoSale_Take_Go")
    out_nt_refuse = g.add_outcome([-2, 0], label="NoSale_Take_Refuse")

    out_sn_go = g.add_outcome([3, 1], label="Sale_NoTake_Go")
    out_sn_refuse = g.add_outcome([0, 0], label="Sale_NoTake_Refuse")

    out_nn_go = g.add_outcome([1, -1], label="NoSale_NoTake_Go")
    out_nn_refuse = g.add_outcome([0, 0], label="NoSale_NoTake_Refuse")

    # Attach outcomes.
    g.set_outcome(st_go, out_st_go)
    g.set_outcome(st_refuse, out_st_refuse)

    g.set_outcome(nt_go, out_nt_go)
    g.set_outcome(nt_refuse, out_nt_refuse)

    g.set_outcome(sn_go, out_sn_go)
    g.set_outcome(sn_refuse, out_sn_refuse)

    g.set_outcome(nn_go, out_nn_go)
    g.set_outcome(nn_refuse, out_nn_refuse)

    return g


if __name__ == "__main__":
    g = build_amy_brenda_newspaper_game(p=0.5)

    out_path = Path(__file__).with_name("amy_brenda_mall_game.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")

    