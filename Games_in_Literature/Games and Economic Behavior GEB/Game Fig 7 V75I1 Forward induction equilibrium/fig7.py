from pathlib import Path
import pygambit as gbt


def build_fig7a_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2", "Player 3"],
        title="GEB Fig. 7(a) Modified Selten's Horse V0"
    )

    # Player 1 moves first
    g.append_move(g.root, "Player 1", actions=["T", "NotT"])
    t_node = g.root.children["T"]
    not_t_node = g.root.children["NotT"]

    # If Not T, Player 2 moves
    g.append_move(not_t_node, "Player 2", actions=["L", "R"])
    l_node = not_t_node.children["L"]
    r_node = not_t_node.children["R"]

    # R ends the game
    out_r = g.add_outcome([1, 2, 2], label="NotT_R")
    g.set_outcome(r_node, out_r)

    # If L, Player 1 moves again
    g.append_move(l_node, "Player 1", actions=["B", "M"])
    b_node = l_node.children["B"]
    m_node = l_node.children["M"]

    # B ends the game
    out_b = g.add_outcome([2, 0, 0], label="NotT_L_B")
    g.set_outcome(b_node, out_b)

    # Player 3 moves after T, and after NotT->L->M in the same infoset
    g.append_move(t_node, "Player 3", actions=["U", "D"])
    shared_infoset = t_node.infoset
    g.append_infoset(m_node, shared_infoset)

    # Distinct outcomes
    out_t_u = g.add_outcome([3, 1, 1], label="T_U")
    out_t_d = g.add_outcome([0, 0, 0], label="T_D")
    out_m_u = g.add_outcome([0, 0, 0], label="NotT_L_M_U")
    out_m_d = g.add_outcome([1, 1, 1], label="NotT_L_M_D")

    # Assign outcomes
    g.set_outcome(t_node.children["U"], out_t_u)
    g.set_outcome(t_node.children["D"], out_t_d)
    g.set_outcome(m_node.children["U"], out_m_u)
    g.set_outcome(m_node.children["D"], out_m_d)

    return g


if __name__ == "__main__":
    game = build_fig7a_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


