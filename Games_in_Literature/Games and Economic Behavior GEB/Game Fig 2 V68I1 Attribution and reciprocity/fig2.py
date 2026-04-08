from pathlib import Path
import pygambit as gbt


def build_gamma2_v0():
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2", "Player 3"],
        title="GEB Fig. 2 Gamma2 V0"
    )

    eps = 1

    # Player 1 at the root
    g.append_move(g.root, "Player 1", actions=["L", "M", "R"])
    left_node = g.root.children["L"]
    middle_node = g.root.children["M"]
    right_node = g.root.children["R"]

    # After L, Player 2 chooses
    g.append_move(left_node, "Player 2", actions=["l", "r"])

    # After R, Player 3 chooses
    g.append_move(right_node, "Player 3", actions=["l", "r"])

    # After M, chance chooses left or right branch with equal probability
    g.append_move(middle_node, g.players.chance, actions=["LeftBranch", "RightBranch"])
    g.set_chance_probs(middle_node.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    chance_left = middle_node.children["LeftBranch"]
    chance_right = middle_node.children["RightBranch"]

    # Then Player 2 or Player 3 moves
    g.append_move(chance_left, "Player 2", actions=["l", "r"])
    g.append_move(chance_right, "Player 3", actions=["l", "r"])

    # Distinct outcomes
    out_L_l = g.add_outcome([3, 0, 1], label="L_l")
    out_L_r = g.add_outcome([1, -eps, 1], label="L_r")

    out_R_l = g.add_outcome([3, 1, 0], label="R_l")
    out_R_r = g.add_outcome([1, 1, -eps], label="R_r")

    out_M_left_l = g.add_outcome([3, 0, 1], label="M_left_l")
    out_M_left_r = g.add_outcome([1, -eps, 1], label="M_left_r")

    out_M_right_l = g.add_outcome([3, 1, 0], label="M_right_l")
    out_M_right_r = g.add_outcome([1, 1, -eps], label="M_right_r")

    # Assign outcomes
    g.set_outcome(left_node.children["l"], out_L_l)
    g.set_outcome(left_node.children["r"], out_L_r)

    g.set_outcome(right_node.children["l"], out_R_l)
    g.set_outcome(right_node.children["r"], out_R_r)

    g.set_outcome(chance_left.children["l"], out_M_left_l)
    g.set_outcome(chance_left.children["r"], out_M_left_r)

    g.set_outcome(chance_right.children["l"], out_M_right_l)
    g.set_outcome(chance_right.children["r"], out_M_right_r)

    return g


if __name__ == "__main__":
    game = build_gamma2_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

