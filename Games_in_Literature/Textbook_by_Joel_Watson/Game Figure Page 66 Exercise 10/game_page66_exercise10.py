from pathlib import Path
import pygambit as gbt


def build_exercise_10() -> gbt.Game:
    """Construct Exercise 10: simplified ultimatum-offer bargaining game."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Exercise 10"
    )

    # Player 1 chooses among Offer H, M, and L.
    g.append_move(g.root, player="1", actions=["Offer H", "M", "L"])

    node_H = g.root.children["Offer H"]
    node_M = g.root.children["M"]
    node_L = g.root.children["L"]

    # After each offer, Player 2 decides whether to accept or reject that specific offer.
    g.append_move(node_H, player="2", actions=["A^H", "R^H"])
    g.append_move(node_M, player="2", actions=["A^M", "R^M"])
    g.append_move(node_L, player="2", actions=["A^L", "R^L"])

    node_AH = node_H.children["A^H"]
    node_RH = node_H.children["R^H"]
    node_AM = node_M.children["A^M"]
    node_RM = node_M.children["R^M"]
    node_AL = node_L.children["A^L"]
    node_RL = node_L.children["R^L"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_AH = g.add_outcome([0, 2], label="Accept H")
    outcome_RH = g.add_outcome([0, 0], label="Reject H")
    outcome_AM = g.add_outcome([1, 1], label="Accept M")
    outcome_RM = g.add_outcome([0, 0], label="Reject M")
    outcome_AL = g.add_outcome([2, 0], label="Accept L")
    outcome_RL = g.add_outcome([0, 0], label="Reject L")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_AH, outcome_AH)
    g.set_outcome(node_RH, outcome_RH)
    g.set_outcome(node_AM, outcome_AM)
    g.set_outcome(node_RM, outcome_RM)
    g.set_outcome(node_AL, outcome_AL)
    g.set_outcome(node_RL, outcome_RL)

    return g


if __name__ == "__main__":
    g = build_exercise_10()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_10.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    