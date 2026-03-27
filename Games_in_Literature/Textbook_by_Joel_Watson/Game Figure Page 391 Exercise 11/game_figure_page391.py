from pathlib import Path
import pygambit as gbt


def build_three_node_infoset_game() -> gbt.Game:
    """Construct the game shown in the image."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Three-Node Infoset Game"
    )

    # Chance selects L or H with equal probability.
    g.append_move(g.root, g.players.chance, actions=["L_state", "H_state"])
    g.set_chance_probs(g.root.infoset, [0.5, 0.5])

    node_Lstate = g.root.children["L_state"]
    node_Hstate = g.root.children["H_state"]

    # After L_state, Player 1 chooses A or B.
    g.append_move(node_Lstate, player="1", actions=["A", "B"])
    node_A = node_Lstate.children["A"]
    node_B = node_Lstate.children["B"]

    # After H_state, Player 1 chooses C, D, or E.
    g.append_move(node_Hstate, player="1", actions=["C", "D", "E"])
    node_C = node_Hstate.children["C"]
    node_D = node_Hstate.children["D"]
    node_E = node_Hstate.children["E"]

    # Player 2 moves after B, C, or D in one information set.
    g.append_move(node_B, player="2", actions=["F", "G"])
    g.append_infoset(node_C, node_B.infoset)
    g.append_infoset(node_D, node_B.infoset)

    node_BF = node_B.children["F"]
    node_BG = node_B.children["G"]
    node_CF = node_C.children["F"]
    node_CG = node_C.children["G"]
    node_DF = node_D.children["F"]
    node_DG = node_D.children["G"]

    # Distinct outcomes.
    out_A = g.add_outcome([2, 10], label="A")
    out_BF = g.add_outcome([0, 10], label="B_F")
    out_BG = g.add_outcome([-10, 2], label="B_G")

    out_CF = g.add_outcome([6, 0], label="C_F")
    out_CG = g.add_outcome([-10, 7], label="C_G")

    out_DF = g.add_outcome([3, 5], label="D_F")
    out_DG = g.add_outcome([3, 5], label="D_G")

    out_E = g.add_outcome([2, 10], label="E")

    # Attach outcomes.
    g.set_outcome(node_A, out_A)
    g.set_outcome(node_BF, out_BF)
    g.set_outcome(node_BG, out_BG)

    g.set_outcome(node_CF, out_CF)
    g.set_outcome(node_CG, out_CG)

    g.set_outcome(node_DF, out_DF)
    g.set_outcome(node_DG, out_DG)

    g.set_outcome(node_E, out_E)

    return g


if __name__ == "__main__":
    g = build_three_node_infoset_game()

    out_path = Path(__file__).with_name("game_figure_page391.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")



