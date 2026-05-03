from pathlib import Path
import pygambit as gbt


def build_geb_investment_true_ii_fig2_distinct_terminals() -> gbt.Game:
    """Construct Fig. 2 with distinct terminal outcome labels for every leaf."""
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Investment True II Fig. 2"
    )

    # Prior used in the paper's worked example:
    # rho(01)=rho(11)=rho(21)=1/3 and rho(02)=1/10, rho(12)=9/10, independently.
    g.append_move(
        g.root,
        g.players.chance,
        actions=["01_02", "01_12", "11_02", "11_12", "21_02", "21_12"]
    )
    g.set_chance_probs(
        g.root.infoset,
        [
            gbt.Rational("1/30"),
            gbt.Rational("3/10"),
            gbt.Rational("1/30"),
            gbt.Rational("3/10"),
            gbt.Rational("1/30"),
            gbt.Rational("3/10"),
        ]
    )

    # Chance branches.
    node_0102 = g.root.children["01_02"]
    node_0112 = g.root.children["01_12"]
    node_1102 = g.root.children["11_02"]
    node_1112 = g.root.children["11_12"]
    node_2102 = g.root.children["21_02"]
    node_2112 = g.root.children["21_12"]

    # Stage 1: Player 1 types 01, 11, 21.
    # Each Player 1 type knows own type and prior realized actions,
    # but not Player 2's type.
    g.append_move(node_0102, player="Player 1", actions=["Invest1", "Out1"])
    g.append_infoset(node_0112, node_0102.infoset)

    g.append_move(node_1102, player="Player 1", actions=["Invest1", "Out1"])
    g.append_infoset(node_1112, node_1102.infoset)

    g.append_move(node_2102, player="Player 1", actions=["Invest1", "Out1"])
    g.append_infoset(node_2112, node_2102.infoset)

    # Distinct terminal outcomes after Out1.
    out_0102_out1 = g.add_outcome([5, 0], label="01_02_Out1")
    out_0112_out1 = g.add_outcome([5, 0], label="01_12_Out1")
    out_1102_out1 = g.add_outcome([5, 0], label="11_02_Out1")
    out_1112_out1 = g.add_outcome([5, 0], label="11_12_Out1")
    out_2102_out1 = g.add_outcome([5, 0], label="21_02_Out1")
    out_2112_out1 = g.add_outcome([5, 0], label="21_12_Out1")

    g.set_outcome(node_0102.children["Out1"], out_0102_out1)
    g.set_outcome(node_0112.children["Out1"], out_0112_out1)
    g.set_outcome(node_1102.children["Out1"], out_1102_out1)
    g.set_outcome(node_1112.children["Out1"], out_1112_out1)
    g.set_outcome(node_2102.children["Out1"], out_2102_out1)
    g.set_outcome(node_2112.children["Out1"], out_2112_out1)

    # Stage 2: Player 2 types 02 and 12 after Invest1.
    # Each Player 2 type knows own type and prior realized actions,
    # but not Player 1's type.
    node_0102_I1 = node_0102.children["Invest1"]
    node_0112_I1 = node_0112.children["Invest1"]
    node_1102_I1 = node_1102.children["Invest1"]
    node_1112_I1 = node_1112.children["Invest1"]
    node_2102_I1 = node_2102.children["Invest1"]
    node_2112_I1 = node_2112.children["Invest1"]

    g.append_move(node_0102_I1, player="Player 2", actions=["Invest2", "Out2"])
    g.append_infoset(node_1102_I1, node_0102_I1.infoset)
    g.append_infoset(node_2102_I1, node_0102_I1.infoset)

    g.append_move(node_0112_I1, player="Player 2", actions=["Invest2", "Out2"])
    g.append_infoset(node_1112_I1, node_0112_I1.infoset)
    g.append_infoset(node_2112_I1, node_0112_I1.infoset)

    # Distinct terminal outcomes after Out2.
    out_0102_out2 = g.add_outcome([0, 6], label="01_02_Invest1_Out2")
    out_0112_out2 = g.add_outcome([0, 6], label="01_12_Invest1_Out2")
    out_1102_out2 = g.add_outcome([0, 6], label="11_02_Invest1_Out2")
    out_1112_out2 = g.add_outcome([0, 6], label="11_12_Invest1_Out2")
    out_2102_out2 = g.add_outcome([0, 6], label="21_02_Invest1_Out2")
    out_2112_out2 = g.add_outcome([0, 6], label="21_12_Invest1_Out2")

    g.set_outcome(node_0102_I1.children["Out2"], out_0102_out2)
    g.set_outcome(node_0112_I1.children["Out2"], out_0112_out2)
    g.set_outcome(node_1102_I1.children["Out2"], out_1102_out2)
    g.set_outcome(node_1112_I1.children["Out2"], out_1112_out2)
    g.set_outcome(node_2102_I1.children["Out2"], out_2102_out2)
    g.set_outcome(node_2112_I1.children["Out2"], out_2112_out2)

    # Stage 3: Player 1 types 01, 11, 21 after Invest1, Invest2.
    # Each Player 1 type again knows own type and realized actions,
    # but not Player 2's type.
    node_0102_I2 = node_0102_I1.children["Invest2"]
    node_0112_I2 = node_0112_I1.children["Invest2"]
    node_1102_I2 = node_1102_I1.children["Invest2"]
    node_1112_I2 = node_1112_I1.children["Invest2"]
    node_2102_I2 = node_2102_I1.children["Invest2"]
    node_2112_I2 = node_2112_I1.children["Invest2"]

    g.append_move(node_0102_I2, player="Player 1", actions=["Invest3", "Out3"])
    g.append_infoset(node_0112_I2, node_0102_I2.infoset)

    g.append_move(node_1102_I2, player="Player 1", actions=["Invest3", "Out3"])
    g.append_infoset(node_1112_I2, node_1102_I2.infoset)

    g.append_move(node_2102_I2, player="Player 1", actions=["Invest3", "Out3"])
    g.append_infoset(node_2112_I2, node_2102_I2.infoset)

    # Distinct terminal outcomes after Invest3 and Out3.
    out_0102_invest3 = g.add_outcome([8, 8], label="01_02_Invest1_Invest2_Invest3")
    out_0102_out3 = g.add_outcome([7, 0], label="01_02_Invest1_Invest2_Out3")

    out_0112_invest3 = g.add_outcome([8, 8], label="01_12_Invest1_Invest2_Invest3")
    out_0112_out3 = g.add_outcome([7, 0], label="01_12_Invest1_Invest2_Out3")

    out_1102_invest3 = g.add_outcome([8, 8], label="11_02_Invest1_Invest2_Invest3")
    out_1102_out3 = g.add_outcome([7, 0], label="11_02_Invest1_Invest2_Out3")

    out_1112_invest3 = g.add_outcome([8, 8], label="11_12_Invest1_Invest2_Invest3")
    out_1112_out3 = g.add_outcome([7, 0], label="11_12_Invest1_Invest2_Out3")

    out_2102_invest3 = g.add_outcome([8, 8], label="21_02_Invest1_Invest2_Invest3")
    out_2102_out3 = g.add_outcome([7, 0], label="21_02_Invest1_Invest2_Out3")

    out_2112_invest3 = g.add_outcome([8, 8], label="21_12_Invest1_Invest2_Invest3")
    out_2112_out3 = g.add_outcome([7, 0], label="21_12_Invest1_Invest2_Out3")

    g.set_outcome(node_0102_I2.children["Invest3"], out_0102_invest3)
    g.set_outcome(node_0102_I2.children["Out3"], out_0102_out3)

    g.set_outcome(node_0112_I2.children["Invest3"], out_0112_invest3)
    g.set_outcome(node_0112_I2.children["Out3"], out_0112_out3)

    g.set_outcome(node_1102_I2.children["Invest3"], out_1102_invest3)
    g.set_outcome(node_1102_I2.children["Out3"], out_1102_out3)

    g.set_outcome(node_1112_I2.children["Invest3"], out_1112_invest3)
    g.set_outcome(node_1112_I2.children["Out3"], out_1112_out3)

    g.set_outcome(node_2102_I2.children["Invest3"], out_2102_invest3)
    g.set_outcome(node_2102_I2.children["Out3"], out_2102_out3)

    g.set_outcome(node_2112_I2.children["Invest3"], out_2112_invest3)
    g.set_outcome(node_2112_I2.children["Out3"], out_2112_out3)

    return g


if __name__ == "__main__":
    g = build_geb_investment_true_ii_fig2_distinct_terminals()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    
