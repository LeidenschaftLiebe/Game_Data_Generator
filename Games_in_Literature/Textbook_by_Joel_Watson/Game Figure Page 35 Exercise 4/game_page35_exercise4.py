from pathlib import Path
import pygambit as gbt


def build_exercise_4() -> gbt.Game:
    """Construct Exercise 4."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Exercise 4"
    )

    # Player 1 first chooses a or b.
    g.append_move(g.root, player="1", actions=["a", "b"])

    node_a = g.root.children["a"]
    node_b = g.root.children["b"]

    # Player 2 chooses c or d without knowing whether Player 1 chose a or b.
    g.append_move([node_a, node_b], player="2", actions=["c", "d"])

    node_ac = node_a.children["c"]
    node_ad = node_a.children["d"]
    node_bc = node_b.children["c"]
    node_bd = node_b.children["d"]

    # After a then c, Player 2 chooses f or g.
    g.append_move(node_ac, player="2", actions=["f", "g"])

    node_acf = node_ac.children["f"]
    node_acg = node_ac.children["g"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_acf = g.add_outcome([4, 1], label="acf")
    outcome_acg = g.add_outcome([1, 2], label="acg")
    outcome_ad = g.add_outcome([0, 3], label="ad")
    outcome_bc = g.add_outcome([8, 0], label="bc")
    outcome_bd = g.add_outcome([0, 2], label="bd")

    # Attach rewards to terminal nodes.
    g.set_outcome(node_acf, outcome_acf)
    g.set_outcome(node_acg, outcome_acg)
    g.set_outcome(node_ad, outcome_ad)
    g.set_outcome(node_bc, outcome_bc)
    g.set_outcome(node_bd, outcome_bd)

    return g


if __name__ == "__main__":
    g = build_exercise_4()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("exercise_4.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")