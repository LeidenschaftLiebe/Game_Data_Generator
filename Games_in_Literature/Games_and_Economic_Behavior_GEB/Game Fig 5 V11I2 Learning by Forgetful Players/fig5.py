from pathlib import Path
import pygambit as gbt


def build_fig5_v0():
    g = gbt.Game.new_tree(
        players=["1", "2", "3"],
        title="Burn 0 or Burn 1 V0"
    )

    # Player 3 moves first
    g.append_move(g.root, "3", actions=["burn0", "burn1"])
    root = g.root

    # Left subgame after burn 0
    burn0 = root.children["burn0"]
    g.append_move(burn0, "1", actions=["L", "R"])

    burn0_L = burn0.children["L"]
    burn0_R = burn0.children["R"]

    # Player 2 infoset after burn 0
    g.append_move(burn0_L, "2", actions=["l", "r"])
    burn0_p2_infoset = burn0_L.infoset
    g.append_infoset(burn0_R, burn0_p2_infoset)

    # Outcomes after burn 0
    out_burn0_L_l = g.add_outcome([3, 3, 3], label="burn0_L_l")
    out_burn0_L_r = g.add_outcome([0, 0, 0], label="burn0_L_r")
    out_burn0_R_l = g.add_outcome([0, 0, 0], label="burn0_R_l")
    out_burn0_R_r = g.add_outcome([1, 1, 1], label="burn0_R_r")

    g.set_outcome(burn0_L.children["l"], out_burn0_L_l)
    g.set_outcome(burn0_L.children["r"], out_burn0_L_r)
    g.set_outcome(burn0_R.children["l"], out_burn0_R_l)
    g.set_outcome(burn0_R.children["r"], out_burn0_R_r)

    # Right subgame after burn 1
    burn1 = root.children["burn1"]
    g.append_move(burn1, "1", actions=["L", "R"])

    burn1_L = burn1.children["L"]
    burn1_R = burn1.children["R"]

    # Player 2 infoset after burn 1
    g.append_move(burn1_L, "2", actions=["l", "r"])
    burn1_p2_infoset = burn1_L.infoset
    g.append_infoset(burn1_R, burn1_p2_infoset)

    # Outcomes after burn 1
    out_burn1_L_l = g.add_outcome([3, 3, 2], label="burn1_L_l")
    out_burn1_L_r = g.add_outcome([0, 0, -1], label="burn1_L_r")
    out_burn1_R_l = g.add_outcome([0, 0, -1], label="burn1_R_l")
    out_burn1_R_r = g.add_outcome([1, 1, 0], label="burn1_R_r")

    g.set_outcome(burn1_L.children["l"], out_burn1_L_l)
    g.set_outcome(burn1_L.children["r"], out_burn1_L_r)
    g.set_outcome(burn1_R.children["l"], out_burn1_R_l)
    g.set_outcome(burn1_R.children["r"], out_burn1_R_r)

    return g


if __name__ == "__main__":
    game = build_fig5_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


    