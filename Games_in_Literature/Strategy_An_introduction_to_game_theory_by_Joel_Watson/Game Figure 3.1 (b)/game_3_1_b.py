from pathlib import Path
import pygambit as gbt


def build_3_1_b() -> gbt.Game:
    """Construct Watson Figure 3.1(b)."""
    # Create a two-player extensive-form tree.
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 3.1(b)"
    )

    # Player 1 first chooses Out or In.
    g.append_move(g.root, player="1", actions=["O", "I"])

    out_node = g.root.children["O"]
    in_node = g.root.children["I"]

    # If Player 1 chooses In, Player 2 chooses Out or In.
    g.append_move(in_node, player="2", actions=["O", "I"])

    p2_out_node = in_node.children["O"]
    p2_in_node = in_node.children["I"]

    # If Player 2 also chooses In, Player 1 chooses A or B.
    g.append_move(p2_in_node, player="1", actions=["A", "B"])

    A_node = p2_in_node.children["A"]
    B_node = p2_in_node.children["B"]

    # Terminal outcomes in the order (Player 1, Player 2).
    out_outcome = g.add_outcome([2, 2], label="O")
    p2_out_outcome = g.add_outcome([1, 3], label="IO")
    A_outcome = g.add_outcome([4, 2], label="IIA")
    B_outcome = g.add_outcome([3, 4], label="IIB")

    # Attach outcomes to the terminal nodes.
    g.set_outcome(out_node, out_outcome)
    g.set_outcome(p2_out_node, p2_out_outcome)
    g.set_outcome(A_node, A_outcome)
    g.set_outcome(B_node, B_outcome)

    return g


if __name__ == "__main__":
    g = build_3_1_b()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("figure_3_1_b.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    