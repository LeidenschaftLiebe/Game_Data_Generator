from pathlib import Path
import pygambit as gbt


def build_geb_fig1_no_disclosure() -> gbt.Game:
    """Construct Fig. 1 (No disclosure) from the article."""
    g = gbt.Game.new_tree(
        players=["Agent", "Principal"],
        title="GEB Fig. 1 No Disclosure"
    )

    # Nature first determines whether the task is easy or difficult.
    g.append_move(g.root, player=g.players.chance, actions=["EasyTask", "DifficultTask"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational("1/2"), gbt.Rational("1/2")])

    node_easy = g.root.children["EasyTask"]
    node_diff = g.root.children["DifficultTask"]

    # The agent chooses IN or OUT without knowing the task difficulty.
    g.append_move(node_easy, player="Agent", actions=["IN", "OUT"])
    g.append_infoset(node_diff, node_easy.infoset)

    node_easy_in = node_easy.children["IN"]
    node_easy_out = node_easy.children["OUT"]

    node_diff_in = node_diff.children["IN"]
    node_diff_out = node_diff.children["OUT"]

    # OUT leads to the outside-option result in either state.
    out_easy_out = g.add_outcome([30, 25], label="Easy_OUT")
    out_diff_out = g.add_outcome([30, 25], label="Difficult_OUT")

    g.set_outcome(node_easy_out, out_easy_out)
    g.set_outcome(node_diff_out, out_diff_out)

    # After choosing IN, the agent chooses HIGH or LOW, still without disclosure.
    g.append_move(node_easy_in, player="Agent", actions=["HIGH", "LOW"])
    g.append_infoset(node_diff_in, node_easy_in.infoset)

    node_easy_high = node_easy_in.children["HIGH"]
    node_easy_low = node_easy_in.children["LOW"]

    node_diff_high = node_diff_in.children["HIGH"]
    node_diff_low = node_diff_in.children["LOW"]

    # Terminal results after IN.
    out_easy_high = g.add_outcome([20, 50], label="Easy_IN_HIGH")
    out_easy_low = g.add_outcome([50, 35], label="Easy_IN_LOW")
    out_diff_high = g.add_outcome([20, 50], label="Difficult_IN_HIGH")
    out_diff_low = g.add_outcome([0, 35], label="Difficult_IN_LOW")

    g.set_outcome(node_easy_high, out_easy_high)
    g.set_outcome(node_easy_low, out_easy_low)
    g.set_outcome(node_diff_high, out_diff_high)
    g.set_outcome(node_diff_low, out_diff_low)

    return g


if __name__ == "__main__":
    g = build_geb_fig1_no_disclosure()

    out_path = Path(__file__).with_name("game_fig1_v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")