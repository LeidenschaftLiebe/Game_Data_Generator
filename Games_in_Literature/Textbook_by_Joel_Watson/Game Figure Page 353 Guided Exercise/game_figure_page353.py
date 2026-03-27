from pathlib import Path
import pygambit as gbt


def build_hidden_chance_game() -> gbt.Game:
    """Construct the game shown in the image."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Hidden Chance and Imperfect Information Game"
    )

    # Player 1 first chooses L or D.
    g.append_move(g.root, player="1", actions=["L", "D"])

    node_L = g.root.children["L"]
    node_D = g.root.children["D"]

    # If Player 1 chooses L, Player 2 chooses A or B.
    g.append_move(node_L, player="2", actions=["A", "B"])

    node_LA = node_L.children["A"]
    node_LB = node_L.children["B"]

    # If Player 1 chooses D, chance selects P or Q with equal probability.
    g.append_move(node_D, g.players.chance, actions=["P", "Q"])
    g.set_chance_probs(node_D.infoset, [0.5, 0.5])

    node_DP = node_D.children["P"]
    node_DQ = node_D.children["Q"]

    # After P, Player 2 chooses A or B in the same infoset as after L.
    g.append_infoset(node_DP, node_L.infoset)

    node_DPA = node_DP.children["A"]
    node_DPB = node_DP.children["B"]

    # After Q, Player 2 chooses X or Y at a separate decision node.
    g.append_move(node_DQ, player="2", actions=["X", "Y"])

    node_DQX = node_DQ.children["X"]
    node_DQY = node_DQ.children["Y"]

    # One distinct outcome per terminal node.
    outcome_LA = g.add_outcome([0, 4], label="L_A")
    outcome_LB = g.add_outcome([4, 0], label="L_B")
    outcome_DPA = g.add_outcome([4, 0], label="D_P_A")
    outcome_DPB = g.add_outcome([0, 4], label="D_P_B")
    outcome_DQX = g.add_outcome([2, 2], label="D_Q_X")
    outcome_DQY = g.add_outcome([0, 0], label="D_Q_Y")

    # Attach outcomes.
    g.set_outcome(node_LA, outcome_LA)
    g.set_outcome(node_LB, outcome_LB)
    g.set_outcome(node_DPA, outcome_DPA)
    g.set_outcome(node_DPB, outcome_DPB)
    g.set_outcome(node_DQX, outcome_DQX)
    g.set_outcome(node_DQY, outcome_DQY)

    return g


if __name__ == "__main__":
    g = build_hidden_chance_game()

    out_path = Path(__file__).with_name("game_figure_page353.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")


