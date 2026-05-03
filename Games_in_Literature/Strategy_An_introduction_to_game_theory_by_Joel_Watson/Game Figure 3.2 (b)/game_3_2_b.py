from pathlib import Path
import pygambit as gbt


def build_3_2_b() -> gbt.Game:
    """Construct Watson Figure 3.2(b)."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 3.2(b)"
    )

    # Player 1 chooses A, B, or C.
    g.append_move(g.root, player="1", actions=["A", "B", "C"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]
    node_C = g.root.children["C"]

    # After A or B, Player 2 chooses X or Y without knowing whether A or B was chosen.
    g.append_move([node_A, node_B], player="2", actions=["X", "Y"])

    AX = node_A.children["X"]
    AY = node_A.children["Y"]
    BX = node_B.children["X"]
    BY = node_B.children["Y"]

    # After C, Player 1 chooses W or Z.
    g.append_move(node_C, player="1", actions=["W", "Z"])

    CW = node_C.children["W"]
    CZ = node_C.children["Z"]

    # Terminal outcomes in the order (Player 1, Player 2).
    o_AX = g.add_outcome([2, 5], label="AX")
    o_AY = g.add_outcome([5, 2], label="AY")
    o_BX = g.add_outcome([5, 2], label="BX")
    o_BY = g.add_outcome([2, 5], label="BY")
    o_CW = g.add_outcome([2, 2], label="CW")
    o_CZ = g.add_outcome([3, 3], label="CZ")

    # Attach outcomes.
    g.set_outcome(AX, o_AX)
    g.set_outcome(AY, o_AY)
    g.set_outcome(BX, o_BX)
    g.set_outcome(BY, o_BY)
    g.set_outcome(CW, o_CW)
    g.set_outcome(CZ, o_CZ)

    return g


if __name__ == "__main__":
    g = build_3_2_b()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("figure_3_2_b.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    