from pathlib import Path
import pygambit as gbt


def build_fig_oc_v0():
    g = gbt.Game.new_tree(
        players=["Seller", "Buyer"],
        title="GEB Option Contract V0"
    )

    # Seller decides whether to accept the option contract
    g.append_move(g.root, "Seller", actions=["yes", "no"])
    seller_yes = g.root.children["yes"]
    seller_no = g.root.children["no"]

    # Buyer moves after seller_yes
    g.append_move(seller_yes, "Buyer", actions=["yes", "no"])

    # Make the Buyer node after seller_no part of the same infoset.
    # seller_no must still be terminal here.
    g.append_infoset(seller_no, seller_yes.infoset)

    buyer_yes_after_yes = seller_yes.children["yes"]
    buyer_no_after_yes = seller_yes.children["no"]
    buyer_yes_after_no = seller_no.children["yes"]
    buyer_no_after_no = seller_no.children["no"]

    # If seller said no, or buyer said no, game ends with (0, 0)
    g.set_outcome(buyer_yes_after_no, g.add_outcome([0, 0], label="seller_no_buyer_yes"))
    g.set_outcome(buyer_no_after_no, g.add_outcome([0, 0], label="seller_no_buyer_no"))
    g.set_outcome(buyer_no_after_yes, g.add_outcome([0, 0], label="seller_yes_buyer_no"))

    # If both accept, seller chooses investment
    g.append_move(buyer_yes_after_yes, "Seller", actions=["e0", "e8"])
    e0 = buyer_yes_after_yes.children["e0"]
    e8 = buyer_yes_after_yes.children["e8"]

    # Buyer chooses whether to exercise
    g.append_move(e0, "Buyer", actions=["exercise", "not_exercise"])
    g.append_move(e8, "Buyer", actions=["exercise", "not_exercise"])

    # Distinct outcomes
    out_e0_ex = g.add_outcome([15, -5], label="yes_yes_e0_exercise")
    out_e0_no = g.add_outcome([0, 0], label="yes_yes_e0_not_exercise")
    out_e8_ex = g.add_outcome([7, 7], label="yes_yes_e8_exercise")
    out_e8_no = g.add_outcome([-8, 0], label="yes_yes_e8_not_exercise")

    g.set_outcome(e0.children["exercise"], out_e0_ex)
    g.set_outcome(e0.children["not_exercise"], out_e0_no)
    g.set_outcome(e8.children["exercise"], out_e8_ex)
    g.set_outcome(e8.children["not_exercise"], out_e8_no)

    return g


if __name__ == "__main__":
    game = build_fig_oc_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
