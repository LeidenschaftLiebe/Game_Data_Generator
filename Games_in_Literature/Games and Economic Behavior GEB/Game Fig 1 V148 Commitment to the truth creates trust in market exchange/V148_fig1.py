from pathlib import Path
import pygambit as gbt


def build_geb_trust_game_fig1(f: int = 2) -> gbt.Game:
    """Construct Fig. 1 trust game with prior communication and dishonesty fines."""
    g = gbt.Game.new_tree(
        players=["Player A", "Player B"],
        title="GEB Trust Game Fig. 1"
    )

    # Player B first chooses which message to send.
    g.append_move(g.root, player="Player B", actions=["m(E)", "m(S)", "m(K)"])

    node_mE = g.root.children["m(E)"]
    node_mS = g.root.children["m(S)"]
    node_mK = g.root.children["m(K)"]

    # After observing the message, Player A chooses whether to invest.
    g.append_move(node_mE, player="Player A", actions=["I", "N"])
    g.append_move(node_mS, player="Player A", actions=["I", "N"])
    g.append_move(node_mK, player="Player A", actions=["I", "N"])

    node_mE_I = node_mE.children["I"]
    node_mE_N = node_mE.children["N"]

    node_mS_I = node_mS.children["I"]
    node_mS_N = node_mS.children["N"]

    node_mK_I = node_mK.children["I"]
    node_mK_N = node_mK.children["N"]

    # If Player A does not invest, the game ends immediately.
    out_mE_N = g.add_outcome([2, 0], label="mE_N")
    out_mS_N = g.add_outcome([2, 0], label="mS_N")
    out_mK_N = g.add_outcome([2, 0], label="mK_N")

    g.set_outcome(node_mE_N, out_mE_N)
    g.set_outcome(node_mS_N, out_mS_N)
    g.set_outcome(node_mK_N, out_mK_N)

    # If Player A invests, Player B chooses whether to split or keep.
    g.append_move(node_mE_I, player="Player B", actions=["S", "K"])
    g.append_move(node_mS_I, player="Player B", actions=["S", "K"])
    g.append_move(node_mK_I, player="Player B", actions=["S", "K"])

    # Outcomes after message m(E).
    out_mE_I_S = g.add_outcome([4, 4], label="mE_I_S")
    out_mE_I_K = g.add_outcome([0, 8], label="mE_I_K")

    g.set_outcome(node_mE_I.children["S"], out_mE_I_S)
    g.set_outcome(node_mE_I.children["K"], out_mE_I_K)

    # Outcomes after message m(S).
    out_mS_I_S = g.add_outcome([4, 4], label="mS_I_S")
    out_mS_I_K = g.add_outcome([0, 8 - f], label="mS_I_K")

    g.set_outcome(node_mS_I.children["S"], out_mS_I_S)
    g.set_outcome(node_mS_I.children["K"], out_mS_I_K)

    # Outcomes after message m(K).
    out_mK_I_S = g.add_outcome([4, 4 - f], label="mK_I_S")
    out_mK_I_K = g.add_outcome([0, 8], label="mK_I_K")

    g.set_outcome(node_mK_I.children["S"], out_mK_I_S)
    g.set_outcome(node_mK_I.children["K"], out_mK_I_K)

    return g


if __name__ == "__main__":
    g = build_geb_trust_game_fig1(f=2)

    out_path = Path(__file__).with_name("V148_fig1_v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")



