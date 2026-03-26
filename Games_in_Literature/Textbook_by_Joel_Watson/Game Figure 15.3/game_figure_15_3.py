from pathlib import Path
import pygambit as gbt


def build_figure_15_3() -> gbt.Game:
    """Construct Watson Figure 15.3: subgames."""
    g = gbt.Game.new_tree(
        players=["1", "2", "3"],
        title="Watson Figure 15.3 - Subgames"
    )

    # Player 1 first chooses U or D.
    g.append_move(g.root, player="1", actions=["U", "D"])

    node_U = g.root.children["U"]
    node_D = g.root.children["D"]

    # After U, Player 2 chooses A or B.
    g.append_move(node_U, player="2", actions=["A", "B"])
    node_UA = node_U.children["A"]
    node_UB = node_U.children["B"]

    # After D, Player 2 chooses C or D.
    g.append_move(node_D, player="2", actions=["C", "D"])
    node_DC = node_D.children["C"]
    node_DD = node_D.children["D"]

    # After U then A, Player 1 chooses E or F.
    g.append_move(node_UA, player="1", actions=["E", "F"])
    node_UAE = node_UA.children["E"]
    node_UAF = node_UA.children["F"]

    # After U then B or D then C, Player 3 chooses G or H at the same information set.
    g.append_move([node_UB, node_DC], player="3", actions=["G", "H"])
    node_UBG = node_UB.children["G"]
    node_UBH = node_UB.children["H"]
    node_DCG = node_DC.children["G"]
    node_DCH = node_DC.children["H"]

    # Terminal rewards in the order (Player 1, Player 2, Player 3).
    outcome_UAE = g.add_outcome([3, 3, 6], label="UAE")
    outcome_UAF = g.add_outcome([1, 5, 7], label="UAF")
    outcome_UBG = g.add_outcome([2, 0, 3], label="UBG")
    outcome_UBH = g.add_outcome([7, 7, 2], label="UBH")
    outcome_DCG = g.add_outcome([0, 6, 1], label="DCG")
    outcome_DCH = g.add_outcome([8, 6, 0], label="DCH")
    outcome_DD = g.add_outcome([6, 2, 4], label="DD")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_UAE, outcome_UAE)
    g.set_outcome(node_UAF, outcome_UAF)
    g.set_outcome(node_UBG, outcome_UBG)
    g.set_outcome(node_UBH, outcome_UBH)
    g.set_outcome(node_DCG, outcome_DCG)
    g.set_outcome(node_DCH, outcome_DCH)
    g.set_outcome(node_DD, outcome_DD)

    return g


if __name__ == "__main__":
    g = build_figure_15_3()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("figure_15_3.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")


    