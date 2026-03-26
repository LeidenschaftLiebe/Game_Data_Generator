from pathlib import Path
import pygambit as gbt


def build_3_2_a() -> gbt.Game:
    """Construct Watson Figure 3.2(a)."""
    g = gbt.Game.new_tree(
        players=["1", "2", "3"],
        title="Watson Figure 3.2(a)"
    )

    # Player 1 chooses action U or D.
    g.append_move(g.root, player="1", actions=["U", "D"])

    node_U = g.root.children["U"]
    node_D = g.root.children["D"]

    # Player 2 moves after U.
    g.append_move(node_U, player="2", actions=["A", "B"])
    node_A = node_U.children["A"]
    node_B = node_U.children["B"]

    # Player 2 moves after D.
    g.append_move(node_D, player="2", actions=["C", "E"])
    node_C = node_D.children["C"]
    node_E = node_D.children["E"]

    # Player 3 moves after A with actions R and T.
    g.append_move(node_A, player="3", actions=["R", "T"])
    node_R = node_A.children["R"]
    node_T = node_A.children["T"]

    # Player 3 moves after B or C with actions P and Q,
    # and these two decision nodes are in the same information set.
    g.append_move([node_B, node_C], player="3", actions=["P", "Q"])

    node_BP = node_B.children["P"]
    node_BQ = node_B.children["Q"]
    node_CP = node_C.children["P"]
    node_CQ = node_C.children["Q"]

    # Terminal outcomes in the order (1, 2, 3).
    o_R = g.add_outcome([9, 2, 5], label="R")
    o_T = g.add_outcome([2, 4, 4], label="T")
    o_BP = g.add_outcome([0, 5, 4], label="BP")
    o_BQ = g.add_outcome([3, 0, 0], label="BQ")
    o_CP = g.add_outcome([2, 2, 2], label="CP")
    o_CQ = g.add_outcome([1, 2, 2], label="CQ")
    o_E = g.add_outcome([6, 3, 2], label="E")

    # Attach outcomes.
    g.set_outcome(node_R, o_R)
    g.set_outcome(node_T, o_T)
    g.set_outcome(node_BP, o_BP)
    g.set_outcome(node_BQ, o_BQ)
    g.set_outcome(node_CP, o_CP)
    g.set_outcome(node_CQ, o_CQ)
    g.set_outcome(node_E, o_E)

    return g


if __name__ == "__main__":
    g = build_3_2_a()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("figure_3_2_a.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    