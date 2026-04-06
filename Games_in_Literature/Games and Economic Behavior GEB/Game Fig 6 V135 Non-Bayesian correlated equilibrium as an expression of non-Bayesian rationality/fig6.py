from pathlib import Path
import pygambit as gbt


def build_geb_fig6_perfect_information() -> gbt.Game:
    """Construct Fig. 6 extensive-form game with perfect information."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Fig. 6 Perfect Information"
    )

    # Player 1 first chooses whether to take the outside option B.
    g.append_move(g.root, player="Player 1", actions=["B", "not B"])

    node_B = g.root.children["B"]
    node_notB = g.root.children["not B"]

    # If Player 1 chooses B, the game ends immediately.
    out_B = g.add_outcome([-1, 1], label="B")
    g.set_outcome(node_B, out_B)

    # If Player 1 chooses not B, Player 1 then chooses H or T.
    g.append_move(node_notB, player="Player 1", actions=["H", "T"])

    node_H = node_notB.children["H"]
    node_T = node_notB.children["T"]

    # Player 2 moves after observing Player 1's earlier choices.
    g.append_move(node_H, player="Player 2", actions=["H", "T"])
    g.append_move(node_T, player="Player 2", actions=["H", "T"])

    # Outcomes after not B, H.
    out_HH = g.add_outcome([4, -4], label="notB_H_H")
    out_HT = g.add_outcome([-4, 4], label="notB_H_T")
    g.set_outcome(node_H.children["H"], out_HH)
    g.set_outcome(node_H.children["T"], out_HT)

    # Outcomes after not B, T.
    out_TH = g.add_outcome([-4, 4], label="notB_T_H")
    out_TT = g.add_outcome([4, -4], label="notB_T_T")
    g.set_outcome(node_T.children["H"], out_TH)
    g.set_outcome(node_T.children["T"], out_TT)

    return g


if __name__ == "__main__":
    g = build_geb_fig6_perfect_information()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")


