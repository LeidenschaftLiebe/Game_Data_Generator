from pathlib import Path
import pygambit as gbt


def build_exercise_3() -> gbt.Game:
    """Construct Page 200, Exercise 3."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Page 200 Exercise 3"
    )

    # Player 1 first chooses A or B.
    g.append_move(g.root, player="1", actions=["A", "B"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]

    # If Player 1 chooses B, the game ends immediately.
    outcome_B = g.add_outcome([5, 4], label="B")
    g.set_outcome(node_B, outcome_B)

    # After A, Player 2 chooses C or D.
    g.append_move(node_A, player="2", actions=["C", "D"])
    node_AC = node_A.children["C"]
    node_AD = node_A.children["D"]

    # After A then D, Player 1 chooses I or J.
    g.append_move(node_AD, player="1", actions=["I", "J"])
    node_ADI = node_AD.children["I"]
    node_ADJ = node_AD.children["J"]

    # After A then C, Player 1 chooses G or H.
    g.append_move(node_AC, player="1", actions=["G", "H"])
    node_ACG = node_AC.children["G"]
    node_ACH = node_AC.children["H"]

    # If Player 1 chooses H after A then C, the game ends.
    outcome_ACH = g.add_outcome([7, 3], label="ACH")
    g.set_outcome(node_ACH, outcome_ACH)

    # If Player 1 chooses G after A then C, Player 2 chooses E or F.
    g.append_move(node_ACG, player="2", actions=["E", "F"])
    node_ACGE = node_ACG.children["E"]
    node_ACGF = node_ACG.children["F"]

    # After A-C-G-E, Player 1 chooses K or L.
    g.append_move(node_ACGE, player="1", actions=["K", "L"])
    node_ACGEK = node_ACGE.children["K"]
    node_ACGEL = node_ACGE.children["L"]

    # After A-C-G-F, Player 1 chooses M or N.
    g.append_move(node_ACGF, player="1", actions=["M", "N"])
    node_ACGFM = node_ACGF.children["M"]
    node_ACGFN = node_ACGF.children["N"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_ADI = g.add_outcome([9, 2], label="ADI")
    outcome_ADJ = g.add_outcome([4, 5], label="ADJ")
    outcome_ACGEK = g.add_outcome([2, 4], label="ACGEK")
    outcome_ACGEL = g.add_outcome([3, 6], label="ACGEL")
    outcome_ACGFM = g.add_outcome([6, 7], label="ACGFM")
    outcome_ACGFN = g.add_outcome([8, 1], label="ACGFN")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_ADI, outcome_ADI)
    g.set_outcome(node_ADJ, outcome_ADJ)
    g.set_outcome(node_ACGEK, outcome_ACGEK)
    g.set_outcome(node_ACGEL, outcome_ACGEL)
    g.set_outcome(node_ACGFM, outcome_ACGFM)
    g.set_outcome(node_ACGFN, outcome_ACGFN)

    return g


if __name__ == "__main__":
    g = build_exercise_3()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_3.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")