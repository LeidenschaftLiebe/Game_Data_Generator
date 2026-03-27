from pathlib import Path
import pygambit as gbt


def build_figure_24_4() -> gbt.Game:
    """Construct Watson Figure 24.4 with x=12 prob 2/3 and x=0 prob 1/3."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 24.4 - Extensive and Normal Form"
    )

    # Nature chooses x.
    g.append_move(g.root, g.players.chance, actions=["x=12", "x=0"])
    g.set_chance_probs(g.root.infoset, [0.66667, 0.33333])

    node_x12 = g.root.children["x=12"]
    node_x0 = g.root.children["x=0"]

    # Player 1 observes x and chooses A or B separately at each type.
    g.append_move(node_x12, player="1", actions=["A^12", "B^12"])
    g.append_move(node_x0, player="1", actions=["A^0", "B^0"])

    node_A12 = node_x12.children["A^12"]
    node_B12 = node_x12.children["B^12"]
    node_A0 = node_x0.children["A^0"]
    node_B0 = node_x0.children["B^0"]

    # Player 2 does not observe x or Player 1's action.
    # All four nodes are in one information set.
    g.append_move(node_A12, player="2", actions=["C", "D"])
    g.append_infoset(node_B12, node_A12.infoset)
    g.append_infoset(node_A0, node_A12.infoset)
    g.append_infoset(node_B0, node_A12.infoset)

    node_A12C = node_A12.children["C"]
    node_A12D = node_A12.children["D"]
    node_B12C = node_B12.children["C"]
    node_B12D = node_B12.children["D"]
    node_A0C = node_A0.children["C"]
    node_A0D = node_A0.children["D"]
    node_B0C = node_B0.children["C"]
    node_B0D = node_B0.children["D"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_A12C = g.add_outcome([12, 9], label="A12C")
    outcome_A12D = g.add_outcome([3, 6], label="A12D")
    outcome_B12C = g.add_outcome([6, 0], label="B12C")
    outcome_B12D = g.add_outcome([6, 9], label="B12D")

    outcome_A0C = g.add_outcome([0, 9], label="A0C")
    outcome_A0D = g.add_outcome([3, 6], label="A0D")
    outcome_B0C = g.add_outcome([6, 0], label="B0C")
    outcome_B0D = g.add_outcome([6, 9], label="B0D")

    # Attach rewards.
    g.set_outcome(node_A12C, outcome_A12C)
    g.set_outcome(node_A12D, outcome_A12D)
    g.set_outcome(node_B12C, outcome_B12C)
    g.set_outcome(node_B12D, outcome_B12D)

    g.set_outcome(node_A0C, outcome_A0C)
    g.set_outcome(node_A0D, outcome_A0D)
    g.set_outcome(node_B0C, outcome_B0C)
    g.set_outcome(node_B0D, outcome_B0D)

    return g


if __name__ == "__main__":
    g = build_figure_24_4()

    out_path = Path(__file__).with_name("figure_24_4.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")