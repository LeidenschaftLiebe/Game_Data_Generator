from pathlib import Path
import pygambit as gbt


def build_joint_venture_game() -> gbt.Game:
    """Construct the Microsoft-Celera style game with two Microsoft types."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Joint Venture with Hidden Type"
    )

    # Chance selects Microsoft's type.
    g.append_move(g.root, g.players.chance, actions=["Enemy", "Friend"])
    g.set_chance_probs(g.root.infoset, [0.5, 0.5])

    enemy_node = g.root.children["Enemy"]
    friend_node = g.root.children["Friend"]

    # Microsoft observes its type and chooses Invest or Sabotage.
    g.append_move(enemy_node, player="1", actions=["Invest_E", "Sabotage_E"])
    g.append_move(friend_node, player="1", actions=["Invest_F", "Sabotage_F"])

    enemy_invest = enemy_node.children["Invest_E"]
    enemy_sabotage = enemy_node.children["Sabotage_E"]
    friend_invest = friend_node.children["Invest_F"]
    friend_sabotage = friend_node.children["Sabotage_F"]

    # Celera chooses Reveal or Hide without observing Microsoft's type or action.
    g.append_move(enemy_invest, player="2", actions=["Reveal", "Hide"])
    g.append_infoset(enemy_sabotage, enemy_invest.infoset)
    g.append_infoset(friend_invest, enemy_invest.infoset)
    g.append_infoset(friend_sabotage, enemy_invest.infoset)

    # Terminal nodes.
    ei_r = enemy_invest.children["Reveal"]
    ei_h = enemy_invest.children["Hide"]

    es_r = enemy_sabotage.children["Reveal"]
    es_h = enemy_sabotage.children["Hide"]

    fi_r = friend_invest.children["Reveal"]
    fi_h = friend_invest.children["Hide"]

    fs_r = friend_sabotage.children["Reveal"]
    fs_h = friend_sabotage.children["Hide"]

    # One distinct outcome per terminal node.
    out_ei_r = g.add_outcome([5, 1], label="Enemy_Invest_Reveal")
    out_ei_h = g.add_outcome([0, 3], label="Enemy_Invest_Hide")

    out_es_r = g.add_outcome([8, -1], label="Enemy_Sabotage_Reveal")
    out_es_h = g.add_outcome([7, 0], label="Enemy_Sabotage_Hide")

    out_fi_r = g.add_outcome([9, 9], label="Friend_Invest_Reveal")
    out_fi_h = g.add_outcome([0, 0], label="Friend_Invest_Hide")

    out_fs_r = g.add_outcome([2, 0], label="Friend_Sabotage_Reveal")
    out_fs_h = g.add_outcome([0, 4], label="Friend_Sabotage_Hide")

    # Attach outcomes.
    g.set_outcome(ei_r, out_ei_r)
    g.set_outcome(ei_h, out_ei_h)

    g.set_outcome(es_r, out_es_r)
    g.set_outcome(es_h, out_es_h)

    g.set_outcome(fi_r, out_fi_r)
    g.set_outcome(fi_h, out_fi_h)

    g.set_outcome(fs_r, out_fs_r)
    g.set_outcome(fs_h, out_fs_h)

    return g


if __name__ == "__main__":
    g = build_joint_venture_game()

    out_path = Path(__file__).with_name("game_page334_exercise5a.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")