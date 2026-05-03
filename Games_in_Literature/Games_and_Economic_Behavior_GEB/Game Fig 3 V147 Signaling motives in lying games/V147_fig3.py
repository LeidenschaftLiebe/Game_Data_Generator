from pathlib import Path
import pygambit as gbt


def build_geb_fig3_selection_game(
    p: str = "1/2",
    q: str = "1/2",
    epsilon: str = "1/10",
    y1: int = 0,
    y2: int = 2,
) -> gbt.Game:
    """Construct Fig. 3 selection game with instantiated parameters."""
    g = gbt.Game.new_tree(
        players=["Agent"],
        title="GEB Fig. 3 Selection Game"
    )

    p_r = gbt.Rational(p)
    q_r = gbt.Rational(q)
    e_r = gbt.Rational(epsilon)

    # The agent first decides whether to indicate interest in the lying stage.
    g.append_move(g.root, player="Agent", actions=["i=0", "i=1"])

    node_i0 = g.root.children["i=0"]
    node_i1 = g.root.children["i=1"]

    # After i=0, chance chooses z=1 with probability epsilon and z=2 otherwise.
    g.append_move(node_i0, player=g.players.chance, actions=["z=1", "z=2"])
    g.set_chance_probs(node_i0.infoset, [e_r, 1 - e_r])

    # After i=1, chance chooses z=1 with probability q+epsilon and z=3 otherwise.
    g.append_move(node_i1, player=g.players.chance, actions=["z=1", "z=3"])
    g.set_chance_probs(node_i1.infoset, [q_r + e_r, 1 - q_r - e_r])

    node_i0_z1 = node_i0.children["z=1"]
    node_i0_z2 = node_i0.children["z=2"]

    node_i1_z1 = node_i1.children["z=1"]
    node_i1_z3 = node_i1.children["z=3"]

    # Nature then draws the hidden state j in every branch.
    for node in [node_i0_z1, node_i0_z2, node_i1_z1, node_i1_z3]:
        g.append_move(node, player=g.players.chance, actions=["j=1", "j=2"])
        g.set_chance_probs(node.infoset, [1 - p_r, p_r])

    # If z=2 or z=3, the agent does not report and simply receives y(j).
    node_i0_z2_j1 = node_i0_z2.children["j=1"]
    node_i0_z2_j2 = node_i0_z2.children["j=2"]
    node_i1_z3_j1 = node_i1_z3.children["j=1"]
    node_i1_z3_j2 = node_i1_z3.children["j=2"]

    out_i0_z2_j1 = g.add_outcome([y1], label="i0_z2_j1")
    out_i0_z2_j2 = g.add_outcome([y2], label="i0_z2_j2")
    out_i1_z3_j1 = g.add_outcome([y1], label="i1_z3_j1")
    out_i1_z3_j2 = g.add_outcome([y2], label="i1_z3_j2")

    g.set_outcome(node_i0_z2_j1, out_i0_z2_j1)
    g.set_outcome(node_i0_z2_j2, out_i0_z2_j2)
    g.set_outcome(node_i1_z3_j1, out_i1_z3_j1)
    g.set_outcome(node_i1_z3_j2, out_i1_z3_j2)

    # If z=1, the agent reaches the reporting stage after seeing j.
    node_i0_z1_j1 = node_i0_z1.children["j=1"]
    node_i0_z1_j2 = node_i0_z1.children["j=2"]
    node_i1_z1_j1 = node_i1_z1.children["j=1"]
    node_i1_z1_j2 = node_i1_z1.children["j=2"]

    for node in [node_i0_z1_j1, node_i0_z1_j2, node_i1_z1_j1, node_i1_z1_j2]:
        g.append_move(node, player="Agent", actions=["a=1", "a=2"])

    # Reporting determines the final material result.
    report_nodes = [
        (node_i0_z1_j1, "i0_z1_j1"),
        (node_i0_z1_j2, "i0_z1_j2"),
        (node_i1_z1_j1, "i1_z1_j1"),
        (node_i1_z1_j2, "i1_z1_j2"),
    ]

    for node, prefix in report_nodes:
        out_a1 = g.add_outcome([y1], label=f"{prefix}_a1")
        out_a2 = g.add_outcome([y2], label=f"{prefix}_a2")
        g.set_outcome(node.children["a=1"], out_a1)
        g.set_outcome(node.children["a=2"], out_a2)

    return g


if __name__ == "__main__":
    g = build_geb_fig3_selection_game(
        p="1/2",
        q="1/2",
        epsilon="1/10",
        y1=0,
        y2=2,
    )

    out_path = Path(__file__).with_name("game_fig3_v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    