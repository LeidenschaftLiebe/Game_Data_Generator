from pathlib import Path
import pygambit as gbt


def build_geb_beer_and_quiche_fig5() -> gbt.Game:
    """Construct Fig. 5 Beer-and-Quiche Game."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Receiver"],
        title="GEB Beer-and-Quiche Fig. 5"
    )

    # Nature determines Player 1's type.
    g.append_move(g.root, player=g.players.chance, actions=["s", "w"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational("9/10"), gbt.Rational("1/10")])

    node_s = g.root.children["s"]
    node_w = g.root.children["w"]

    # Player 1 chooses between B and Q after learning the type.
    g.append_move(node_s, player="Player 1", actions=["B", "Q"])
    g.append_move(node_w, player="Player 1", actions=["B", "Q"])

    node_s_B = node_s.children["B"]
    node_s_Q = node_s.children["Q"]
    node_w_B = node_w.children["B"]
    node_w_Q = node_w.children["Q"]

    # Receiver observes B versus Q, but not the type.
    g.append_move(node_s_B, player="Receiver", actions=["NF", "F"])
    g.append_infoset(node_w_B, node_s_B.infoset)

    g.append_move(node_s_Q, player="Receiver", actions=["NF", "F"])
    g.append_infoset(node_w_Q, node_s_Q.infoset)

    # Outcomes after B.
    out_s_B_NF = g.add_outcome([3, 1], label="s_B_NF")
    out_s_B_F = g.add_outcome([1, 0], label="s_B_F")
    out_w_B_NF = g.add_outcome([2, 0], label="w_B_NF")
    out_w_B_F = g.add_outcome([0, 1], label="w_B_F")

    g.set_outcome(node_s_B.children["NF"], out_s_B_NF)
    g.set_outcome(node_s_B.children["F"], out_s_B_F)
    g.set_outcome(node_w_B.children["NF"], out_w_B_NF)
    g.set_outcome(node_w_B.children["F"], out_w_B_F)

    # Outcomes after Q.
    out_s_Q_NF = g.add_outcome([2, 1], label="s_Q_NF")
    out_s_Q_F = g.add_outcome([0, 0], label="s_Q_F")
    out_w_Q_NF = g.add_outcome([3, 0], label="w_Q_NF")
    out_w_Q_F = g.add_outcome([1, 1], label="w_Q_F")

    g.set_outcome(node_s_Q.children["NF"], out_s_Q_NF)
    g.set_outcome(node_s_Q.children["F"], out_s_Q_F)
    g.set_outcome(node_w_Q.children["NF"], out_w_Q_NF)
    g.set_outcome(node_w_Q.children["F"], out_w_Q_F)

    return g


if __name__ == "__main__":
    g = build_geb_beer_and_quiche_fig5()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")