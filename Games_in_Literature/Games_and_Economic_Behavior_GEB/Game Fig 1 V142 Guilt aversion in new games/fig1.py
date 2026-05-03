from pathlib import Path
import pygambit as gbt


def build_geb_investment_game_fig1() -> gbt.Game:
    """Construct Fig. 1 Investment game from the article."""
    g = gbt.Game.new_tree(
        players=["A", "B", "C"],
        title="GEB Investment Game Fig. 1"
    )

    # Player A moves first and chooses whether to stay out or send 25 ECU to B.
    g.append_move(g.root, player="A", actions=["Out", "In"])

    node_out = g.root.children["Out"]
    node_in = g.root.children["In"]

    # If A chooses Out, the game ends immediately at the initial endowments.
    out_out = g.add_outcome([170, 100, 30], label="Out")
    g.set_outcome(node_out, out_out)

    # If A chooses In, B decides how much to return to A.
    g.append_move(node_in, player="B", actions=["Left", "Right"])

    node_left = node_in.children["Left"]
    node_right = node_in.children["Right"]

    # Left: B keeps 20 ECU and returns 5 ECU to A, doubled to 10.
    out_left = g.add_outcome([155, 120, 30], label="In_Left")

    # Right: B returns the full 25 ECU to A, doubled to 50.
    out_right = g.add_outcome([195, 100, 30], label="In_Right")

    g.set_outcome(node_left, out_left)
    g.set_outcome(node_right, out_right)

    return g


if __name__ == "__main__":
    g = build_geb_investment_game_fig1()

    out_path = Path(__file__).with_name("game_fig1_v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")




