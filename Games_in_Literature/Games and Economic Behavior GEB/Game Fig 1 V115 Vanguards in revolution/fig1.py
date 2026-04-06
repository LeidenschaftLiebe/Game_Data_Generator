from pathlib import Path
import pygambit as gbt


def build_vanguard_citizen_game():
    g = gbt.Game.new_tree(
        players=["Vanguard", "Citizen"],
        title="GEB Vanguard-Citizen Game Fig. 1"
    )

    # Parameter values
    h1 = 1
    h2 = 2
    w1 = 3
    l2 = 0
    l1 = 0
    w2 = 3
    theta = 2
    z = 1

    # Vanguard moves first
    g.append_move(g.root, player="Vanguard", actions=["NoRevolt", "Revolt"])
    node_no_revolt = g.root.children["NoRevolt"]
    node_revolt = g.root.children["Revolt"]

    # Citizen moves after observing the vanguard's choice
    g.append_move(node_no_revolt, player="Citizen", actions=["NoRevolt", "Revolt"])
    g.append_move(node_revolt, player="Citizen", actions=["NoRevolt", "Revolt"])

    # Outcomes
    out_no_no = g.add_outcome([h1, h2], label="NoRevolt_NoRevolt")
    out_no_yes = g.add_outcome([w1, l2], label="NoRevolt_Revolt")
    out_yes_no = g.add_outcome([l1, w2], label="Revolt_NoRevolt")
    out_yes_yes = g.add_outcome([theta + z, theta], label="Revolt_Revolt")

    g.set_outcome(node_no_revolt.children["NoRevolt"], out_no_no)
    g.set_outcome(node_no_revolt.children["Revolt"], out_no_yes)
    g.set_outcome(node_revolt.children["NoRevolt"], out_yes_no)
    g.set_outcome(node_revolt.children["Revolt"], out_yes_yes)

    return g


if __name__ == "__main__":
    g = build_vanguard_citizen_game()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


