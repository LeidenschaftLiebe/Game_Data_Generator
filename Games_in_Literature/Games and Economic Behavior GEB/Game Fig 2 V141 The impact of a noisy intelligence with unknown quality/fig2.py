from pathlib import Path
import pygambit as gbt


def build_geb_complete_information_fig2() -> gbt.Game:
    """Construct Fig. 2 (The Game with Complete Information)."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Complete Information Fig. 2"
    )

    # Fixed parameter values for this dataset instance.
    alpha = gbt.Rational("4/5")   # 0.8
    r1 = gbt.Rational("1/5")      # 0.2
    r2 = gbt.Rational("3/10")     # 0.3
    w1 = gbt.Rational("7/10")     # 0.7
    w2 = gbt.Rational("4/5")      # 0.8

    # Player 1 first chooses whether to build a bomb.
    g.append_move(g.root, player="Player 1", actions=["NB", "B"])

    node_NB = g.root.children["NB"]
    node_B = g.root.children["B"]

    # The intelligence system sends a noisy signal.
    g.append_move(node_NB, player=g.players.chance, actions=["b", "nb"])
    g.set_chance_probs(node_NB.infoset, [1 - alpha, alpha])

    g.append_move(node_B, player=g.players.chance, actions=["b", "nb"])
    g.set_chance_probs(node_B.infoset, [alpha, 1 - alpha])

    node_NB_b = node_NB.children["b"]
    node_NB_nb = node_NB.children["nb"]
    node_B_b = node_B.children["b"]
    node_B_nb = node_B.children["nb"]

    # Player 2 observes the signal but not Player 1's actual action.
    # One infoset after signal b, another infoset after signal nb.
    g.append_move(node_NB_b, player="Player 2", actions=["A", "NA"])
    g.append_infoset(node_B_b, node_NB_b.infoset)

    g.append_move(node_NB_nb, player="Player 2", actions=["A", "NA"])
    g.append_infoset(node_B_nb, node_NB_nb.infoset)

    # Outcomes after signal b.
    out_NB_A = g.add_outcome([r1, r2], label="NB_b_A")
    out_NB_NA = g.add_outcome([w1, 1], label="NB_b_NA")
    out_B_A = g.add_outcome([0, w2], label="B_b_A")
    out_B_NA = g.add_outcome([1, 0], label="B_b_NA")

    g.set_outcome(node_NB_b.children["A"], out_NB_A)
    g.set_outcome(node_NB_b.children["NA"], out_NB_NA)
    g.set_outcome(node_B_b.children["A"], out_B_A)
    g.set_outcome(node_B_b.children["NA"], out_B_NA)

    # Outcomes after signal nb.
    out_NB_A_nb = g.add_outcome([r1, r2], label="NB_nb_A")
    out_NB_NA_nb = g.add_outcome([w1, 1], label="NB_nb_NA")
    out_B_A_nb = g.add_outcome([0, w2], label="B_nb_A")
    out_B_NA_nb = g.add_outcome([1, 0], label="B_nb_NA")

    g.set_outcome(node_NB_nb.children["A"], out_NB_A_nb)
    g.set_outcome(node_NB_nb.children["NA"], out_NB_NA_nb)
    g.set_outcome(node_B_nb.children["A"], out_B_A_nb)
    g.set_outcome(node_B_nb.children["NA"], out_B_NA_nb)

    return g


if __name__ == "__main__":
    g = build_geb_complete_information_fig2()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")




    