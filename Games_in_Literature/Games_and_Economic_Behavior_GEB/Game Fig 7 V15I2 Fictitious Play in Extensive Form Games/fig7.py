from pathlib import Path
import pygambit as gbt


def build_game06_v0():
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Article Example with Two Updating Paths V0"
    )

    # Player 1 moves first
    g.append_move(g.root, "1", actions=["S", "C", "G"])
    root = g.root

    # Immediate terminal after S
    out_S = g.add_outcome([16, 0], label="choose_S")
    g.set_outcome(root.children["S"], out_S)

    # Player 2 moves after C
    after_C = root.children["C"]
    g.append_move(after_C, "2", actions=["l", "r"])
    p2_infoset = after_C.infoset

    # Player 2 also moves after G, same infoset
    after_G = root.children["G"]
    g.append_infoset(after_G, p2_infoset)

    # Outcomes after C
    out_C_l = g.add_outcome([0, 0], label="C_then_l")
    out_C_r = g.add_outcome([0, 4], label="C_then_r")
    g.set_outcome(after_C.children["l"], out_C_l)
    g.set_outcome(after_C.children["r"], out_C_r)

    # Player 1 moves again after G then l
    after_G_l = after_G.children["l"]
    g.append_move(after_G_l, "1", actions=["L", "R"])
    p1_later_infoset = after_G_l.infoset

    # Player 1 also moves after G then r, same infoset
    after_G_r = after_G.children["r"]
    g.append_infoset(after_G_r, p1_later_infoset)

    # Terminal outcomes after G
    out_G_l_L = g.add_outcome([23, 7], label="G_then_l_then_L")
    out_G_l_R = g.add_outcome([0, 0], label="G_then_l_then_R")
    out_G_r_L = g.add_outcome([0, 0], label="G_then_r_then_L")
    out_G_r_R = g.add_outcome([17, 33], label="G_then_r_then_R")

    g.set_outcome(after_G_l.children["L"], out_G_l_L)
    g.set_outcome(after_G_l.children["R"], out_G_l_R)
    g.set_outcome(after_G_r.children["L"], out_G_r_L)
    g.set_outcome(after_G_r.children["R"], out_G_r_R)

    return g


if __name__ == "__main__":
    game = build_game06_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")
    