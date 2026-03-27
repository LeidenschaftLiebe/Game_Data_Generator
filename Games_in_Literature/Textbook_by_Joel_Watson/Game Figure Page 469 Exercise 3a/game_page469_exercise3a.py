from pathlib import Path
import pygambit as gbt


def build_page_469_exercise_3a() -> gbt.Game:
    """Construct Page 469 Exercise 3(a)."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Page 469 Exercise 3(a)"
    )

    # Chance selects A or B with equal probability.
    g.append_move(g.root, g.players.chance, actions=["A", "B"])
    g.set_chance_probs(
        g.root.infoset,
        [gbt.Rational("1/2"), gbt.Rational("1/2")]
    )

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]

    # Player 1 observes nature's choice and moves.
    g.append_move(node_A, player="1", actions=["U", "D"])
    g.append_move(node_B, player="1", actions=["u", "d"])

    node_AU = node_A.children["U"]
    node_AD = node_A.children["D"]
    node_Bu = node_B.children["u"]
    node_Bd = node_B.children["d"]

    # Player 2 moves at one information set across all four nodes.
    g.append_move(node_AU, player="2", actions=["L", "R"])
    g.append_infoset(node_AD, node_AU.infoset)
    g.append_infoset(node_Bu, node_AU.infoset)
    g.append_infoset(node_Bd, node_AU.infoset)

    node_AUL = node_AU.children["L"]
    node_AUR = node_AU.children["R"]
    node_ADL = node_AD.children["L"]
    node_ADR = node_AD.children["R"]
    node_BuL = node_Bu.children["L"]
    node_BuR = node_Bu.children["R"]
    node_BdL = node_Bd.children["L"]
    node_BdR = node_Bd.children["R"]

    # Distinct outcomes for each terminal node.
    out_AUL = g.add_outcome([2, 2], label="A_U_L")
    out_AUR = g.add_outcome([0, 0], label="A_U_R")
    out_ADL = g.add_outcome([0, 0], label="A_D_L")
    out_ADR = g.add_outcome([4, 4], label="A_D_R")

    out_BuL = g.add_outcome([0, 2], label="B_u_L")
    out_BuR = g.add_outcome([2, 0], label="B_u_R")
    out_BdL = g.add_outcome([4, 0], label="B_d_L")
    out_BdR = g.add_outcome([0, 4], label="B_d_R")

    # Attach outcomes.
    g.set_outcome(node_AUL, out_AUL)
    g.set_outcome(node_AUR, out_AUR)
    g.set_outcome(node_ADL, out_ADL)
    g.set_outcome(node_ADR, out_ADR)

    g.set_outcome(node_BuL, out_BuL)
    g.set_outcome(node_BuR, out_BuR)
    g.set_outcome(node_BdL, out_BdL)
    g.set_outcome(node_BdR, out_BdR)

    return g


if __name__ == "__main__":
    g = build_page_469_exercise_3a()

    out_path = Path(__file__).with_name("game_page469_exercise3a.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")



