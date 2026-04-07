from pathlib import Path
import pygambit as gbt


def build_fig4_v0_delegation_game():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2", "Player 3"],
        title="GEB Fig. 4 Variation of the Three-Player Delegation Game V0"
    )

    # Player 1 moves first: A or B
    g.append_move(g.root, "Player 1", actions=["A", "B"])
    node_a = g.root.children["A"]
    node_b = g.root.children["B"]

    # If Player 1 chooses B, Player 2 moves: C or D
    g.append_move(node_b, "Player 2", actions=["C", "D"])
    node_c = node_b.children["C"]
    node_d = node_b.children["D"]

    # If Player 2 chooses D, Player 1 moves again: E or F
    g.append_move(node_d, "Player 1", actions=["E", "F"])
    node_e = node_d.children["E"]
    node_f = node_d.children["F"]

    # If Player 1 chooses F, Player 3 moves: G or H
    g.append_move(node_f, "Player 3", actions=["G", "H"])
    node_g = node_f.children["G"]
    node_h = node_f.children["H"]

    # Outcomes
    out_a = g.add_outcome([5, 5, 5], label="A")
    out_c = g.add_outcome([7, 9, -3], label="B_C")
    out_e = g.add_outcome([8, 5, 0], label="B_D_E")
    out_g = g.add_outcome([11, 11, 9], label="B_D_F_G")
    out_h = g.add_outcome([2, 7, 10], label="B_D_F_H")

    # Assign outcomes to terminal nodes
    g.set_outcome(node_a, out_a)
    g.set_outcome(node_c, out_c)
    g.set_outcome(node_e, out_e)
    g.set_outcome(node_g, out_g)
    g.set_outcome(node_h, out_h)

    return g


if __name__ == "__main__":
    g = build_fig4_v0_delegation_game()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



    