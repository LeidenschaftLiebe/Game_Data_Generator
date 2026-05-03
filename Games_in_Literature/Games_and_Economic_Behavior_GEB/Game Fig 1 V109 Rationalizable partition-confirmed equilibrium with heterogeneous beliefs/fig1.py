from pathlib import Path
import pygambit as gbt


def build_broker_seller_buyer_v0():
    g = gbt.Game.new_tree(
        players=["Broker", "Seller", "Buyer"],
        title="Fig1 Game V0"
    )

    # Broker moves first
    g.append_move(g.root, "Broker", actions=["Out1", "In1"])
    out1 = g.root.children["Out1"]
    in1 = g.root.children["In1"]

    # Seller moves after broker enters
    g.append_move(in1, "Seller", actions=["U2", "D2"])
    u2 = in1.children["U2"]
    d2 = in1.children["D2"]

    # Buyer moves after U2
    g.append_move(u2, "Buyer", actions=["U3", "D3"])

    # Buyer moves after D2, sharing the same infoset
    g.append_infoset(d2, u2.infoset)

    # Outcomes
    out_out1 = g.add_outcome([2, 0, 0], label="Out1")
    out_in1_u2_u3 = g.add_outcome([3, 3, 3], label="In1_U2_U3")
    out_in1_u2_d3 = g.add_outcome([0, 0, 0], label="In1_U2_D3")
    out_in1_d2_u3 = g.add_outcome([0, 0, 0], label="In1_D2_U3")
    out_in1_d2_d3 = g.add_outcome([1, 1, 1], label="In1_D2_D3")

    # Assign outcomes
    g.set_outcome(out1, out_out1)
    g.set_outcome(u2.children["U3"], out_in1_u2_u3)
    g.set_outcome(u2.children["D3"], out_in1_u2_d3)
    g.set_outcome(d2.children["U3"], out_in1_d2_u3)
    g.set_outcome(d2.children["D3"], out_in1_d2_d3)

    return g


if __name__ == "__main__":
    g = build_broker_seller_buyer_v0()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


