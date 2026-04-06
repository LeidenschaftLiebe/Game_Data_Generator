from pathlib import Path
import pygambit as gbt


def build_geb_quasi_perfect_example_fig1() -> gbt.Game:
    g = gbt.Game.new_tree(
        players=["Player 1", "Player 2"],
        title="GEB Quasi-Perfect Example Fig. 1"
    )

    # Player 1 first choice
    g.append_move(g.root, player="Player 1", actions=["A", "B", "E"])
    node_A = g.root.children["A"]
    node_B = g.root.children["B"]
    node_E = g.root.children["E"]

    # Immediate terminal after E
    out_E = g.add_outcome([3, 0], label="E")
    g.set_outcome(node_E, out_E)

    # After A, Player 1 chooses C or D
    g.append_move(node_A, player="Player 1", actions=["C", "D"])
    node_AC = node_A.children["C"]
    node_AD = node_A.children["D"]

    # Create Player 2 move at AC
    g.append_move(node_AC, player="Player 2", actions=["a", "b"])

    # Attach AD and B to the same Player 2 infoset
    g.append_infoset(node_AD, node_AC.infoset)
    g.append_infoset(node_B, node_AC.infoset)

    # Outcomes
    out_AC_a = g.add_outcome([4, 0], label="A_C_a")
    out_AC_b = g.add_outcome([2, 0], label="A_C_b")
    out_AD_a = g.add_outcome([1, 1], label="A_D_a")
    out_AD_b = g.add_outcome([0, 0], label="A_D_b")
    out_B_a = g.add_outcome([0, 0], label="B_a")
    out_B_b = g.add_outcome([1, 1], label="B_b")

    g.set_outcome(node_AC.children["a"], out_AC_a)
    g.set_outcome(node_AC.children["b"], out_AC_b)
    g.set_outcome(node_AD.children["a"], out_AD_a)
    g.set_outcome(node_AD.children["b"], out_AD_b)
    g.set_outcome(node_B.children["a"], out_B_a)
    g.set_outcome(node_B.children["b"], out_B_b)

    return g


if __name__ == "__main__":
    g = build_geb_quasi_perfect_example_fig1()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to {out_path}")
    