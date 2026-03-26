from pathlib import Path
import pygambit as gbt


def build_3_1_a() -> gbt.Game:
    """Construct Watson Figure 3.1(a): aggressive / passive / out."""
    # Create a two-player extensive-form tree.
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 3.1(a)"
    )

    # Player 1 chooses Aggressive, Passive, or Out.
    g.append_move(g.root, player="1", actions=["A", "P", "O"])

    node_A = g.root.children["A"]
    node_P = g.root.children["P"]
    node_O = g.root.children["O"]

    # If Player 1 stays in the market, Player 2 chooses A or P
    # without observing whether Player 1 chose A or P.
    g.append_move(
        [node_A, node_P],
        player="2",
        actions=["A", "P"]
    )

    # Terminal nodes after Player 1 chose A.
    AA = node_A.children["A"]
    AP = node_A.children["P"]

    # Terminal nodes after Player 1 chose P.
    PA = node_P.children["A"]
    PP = node_P.children["P"]

    # Terminal outcomes in the order (Player 1, Player 2).
    out_outcome = g.add_outcome([0, 4], label="O")
    aa_outcome = g.add_outcome([3, 3], label="AA")
    ap_outcome = g.add_outcome([4, 2], label="AP")
    pa_outcome = g.add_outcome([2, 4], label="PA")
    pp_outcome = g.add_outcome([2, 2], label="PP")

    # Attach outcomes to terminal nodes.
    g.set_outcome(node_O, out_outcome)
    g.set_outcome(AA, aa_outcome)
    g.set_outcome(AP, ap_outcome)
    g.set_outcome(PA, pa_outcome)
    g.set_outcome(PP, pp_outcome)

    return g


if __name__ == "__main__":
    g = build_3_1_a()

    # Save the .efg next to this script.
    out_path = Path(__file__).with_name("figure_3_1_a.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    