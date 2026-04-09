from pathlib import Path
import pygambit as gbt


def build_entry_game_imperfect_monitoring_v0():
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Entry Game with Imperfect Monitoring V0"
    )

    # Player 1 moves first
    g.append_move(g.root, "1", actions=["O", "S", "B"])

    node_O = g.root.children["O"]
    node_S = g.root.children["S"]
    node_B = g.root.children["B"]

    # Immediate outcome after O
    out_O = g.add_outcome([0, 6], label="choose_O")
    g.set_outcome(node_O, out_O)

    # Player 2 moves after S
    g.append_move(node_S, "2", actions=["A", "F"])
    p2_after_S = node_S

    # Player 2 also moves after B, in the same information set
    g.append_infoset(node_B, p2_after_S.infoset)
    p2_after_B = node_B

    # Distinct outcomes
    out_S_A = g.add_outcome([1, 4], label="choose_S_then_A")
    out_S_F = g.add_outcome([-2, 5], label="choose_S_then_F")
    out_B_A = g.add_outcome([2, 4], label="choose_B_then_A")
    out_B_F = g.add_outcome([-1, 0], label="choose_B_then_F")

    # Assign outcomes
    g.set_outcome(p2_after_S.children["A"], out_S_A)
    g.set_outcome(p2_after_S.children["F"], out_S_F)
    g.set_outcome(p2_after_B.children["A"], out_B_A)
    g.set_outcome(p2_after_B.children["F"], out_B_F)

    return g


if __name__ == "__main__":
    game = build_entry_game_imperfect_monitoring_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

    