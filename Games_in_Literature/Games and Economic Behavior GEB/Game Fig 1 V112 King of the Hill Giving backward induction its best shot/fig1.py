from pathlib import Path
import pygambit as gbt


def build_koh_line_game_v0():
    g = gbt.Game.new_tree(
        players=["Subject 1", "Subject 2", "Subject 3", "Subject 4"],
        title="GEB Fig. 1 Prediction Line Game N=4 V0"
    )

    # Subject 1
    g.append_move(g.root, "Subject 1", actions=["Stay", "Charge"])
    s1_stay = g.root.children["Stay"]
    s1_charge = g.root.children["Charge"]

    # Subject 2
    g.append_move(s1_charge, "Subject 2", actions=["Stay", "Charge"])
    s2_stay = s1_charge.children["Stay"]
    s2_charge = s1_charge.children["Charge"]

    # Subject 3
    g.append_move(s2_charge, "Subject 3", actions=["Stay", "Charge"])
    s3_stay = s2_charge.children["Stay"]
    s3_charge = s2_charge.children["Charge"]

    # Subject 4
    g.append_move(s3_charge, "Subject 4", actions=["Stay", "Charge"])
    s4_stay = s3_charge.children["Stay"]
    s4_charge = s3_charge.children["Charge"]

    # Outcomes
    out_s1_stay = g.add_outcome([4, 4, 4, 4], label="Stay")
    out_s2_stay = g.add_outcome([8, 4, 4, 4], label="Charge_Stay")
    out_s3_stay = g.add_outcome([0, 8, 4, 4], label="Charge_Charge_Stay")
    out_s4_stay = g.add_outcome([0, 0, 8, 4], label="Charge_Charge_Charge_Stay")
    out_s4_charge = g.add_outcome([0, 0, 0, 8], label="Charge_Charge_Charge_Charge")

    # Assign outcomes
    g.set_outcome(s1_stay, out_s1_stay)
    g.set_outcome(s2_stay, out_s2_stay)
    g.set_outcome(s3_stay, out_s3_stay)
    g.set_outcome(s4_stay, out_s4_stay)
    g.set_outcome(s4_charge, out_s4_charge)

    return g


if __name__ == "__main__":
    g = build_koh_line_game_v0()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



