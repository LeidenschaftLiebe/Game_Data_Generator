from pathlib import Path
import pygambit as gbt


def build_symmetric_extensive_form_game_v0():
    g = gbt.Game.new_tree(
        players=["I", "II"],
        title="Symmetric Extensive Form Game V0"
    )

    # Nature chooses u or v with equal probability
    g.append_move(g.root, g.players.chance, actions=["u", "v"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    node_u = g.root.children["u"]
    node_v = g.root.children["v"]

    # Player I moves after u and after v
    g.append_move(node_u, "I", actions=["R", "S", "P"])
    g.append_move(node_v, "I", actions=["R", "S", "P"])

    # Player II moves in subgame u, without observing I's action there
    u_after_R = node_u.children["R"]
    u_after_S = node_u.children["S"]
    u_after_P = node_u.children["P"]

    g.append_move(u_after_R, "II", actions=["R", "S", "P"])
    u_infoset = u_after_R.infoset
    g.append_infoset(u_after_S, u_infoset)
    g.append_infoset(u_after_P, u_infoset)

    # Player II moves in subgame v, without observing I's action there
    v_after_R = node_v.children["R"]
    v_after_S = node_v.children["S"]
    v_after_P = node_v.children["P"]

    g.append_move(v_after_R, "II", actions=["R", "S", "P"])
    v_infoset = v_after_R.infoset
    g.append_infoset(v_after_S, v_infoset)
    g.append_infoset(v_after_P, v_infoset)

    # Distinct outcomes for subgame u
    out_u_R_R = g.add_outcome([0, 0], label="u_I_R_II_R")
    out_u_R_S = g.add_outcome([6, -4], label="u_I_R_II_S")
    out_u_R_P = g.add_outcome([-4, 2], label="u_I_R_II_P")

    out_u_S_R = g.add_outcome([-4, 6], label="u_I_S_II_R")
    out_u_S_S = g.add_outcome([0, 0], label="u_I_S_II_S")
    out_u_S_P = g.add_outcome([4, -2], label="u_I_S_II_P")

    out_u_P_R = g.add_outcome([2, -4], label="u_I_P_II_R")
    out_u_P_S = g.add_outcome([-2, 4], label="u_I_P_II_S")
    out_u_P_P = g.add_outcome([0, 0], label="u_I_P_II_P")

    # Distinct outcomes for subgame v
    out_v_R_R = g.add_outcome([0, 0], label="v_I_R_II_R")
    out_v_R_S = g.add_outcome([6, -4], label="v_I_R_II_S")
    out_v_R_P = g.add_outcome([-4, 2], label="v_I_R_II_P")

    out_v_S_R = g.add_outcome([-4, 6], label="v_I_S_II_R")
    out_v_S_S = g.add_outcome([0, 0], label="v_I_S_II_S")
    out_v_S_P = g.add_outcome([4, -2], label="v_I_S_II_P")

    out_v_P_R = g.add_outcome([2, -4], label="v_I_P_II_R")
    out_v_P_S = g.add_outcome([-2, 4], label="v_I_P_II_S")
    out_v_P_P = g.add_outcome([0, 0], label="v_I_P_II_P")

    # Assign outcomes in subgame u
    g.set_outcome(u_after_R.children["R"], out_u_R_R)
    g.set_outcome(u_after_R.children["S"], out_u_R_S)
    g.set_outcome(u_after_R.children["P"], out_u_R_P)

    g.set_outcome(u_after_S.children["R"], out_u_S_R)
    g.set_outcome(u_after_S.children["S"], out_u_S_S)
    g.set_outcome(u_after_S.children["P"], out_u_S_P)

    g.set_outcome(u_after_P.children["R"], out_u_P_R)
    g.set_outcome(u_after_P.children["S"], out_u_P_S)
    g.set_outcome(u_after_P.children["P"], out_u_P_P)

    # Assign outcomes in subgame v
    g.set_outcome(v_after_R.children["R"], out_v_R_R)
    g.set_outcome(v_after_R.children["S"], out_v_R_S)
    g.set_outcome(v_after_R.children["P"], out_v_R_P)

    g.set_outcome(v_after_S.children["R"], out_v_S_R)
    g.set_outcome(v_after_S.children["S"], out_v_S_S)
    g.set_outcome(v_after_S.children["P"], out_v_S_P)

    g.set_outcome(v_after_P.children["R"], out_v_P_R)
    g.set_outcome(v_after_P.children["S"], out_v_P_S)
    g.set_outcome(v_after_P.children["P"], out_v_P_P)

    return g


if __name__ == "__main__":
    game = build_symmetric_extensive_form_game_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
    