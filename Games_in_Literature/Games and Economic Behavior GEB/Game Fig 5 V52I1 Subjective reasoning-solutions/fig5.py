from pathlib import Path
import pygambit as gbt


def build_fig5_procedural_reasoning_v0():
    g = gbt.Game.new_tree(
        players=["Alice", "Bob", "Emma", "David"],
        title="GEB Fig. 5 Procedural Reasoning Is Not Lexicographic V0"
    )

    # Alice moves first
    g.append_move(g.root, "Alice", actions=["a1", "a2"])
    alice_a1 = g.root.children["a1"]
    alice_a2 = g.root.children["a2"]

    # Bob moves after a1
    g.append_move(alice_a1, "Bob", actions=["b1", "b2"])
    bob_left = alice_a1

    # Bob also moves after a2, in the same information set
    g.append_infoset(alice_a2, bob_left.infoset)
    bob_right = alice_a2

    # Immediate terminal after a1 then b1
    out_a1_b1 = g.add_outcome([1, 1, 0, 0], label="a1_b1")
    g.set_outcome(bob_left.children["b1"], out_a1_b1)

    # David after a1 then b2
    david_left = bob_left.children["b2"]

    # Emma after a2 then b2
    emma_left = bob_right.children["b2"]
    g.append_move(emma_left, "Emma", actions=["c1", "c2"])

    # Emma also after a2 then b1, in the same information set
    emma_right = bob_right.children["b1"]
    g.append_infoset(emma_right, emma_left.infoset)

    # Outcomes after Emma left
    out_a2_b2_c1 = g.add_outcome([0, 0, 0, 0], label="a2_b2_c1")
    out_a2_b2_c2 = g.add_outcome([0, 0, 1, 0], label="a2_b2_c2")
    g.set_outcome(emma_left.children["c1"], out_a2_b2_c1)
    g.set_outcome(emma_left.children["c2"], out_a2_b2_c2)

    # Outcome after Emma right chooses c1
    out_a2_b1_c1 = g.add_outcome([0, 1, 1, 0], label="a2_b1_c1")
    g.set_outcome(emma_right.children["c1"], out_a2_b1_c1)

    # David also after a2 then b1 then c2, in the same information set as after a1 then b2
    g.append_move(david_left, "David", actions=["d1", "d2"])
    david_right = emma_right.children["c2"]
    g.append_infoset(david_right, david_left.infoset)

    # Outcomes after David
    out_left_d1 = g.add_outcome([1, 0, 0, 0], label="left_d1")
    out_left_d2 = g.add_outcome([1, 0, 0, 0], label="left_d2")
    out_right_d1 = g.add_outcome([0, 1, 0, 0], label="right_d1")
    out_right_d2 = g.add_outcome([0, 1, 0, 0], label="right_d2")

    g.set_outcome(david_left.children["d1"], out_left_d1)
    g.set_outcome(david_left.children["d2"], out_left_d2)
    g.set_outcome(david_right.children["d1"], out_right_d1)
    g.set_outcome(david_right.children["d2"], out_right_d2)

    return g


if __name__ == "__main__":
    game = build_fig5_procedural_reasoning_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")

    