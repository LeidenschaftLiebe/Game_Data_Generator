from pathlib import Path
import pygambit as gbt


def build_multiselves_agent_form_absentminded_driver():
    g = gbt.Game.new_tree(
        players=["Agent 1", "Agent 2", "Agent 3"],
        title="GEB Multiselves Agent Form of the Absentminded Driver and the Policeman Fig. 4"
    )

    # Nature chooses which ordering of Agent 1 / Agent 2 is used
    g.append_move(g.root, g.players.chance, actions=["LeftOrder", "RightOrder"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    left_order = g.root.children["LeftOrder"]
    right_order = g.root.children["RightOrder"]

    # Agent 1 top-left decision
    g.append_move(left_order, player="Agent 1", actions=["C1", "E1"])
    left_a1_c1 = left_order.children["C1"]
    left_a1_e1 = left_order.children["E1"]

    # Agent 2 top-right decision
    g.append_move(right_order, player="Agent 2", actions=["C2", "E2"])
    right_a2_c2 = right_order.children["C2"]
    right_a2_e2 = right_order.children["E2"]

    # Agent 2 lower-left decision shares infoset with Agent 2 top-right decision
    g.append_infoset(left_a1_c1, right_order.infoset)
    left_a2_c2 = left_a1_c1.children["C2"]
    left_a2_e2 = left_a1_c1.children["E2"]

    # Agent 1 lower-right decision shares infoset with Agent 1 top-left decision
    g.append_infoset(right_a2_c2, left_order.infoset)
    right_a1_c1 = right_a2_c2.children["C1"]
    right_a1_e1 = right_a2_c2.children["E1"]

    # Agent 3's four nodes are all in one infoset
    g.append_move(left_a1_e1, player="Agent 3", actions=["H", "E"])
    g.append_infoset(left_a2_c2, left_a1_e1.infoset)
    g.append_infoset(right_a1_c1, left_a1_e1.infoset)
    g.append_infoset(right_a2_e2, left_a1_e1.infoset)

    # Outcomes
    # Left side
    out_left_c1_c2_h = g.add_outcome([0, 0, 0], label="Left_C1_C2_H")
    out_left_c1_c2_e = g.add_outcome([1, 1, -1], label="Left_C1_C2_E")
    out_left_c1_e2 = g.add_outcome([0, 0, 0], label="Left_C1_E2")
    out_left_e1_h = g.add_outcome([1, 1, -1], label="Left_E1_H")
    out_left_e1_e = g.add_outcome([0, 0, 0], label="Left_E1_E")

    # Right side
    out_right_c2_c1_h = g.add_outcome([0, 0, 0], label="Right_C2_C1_H")
    out_right_c2_c1_e = g.add_outcome([1, 1, -1], label="Right_C2_C1_E")
    out_right_c2_e1 = g.add_outcome([0, 0, 0], label="Right_C2_E1")
    out_right_e2_h = g.add_outcome([1, 1, -1], label="Right_E2_H")
    out_right_e2_e = g.add_outcome([0, 0, 0], label="Right_E2_E")

    # Assign outcomes
    g.set_outcome(left_a2_c2.children["H"], out_left_c1_c2_h)
    g.set_outcome(left_a2_c2.children["E"], out_left_c1_c2_e)
    g.set_outcome(left_a2_e2, out_left_c1_e2)
    g.set_outcome(left_a1_e1.children["H"], out_left_e1_h)
    g.set_outcome(left_a1_e1.children["E"], out_left_e1_e)

    g.set_outcome(right_a1_c1.children["H"], out_right_c2_c1_h)
    g.set_outcome(right_a1_c1.children["E"], out_right_c2_c1_e)
    g.set_outcome(right_a1_e1, out_right_c2_e1)
    g.set_outcome(right_a2_e2.children["H"], out_right_e2_h)
    g.set_outcome(right_a2_e2.children["E"], out_right_e2_e)

    return g


if __name__ == "__main__":
    g = build_multiselves_agent_form_absentminded_driver()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

