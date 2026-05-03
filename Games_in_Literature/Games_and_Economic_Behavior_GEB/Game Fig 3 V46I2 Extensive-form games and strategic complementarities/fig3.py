from pathlib import Path
import pygambit as gbt


def build_optional_bos_ii_v0():
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Optional BoS II V0"
    )

    # Player 1 moves first
    g.append_move(g.root, "1", actions=["No", "Yes"])
    node_no = g.root.children["No"]
    node_yes = g.root.children["Yes"]

    # Player 2 moves after No
    g.append_move(node_no, "2", actions=["O", "B"])
    p2_after_no = node_no

    # Player 2 moves after Yes
    g.append_move(node_yes, "2", actions=["O", "B"])
    p2_after_yes = node_yes

    # Player 1 moves after No, without knowing whether player 2 chose O or B
    g.append_move(p2_after_no.children["O"], "1", actions=["O", "B"])
    no_infoset = p2_after_no.children["O"].infoset
    g.append_infoset(p2_after_no.children["B"], no_infoset)

    # Player 1 moves after Yes, without knowing whether player 2 chose O or B
    g.append_move(p2_after_yes.children["O"], "1", actions=["O", "B"])
    yes_infoset = p2_after_yes.children["O"].infoset
    g.append_infoset(p2_after_yes.children["B"], yes_infoset)

    # Distinct outcomes for No branch
    out_no_OO = g.add_outcome([2, 1], label="no_branch_match_O")
    out_no_OB = g.add_outcome([0, 0], label="no_branch_mismatch_OB")
    out_no_BO = g.add_outcome([0, 0], label="no_branch_mismatch_BO")
    out_no_BB = g.add_outcome([1, 2], label="no_branch_match_B")

    # Distinct outcomes for Yes branch
    out_yes_OO = g.add_outcome([2, 1], label="yes_branch_match_O")
    out_yes_OB = g.add_outcome([0, 0], label="yes_branch_mismatch_OB")
    out_yes_BO = g.add_outcome([0, 0], label="yes_branch_mismatch_BO")
    out_yes_BB = g.add_outcome([1, 2], label="yes_branch_match_B")

    # Assign outcomes on No branch
    p1_after_no_O = p2_after_no.children["O"]
    p1_after_no_B = p2_after_no.children["B"]

    g.set_outcome(p1_after_no_O.children["O"], out_no_OO)
    g.set_outcome(p1_after_no_O.children["B"], out_no_OB)
    g.set_outcome(p1_after_no_B.children["O"], out_no_BO)
    g.set_outcome(p1_after_no_B.children["B"], out_no_BB)

    # Assign outcomes on Yes branch
    p1_after_yes_O = p2_after_yes.children["O"]
    p1_after_yes_B = p2_after_yes.children["B"]

    g.set_outcome(p1_after_yes_O.children["O"], out_yes_OO)
    g.set_outcome(p1_after_yes_O.children["B"], out_yes_OB)
    g.set_outcome(p1_after_yes_B.children["O"], out_yes_BO)
    g.set_outcome(p1_after_yes_B.children["B"], out_yes_BB)

    return g


if __name__ == "__main__":
    game = build_optional_bos_ii_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
    