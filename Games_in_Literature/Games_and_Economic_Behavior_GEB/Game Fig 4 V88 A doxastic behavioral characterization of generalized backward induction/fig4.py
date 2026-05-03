from pathlib import Path
import pygambit as gbt


def build_fig4c_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2", "Player 3"],
        title="GEB Fig. 4(C) Example V0"
    )

    # Player 1 at the root
    g.append_move(g.root, "Player 1", actions=["a", "b", "c"])
    node_a = g.root.children["a"]
    node_b = g.root.children["b"]
    node_c = g.root.children["c"]

    # Player 2 after b, with same infoset after c
    g.append_move(node_b, "Player 2", actions=["d", "e"])
    g.append_infoset(node_c, node_b.infoset)

    node_bd = node_b.children["d"]
    node_be = node_b.children["e"]
    node_cd = node_c.children["d"]
    node_ce = node_c.children["e"]

    # Player 3 after b-d, same infoset for the other three nodes
    g.append_move(node_bd, "Player 3", actions=["s", "t", "u"])
    shared_p3_infoset = node_bd.infoset
    g.append_infoset(node_be, shared_p3_infoset)
    g.append_infoset(node_cd, shared_p3_infoset)
    g.append_infoset(node_ce, shared_p3_infoset)

    # Distinct outcomes for every terminal history
    out_a = g.add_outcome([2, 0, 0], label="a")

    out_bd_s = g.add_outcome([3, 1, 1], label="b_d_s")
    out_bd_t = g.add_outcome([0, 1, 2], label="b_d_t")
    out_bd_u = g.add_outcome([2, 2, 0], label="b_d_u")

    out_be_s = g.add_outcome([0, 0, 2], label="b_e_s")
    out_be_t = g.add_outcome([2, 0, 1], label="b_e_t")
    out_be_u = g.add_outcome([1, 2, 0], label="b_e_u")

    out_cd_s = g.add_outcome([0, 1, 1], label="c_d_s")
    out_cd_t = g.add_outcome([0, 1, 2], label="c_d_t")
    out_cd_u = g.add_outcome([2, 2, 0], label="c_d_u")

    out_ce_s = g.add_outcome([2, 0, 2], label="c_e_s")
    out_ce_t = g.add_outcome([3, 0, 1], label="c_e_t")
    out_ce_u = g.add_outcome([2, 2, 0], label="c_e_u")

    # Assign outcomes
    g.set_outcome(node_a, out_a)

    g.set_outcome(node_bd.children["s"], out_bd_s)
    g.set_outcome(node_bd.children["t"], out_bd_t)
    g.set_outcome(node_bd.children["u"], out_bd_u)

    g.set_outcome(node_be.children["s"], out_be_s)
    g.set_outcome(node_be.children["t"], out_be_t)
    g.set_outcome(node_be.children["u"], out_be_u)

    g.set_outcome(node_cd.children["s"], out_cd_s)
    g.set_outcome(node_cd.children["t"], out_cd_t)
    g.set_outcome(node_cd.children["u"], out_cd_u)

    g.set_outcome(node_ce.children["s"], out_ce_s)
    g.set_outcome(node_ce.children["t"], out_ce_t)
    g.set_outcome(node_ce.children["u"], out_ce_u)

    return g


if __name__ == "__main__":
    game = build_fig4c_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


