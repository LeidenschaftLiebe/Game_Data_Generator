from pathlib import Path
import pygambit as gbt


def build_geb_reversed_investment_game_fig4() -> gbt.Game:
    """Construct Fig. 4 Reversed-Investment game from the article."""
    g = gbt.Game.new_tree(
        players=["A", "B", "C"],
        title="GEB Reversed-Investment Game Fig. 4"
    )

    # Player A moves first and chooses whether to stay out or use 25 ECU from C's endowment.
    g.append_move(g.root, player="A", actions=["Out", "In"])

    node_out = g.root.children["Out"]
    node_in = g.root.children["In"]

    # If A chooses Out, the game ends immediately at the initial endowments.
    out_out = g.add_outcome([170, 100, 30], label="Out")
    g.set_outcome(node_out, out_out)

    # If A chooses In, B decides how much of the 25 ECU to transfer back to C.
    g.append_move(node_in, player="B", actions=["Left", "Right"])

    node_left = node_in.children["Left"]
    node_right = node_in.children["Right"]

    # Left: B keeps 20 ECU and transfers 5 ECU to C, doubled to 10.
    out_left = g.add_outcome([170, 120, 15], label="In_Left")

    # Right: B transfers the full 25 ECU to C, doubled to 50.
    out_right = g.add_outcome([170, 100, 55], label="In_Right")

    g.set_outcome(node_left, out_left)
    g.set_outcome(node_right, out_right)

    return g


if __name__ == "__main__":
    g = build_geb_reversed_investment_game_fig4()

    out_path = Path(__file__).with_name("game_fig4_v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")




