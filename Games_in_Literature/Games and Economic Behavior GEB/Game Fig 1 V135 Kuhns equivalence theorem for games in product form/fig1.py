from pathlib import Path
import pygambit as gbt


def build_geb_alice_bob_nature_example() -> gbt.Game:
    """Construct the Alice-Bob-Nature tree as a concrete dataset instance."""
    g = gbt.Game.new_tree(
        players=["Bob", "Alice"],
        title="GEB Alice Bob Nature Example"
    )

    # Nature moves first.
    g.append_move(g.root, g.players.chance, actions=["omega+", "omega-"])
    g.set_chance_probs(
        g.root.infoset,
        [gbt.Rational("1/2"), gbt.Rational("1/2")]
    )

    node_plus = g.root.children["omega+"]
    node_minus = g.root.children["omega-"]

    # Bob observes Nature's move and chooses L or R.
    g.append_move(node_plus, player="Bob", actions=["L", "R"])
    g.append_move(node_minus, player="Bob", actions=["L", "R"])

    node_plus_L = node_plus.children["L"]
    node_plus_R = node_plus.children["R"]
    node_minus_L = node_minus.children["L"]
    node_minus_R = node_minus.children["R"]

    # Alice observes both Nature and Bob, then chooses T or B.
    g.append_move(node_plus_L, player="Alice", actions=["T", "B"])
    g.append_move(node_plus_R, player="Alice", actions=["T", "B"])
    g.append_move(node_minus_L, player="Alice", actions=["T", "B"])
    g.append_move(node_minus_R, player="Alice", actions=["T", "B"])

    # Explicit terminal outcomes chosen for this dataset instance.
    out_z1 = g.add_outcome([3, 2], label="z1")
    out_z2 = g.add_outcome([1, 4], label="z2")
    out_z3 = g.add_outcome([4, 1], label="z3")
    out_z4 = g.add_outcome([2, 3], label="z4")
    out_z5 = g.add_outcome([2, 3], label="z5")
    out_z6 = g.add_outcome([4, 1], label="z6")
    out_z7 = g.add_outcome([1, 4], label="z7")
    out_z8 = g.add_outcome([3, 2], label="z8")

    g.set_outcome(node_plus_L.children["T"], out_z1)
    g.set_outcome(node_plus_L.children["B"], out_z2)
    g.set_outcome(node_plus_R.children["T"], out_z3)
    g.set_outcome(node_plus_R.children["B"], out_z4)

    g.set_outcome(node_minus_L.children["T"], out_z5)
    g.set_outcome(node_minus_L.children["B"], out_z6)
    g.set_outcome(node_minus_R.children["T"], out_z7)
    g.set_outcome(node_minus_R.children["B"], out_z8)

    return g


if __name__ == "__main__":
    g = build_geb_alice_bob_nature_example()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")