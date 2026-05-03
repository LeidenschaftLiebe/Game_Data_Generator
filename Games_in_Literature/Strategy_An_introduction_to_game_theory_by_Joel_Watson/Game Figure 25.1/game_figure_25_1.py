from pathlib import Path
import pygambit as gbt


def build_figure_25_1() -> gbt.Game:
    """Construct Watson Figure 25.1: lottery or sure thing."""
    g = gbt.Game.new_tree(
        players=["You"],
        title="Watson Figure 25.1 - Lottery or Sure Thing"
    )

    # You choose between the sure amount and the lottery.
    g.append_move(g.root, player="You", actions=["A", "B"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]

    # If you choose B, chance determines the outcome.
    g.append_move(node_B, g.players.chance, actions=["Heads", "Tails"])
    g.set_chance_probs(node_B.infoset, [0.5, 0.5])

    node_B_heads = node_B.children["Heads"]
    node_B_tails = node_B.children["Tails"]

    # Distinct outcomes for each terminal node.
    outcome_A = g.add_outcome([950], label="Sure_950")
    outcome_B_heads = g.add_outcome([2000], label="Lottery_2000")
    outcome_B_tails = g.add_outcome([0], label="Lottery_0")

    # Attach outcomes.
    g.set_outcome(node_A, outcome_A)
    g.set_outcome(node_B_heads, outcome_B_heads)
    g.set_outcome(node_B_tails, outcome_B_tails)

    return g


if __name__ == "__main__":
    g = build_figure_25_1()

    out_path = Path(__file__).with_name("figure_25_1.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")