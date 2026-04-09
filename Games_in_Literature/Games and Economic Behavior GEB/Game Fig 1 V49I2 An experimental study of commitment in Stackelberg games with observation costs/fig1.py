from pathlib import Path
import pygambit as gbt


def build_costly_leader_game_v0():
    # Article treatment values are epsilon in {1, 15, 30, 45, 60}.
    # We use epsilon = 30 as a concrete V0 instance.
    epsilon = 30

    g = gbt.Game.new_tree(
        players=["Leader", "Follower"],
        title="Costly Leader Game V0 (epsilon=30)"
    )

    # Leader moves first
    g.append_move(g.root, "Leader", actions=["S", "C"])
    node_S = g.root.children["S"]
    node_C = g.root.children["C"]

    # Follower chooses whether to observe, without knowing anything new beyond own position
    g.append_move(node_S, "Follower", actions=["Observe", "NotObserve"])
    g.append_infoset(node_C, node_S.infoset)

    foll_after_S = node_S
    foll_after_C = node_C

    # If follower observes after S, follower then chooses s or c knowing leader chose S
    obs_after_S = foll_after_S.children["Observe"]
    g.append_move(obs_after_S, "Follower", actions=["s", "c"])

    # If follower does not observe after S, follower chooses s or c without observing
    noobs_after_S = foll_after_S.children["NotObserve"]
    g.append_move(noobs_after_S, "Follower", actions=["s", "c"])
    noobs_infoset = noobs_after_S.infoset

    # If follower does not observe after C, same hidden decision situation as after S and NotObserve
    noobs_after_C = foll_after_C.children["NotObserve"]
    g.append_infoset(noobs_after_C, noobs_infoset)

    # If follower observes after C, follower then chooses s or c knowing leader chose C
    obs_after_C = foll_after_C.children["Observe"]
    g.append_move(obs_after_C, "Follower", actions=["s", "c"])

    # Outcomes
    out_S_obs_s = g.add_outcome([500, 200 - epsilon], label="S_Observe_s")
    out_S_obs_c = g.add_outcome([300, 100 - epsilon], label="S_Observe_c")
    out_S_noobs_s = g.add_outcome([500, 200], label="S_NotObserve_s")
    out_S_noobs_c = g.add_outcome([300, 100], label="S_NotObserve_c")

    out_C_noobs_s = g.add_outcome([600, 300], label="C_NotObserve_s")
    out_C_noobs_c = g.add_outcome([400, 400], label="C_NotObserve_c")
    out_C_obs_s = g.add_outcome([600, 300 - epsilon], label="C_Observe_s")
    out_C_obs_c = g.add_outcome([400, 400 - epsilon], label="C_Observe_c")

    g.set_outcome(obs_after_S.children["s"], out_S_obs_s)
    g.set_outcome(obs_after_S.children["c"], out_S_obs_c)
    g.set_outcome(noobs_after_S.children["s"], out_S_noobs_s)
    g.set_outcome(noobs_after_S.children["c"], out_S_noobs_c)

    g.set_outcome(noobs_after_C.children["s"], out_C_noobs_s)
    g.set_outcome(noobs_after_C.children["c"], out_C_noobs_c)
    g.set_outcome(obs_after_C.children["s"], out_C_obs_s)
    g.set_outcome(obs_after_C.children["c"], out_C_obs_c)

    return g


if __name__ == "__main__":
    game = build_costly_leader_game_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

    