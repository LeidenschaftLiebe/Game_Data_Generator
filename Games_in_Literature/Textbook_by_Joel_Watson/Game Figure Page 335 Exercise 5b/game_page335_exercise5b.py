from pathlib import Path
import pygambit as gbt


def build_joint_venture_game_part_b() -> gbt.Game:
    """Construct Microsoft-Celera part (b)."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Joint Venture with Hidden Type - Part B"
    )

    # Chance selects Microsoft's type.
    g.append_move(g.root, g.players.chance, actions=["Friend", "Enemy"])
    g.set_chance_probs(g.root.infoset, [0.5, 0.5])

    friend_node = g.root.children["Friend"]
    enemy_node = g.root.children["Enemy"]

    # Microsoft observes its type and chooses Buy or Sell.
    g.append_move(friend_node, player="1", actions=["Sell_F", "Buy_F"])
    g.append_move(enemy_node, player="1", actions=["Sell_E", "Buy_E"])

    sell_f = friend_node.children["Sell_F"]
    buy_f = friend_node.children["Buy_F"]
    sell_e = enemy_node.children["Sell_E"]
    buy_e = enemy_node.children["Buy_E"]

    # Celera observes Buy versus Sell, but not Microsoft's type.
    # One infoset after Sell, one infoset after Buy.
    g.append_move(sell_f, player="2", actions=["Reveal", "Hide"])
    g.append_infoset(sell_e, sell_f.infoset)

    g.append_move(buy_f, player="2", actions=["Reveal", "Hide"])
    g.append_infoset(buy_e, buy_f.infoset)

    # Terminal nodes after Sell.
    sf_r = sell_f.children["Reveal"]
    sf_h = sell_f.children["Hide"]
    se_r = sell_e.children["Reveal"]
    se_h = sell_e.children["Hide"]

    # Terminal nodes after Buy.
    bf_r = buy_f.children["Reveal"]
    bf_h = buy_f.children["Hide"]
    be_r = buy_e.children["Reveal"]
    be_h = buy_e.children["Hide"]

    # One distinct outcome per terminal node.
    out_sf_r = g.add_outcome([5, 6], label="Friend_Sell_Reveal")
    out_sf_h = g.add_outcome([5, -1], label="Friend_Sell_Hide")

    out_bf_r = g.add_outcome([15, 12], label="Friend_Buy_Reveal")
    out_bf_h = g.add_outcome([-1, 1], label="Friend_Buy_Hide")

    out_se_r = g.add_outcome([15, -14], label="Enemy_Sell_Reveal")
    out_se_h = g.add_outcome([0, -1], label="Enemy_Sell_Hide")

    out_be_r = g.add_outcome([5, -6], label="Enemy_Buy_Reveal")
    out_be_h = g.add_outcome([5, 1], label="Enemy_Buy_Hide")

    # Attach outcomes.
    g.set_outcome(sf_r, out_sf_r)
    g.set_outcome(sf_h, out_sf_h)

    g.set_outcome(bf_r, out_bf_r)
    g.set_outcome(bf_h, out_bf_h)

    g.set_outcome(se_r, out_se_r)
    g.set_outcome(se_h, out_se_h)

    g.set_outcome(be_r, out_be_r)
    g.set_outcome(be_h, out_be_h)

    return g


if __name__ == "__main__":
    g = build_joint_venture_game_part_b()

    out_path = Path(__file__).with_name("joint_venture_hidden_type_part_b.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")