from pathlib import Path
import pygambit as gbt


def build_exercise_11() -> gbt.Game:
    """Construct Exercise 11."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Exercise 11"
    )

    # Player 1 first chooses A or B.
    g.append_move(g.root, player="1", actions=["A", "B"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]

    # After A, Player 2 chooses C or D.
    g.append_move(node_A, player="2", actions=["C", "D"])
    node_AC = node_A.children["C"]
    node_AD = node_A.children["D"]

    # After B, Player 2 chooses E or F.
    g.append_move(node_B, player="2", actions=["E", "F"])
    node_BE = node_B.children["E"]
    node_BF = node_B.children["F"]

    # After A then C, Player 1 chooses G or H.
    g.append_move(node_AC, player="1", actions=["G", "H"])
    node_ACG = node_AC.children["G"]
    node_ACH = node_AC.children["H"]

    # After A then D, Player 1 chooses I or J.
    g.append_move(node_AD, player="1", actions=["I", "J"])
    node_ADI = node_AD.children["I"]
    node_ADJ = node_AD.children["J"]

    # After B then E, Player 1 chooses K or L.
    g.append_move(node_BE, player="1", actions=["K", "L"])
    node_BEK = node_BE.children["K"]
    node_BEL = node_BE.children["L"]

    # After B then F, Player 1 chooses M or N.
    g.append_move(node_BF, player="1", actions=["M", "N"])
    node_BFM = node_BF.children["M"]
    node_BFN = node_BF.children["N"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_ACG = g.add_outcome([3, 4], label="ACG")
    outcome_ACH = g.add_outcome([4, 3], label="ACH")
    outcome_ADI = g.add_outcome([1, 2], label="ADI")
    outcome_ADJ = g.add_outcome([5, 7], label="ADJ")
    outcome_BEK = g.add_outcome([6, 5], label="BEK")
    outcome_BEL = g.add_outcome([2, 8], label="BEL")
    outcome_BFM = g.add_outcome([9, 1], label="BFM")
    outcome_BFN = g.add_outcome([3, 6], label="BFN")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_ACG, outcome_ACG)
    g.set_outcome(node_ACH, outcome_ACH)
    g.set_outcome(node_ADI, outcome_ADI)
    g.set_outcome(node_ADJ, outcome_ADJ)
    g.set_outcome(node_BEK, outcome_BEK)
    g.set_outcome(node_BEL, outcome_BEL)
    g.set_outcome(node_BFM, outcome_BFM)
    g.set_outcome(node_BFN, outcome_BFN)

    return g


if __name__ == "__main__":
    g = build_exercise_11()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_11.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")


    