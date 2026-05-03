from pathlib import Path
import pygambit as gbt


def build_sequence_form_fig21_v0():
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Extensive Game and Its Normal Form Example V0"
    )

    # Chance moves first
    g.append_move(g.root, g.players.chance, actions=["v", "v_prime"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 3), gbt.Rational(2, 3)])

    node_v = g.root.children["v"]
    node_vprime = g.root.children["v_prime"]

    # Player 1 moves at v
    g.append_move(node_v, "1", actions=["l", "r"])

    # Player 1 moves at v'
    g.append_move(node_vprime, "1", actions=["L", "R"])

    # Immediate terminals
    out_v_l = g.add_outcome([0, 0], label="v_then_l")
    out_vprime_R = g.add_outcome([gbt.Rational(3, 2), -gbt.Rational(3, 2)], label="vprime_then_R")

    g.set_outcome(node_v.children["l"], out_v_l)
    g.set_outcome(node_vprime.children["R"], out_vprime_R)

    # Player 2 moves after v then r
    after_v_r = node_v.children["r"]
    g.append_move(after_v_r, "2", actions=["c", "d"])
    p2_infoset = after_v_r.infoset

    # Player 2 also moves after v' then L, same infoset
    after_vprime_L = node_vprime.children["L"]
    g.append_infoset(after_vprime_L, p2_infoset)

    # Terminals after player 2 move
    out_v_r_c = g.add_outcome([3, -3], label="v_then_r_then_c")
    out_v_r_d = g.add_outcome([-3, 3], label="v_then_r_then_d")
    out_vprime_L_c = g.add_outcome([-3, 3], label="vprime_then_L_then_c")
    out_vprime_L_d = g.add_outcome([6, -6], label="vprime_then_L_then_d")

    g.set_outcome(after_v_r.children["c"], out_v_r_c)
    g.set_outcome(after_v_r.children["d"], out_v_r_d)
    g.set_outcome(after_vprime_L.children["c"], out_vprime_L_c)
    g.set_outcome(after_vprime_L.children["d"], out_vprime_L_d)

    return g


if __name__ == "__main__":
    game = build_sequence_form_fig21_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


    