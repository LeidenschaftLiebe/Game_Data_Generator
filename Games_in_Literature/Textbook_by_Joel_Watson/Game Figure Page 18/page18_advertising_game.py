from pathlib import Path
import pygambit as gbt


def build_entry_advertising_game() -> gbt.Game:
    """Construct Watson's guided exercise: entry followed by advertising."""
    # Create a two-player extensive-form tree.
    g = gbt.Game.new_tree(
        players=["A", "B"],
        title="Entry and Advertising Game"
    )

    # Firm A first decides whether to enter (E) or stay out (D).
    g.append_move(g.root, player="A", actions=["E", "D"])

    enter_node = g.root.children["E"]
    stay_out_node = g.root.children["D"]

    # If A enters, B chooses whether to advertise (a) or not (n).
    g.append_move(enter_node, player="B", actions=["a", "n"])

    B_adv_after_entry = enter_node.children["a"]
    B_not_after_entry = enter_node.children["n"]

    # If A stays out, B alone chooses whether to advertise (a') or not (n').
    g.append_move(stay_out_node, player="B", actions=["a'", "n'"])

    B_adv_alone = stay_out_node.children["a'"]
    B_not_alone = stay_out_node.children["n'"]

    # If A entered, A then chooses whether to advertise (a) or not (n),
    # without observing whether B chose a or n.
    # Putting the two nodes in one append_move call creates one infoset.
    g.append_move(
        [B_adv_after_entry, B_not_after_entry],
        player="A",
        actions=["a", "n"]
    )

    # Outcomes when A entered and B advertised.
    both_adv = B_adv_after_entry.children["a"]
    only_B_adv = B_adv_after_entry.children["n"]

    # Outcomes when A entered and B did not advertise.
    only_A_adv = B_not_after_entry.children["a"]
    neither_adv = B_not_after_entry.children["n"]

    # Create terminal outcomes in the order (A, B).
    o_both_adv = g.add_outcome([3, 3], label="Both advertise")
    o_only_B_adv = g.add_outcome([1, 6], label="Only B advertises")
    o_only_A_adv = g.add_outcome([6, 1], label="Only A advertises")
    o_neither_adv = g.add_outcome([5, 5], label="Neither advertises")
    o_B_adv_alone = g.add_outcome([0, 4], label="B advertises alone")
    o_B_not_alone = g.add_outcome([0, 3.5], label="B does not advertise alone")

    # Attach outcomes.
    g.set_outcome(both_adv, o_both_adv)
    g.set_outcome(only_B_adv, o_only_B_adv)
    g.set_outcome(only_A_adv, o_only_A_adv)
    g.set_outcome(neither_adv, o_neither_adv)
    g.set_outcome(B_adv_alone, o_B_adv_alone)
    g.set_outcome(B_not_alone, o_B_not_alone)

    return g


if __name__ == "__main__":
    g = build_entry_advertising_game()

    # Save the .efg file next to this script.
    out_path = Path(__file__).with_name("entry_advertising_game.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    