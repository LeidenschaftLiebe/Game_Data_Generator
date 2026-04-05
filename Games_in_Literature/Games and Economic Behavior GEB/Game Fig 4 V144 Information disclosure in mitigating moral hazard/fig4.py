from pathlib import Path
import pygambit as gbt


def build_geb_fig4_non_commitment() -> gbt.Game:
    """Construct Fig. 4 (principal discloses after learning the state)."""
    g = gbt.Game.new_tree(
        players=["Agent", "Principal"],
        title="GEB Fig. 4 Non-Commitment"
    )

    # Nature first determines whether the task is easy or difficult.
    g.append_move(g.root, player=g.players.chance, actions=["EasyTask", "DifficultTask"])
    g.set_chance_probs(g.root.infoset, [gbt.Rational("1/2"), gbt.Rational("1/2")])

    node_easy = g.root.children["EasyTask"]
    node_diff = g.root.children["DifficultTask"]

    # After learning the realized state, the principal chooses whether to disclose immediately.
    g.append_move(node_easy, player="Principal", actions=["NoDisclosure", "ImmediateDisclosure"])
    g.append_move(node_diff, player="Principal", actions=["NoDisclosure", "ImmediateDisclosure"])

    node_easy_no = node_easy.children["NoDisclosure"]
    node_easy_im = node_easy.children["ImmediateDisclosure"]
    node_diff_no = node_diff.children["NoDisclosure"]
    node_diff_im = node_diff.children["ImmediateDisclosure"]

    # Under no disclosure, the agent chooses IN or OUT without learning the state.
    g.append_move(node_easy_no, player="Agent", actions=["IN", "OUT"])
    g.append_infoset(node_diff_no, node_easy_no.infoset)

    node_easy_no_in = node_easy_no.children["IN"]
    node_easy_no_out = node_easy_no.children["OUT"]
    node_diff_no_in = node_diff_no.children["IN"]
    node_diff_no_out = node_diff_no.children["OUT"]

    out_easy_no_out = g.add_outcome([30, 25], label="Easy_NoDisclosure_OUT")
    out_diff_no_out = g.add_outcome([30, 25], label="Difficult_NoDisclosure_OUT")

    g.set_outcome(node_easy_no_out, out_easy_no_out)
    g.set_outcome(node_diff_no_out, out_diff_no_out)

    # If the agent enters under no disclosure, effort is chosen without learning the state.
    g.append_move(node_easy_no_in, player="Agent", actions=["HIGH", "LOW"])
    g.append_infoset(node_diff_no_in, node_easy_no_in.infoset)

    node_easy_no_high = node_easy_no_in.children["HIGH"]
    node_easy_no_low = node_easy_no_in.children["LOW"]
    node_diff_no_high = node_diff_no_in.children["HIGH"]
    node_diff_no_low = node_diff_no_in.children["LOW"]

    out_easy_no_high = g.add_outcome([20, 50], label="Easy_NoDisclosure_IN_HIGH")
    out_easy_no_low = g.add_outcome([50, 35], label="Easy_NoDisclosure_IN_LOW")
    out_diff_no_high = g.add_outcome([20, 50], label="Difficult_NoDisclosure_IN_HIGH")
    out_diff_no_low = g.add_outcome([0, 35], label="Difficult_NoDisclosure_IN_LOW")

    g.set_outcome(node_easy_no_high, out_easy_no_high)
    g.set_outcome(node_easy_no_low, out_easy_no_low)
    g.set_outcome(node_diff_no_high, out_diff_no_high)
    g.set_outcome(node_diff_no_low, out_diff_no_low)

    # Under immediate disclosure, the agent observes the state before choosing IN or OUT.
    g.append_move(node_easy_im, player="Agent", actions=["IN", "OUT"])
    g.append_move(node_diff_im, player="Agent", actions=["IN", "OUT"])

    node_easy_im_in = node_easy_im.children["IN"]
    node_easy_im_out = node_easy_im.children["OUT"]
    node_diff_im_in = node_diff_im.children["IN"]
    node_diff_im_out = node_diff_im.children["OUT"]

    out_easy_im_out = g.add_outcome([30, 25], label="Easy_ImmediateDisclosure_OUT")
    out_diff_im_out = g.add_outcome([30, 25], label="Difficult_ImmediateDisclosure_OUT")

    g.set_outcome(node_easy_im_out, out_easy_im_out)
    g.set_outcome(node_diff_im_out, out_diff_im_out)

    # If the agent enters under immediate disclosure, effort is chosen after learning the state.
    g.append_move(node_easy_im_in, player="Agent", actions=["HIGH", "LOW"])
    g.append_move(node_diff_im_in, player="Agent", actions=["HIGH", "LOW"])

    node_easy_im_high = node_easy_im_in.children["HIGH"]
    node_easy_im_low = node_easy_im_in.children["LOW"]
    node_diff_im_high = node_diff_im_in.children["HIGH"]
    node_diff_im_low = node_diff_im_in.children["LOW"]

    out_easy_im_high = g.add_outcome([20, 50], label="Easy_ImmediateDisclosure_IN_HIGH")
    out_easy_im_low = g.add_outcome([50, 35], label="Easy_ImmediateDisclosure_IN_LOW")
    out_diff_im_high = g.add_outcome([20, 50], label="Difficult_ImmediateDisclosure_IN_HIGH")
    out_diff_im_low = g.add_outcome([0, 35], label="Difficult_ImmediateDisclosure_IN_LOW")

    g.set_outcome(node_easy_im_high, out_easy_im_high)
    g.set_outcome(node_easy_im_low, out_easy_im_low)
    g.set_outcome(node_diff_im_high, out_diff_im_high)
    g.set_outcome(node_diff_im_low, out_diff_im_low)

    return g


if __name__ == "__main__":
    g = build_geb_fig4_non_commitment()

    out_path = Path(__file__).with_name("game_fig4_v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
