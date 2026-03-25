from pathlib import Path
import pygambit as gbt


def build_katzenberg_movie_game() -> gbt.Game:
    """Construct Watson's bug-movie game (Figure 2.5) as an extensive-form game."""
    # Create a tree game with the two players named as in the figure.
    g = gbt.Game.new_tree(
        players=["K", "E"],
        title="Katzenberg Bug Movies Game"
    )

    # Root move: Katzenberg chooses whether to leave Disney or stay.
    g.append_move(g.root, player="K", actions=["Leave", "Stay"])

    # Access the two branches by action label.
    leave_node = g.root.children["Leave"]
    stay_node = g.root.children["Stay"]

    # If Katzenberg leaves, Eisner decides whether Disney produces A Bug's Life.
    g.append_move(
        leave_node,
        player="E",
        actions=["Produce A Bug's Life", "Not"]
    )

    produce_bug_node = leave_node.children["Produce A Bug's Life"]
    no_bug_node = leave_node.children["Not"]

    # Katzenberg then decides whether to produce Antz without observing Eisner's choice.
    # Passing a list of nodes puts these two decision nodes in the same infoset.
    g.append_move(
        [produce_bug_node, no_bug_node],
        player="K",
        actions=["Produce Antz", "Not"]
    )

    # Branches after Eisner produces A Bug's Life.
    both_produce_node = produce_bug_node.children["Produce Antz"]
    only_bug_node = produce_bug_node.children["Not"]

    # Branches after Eisner does not produce A Bug's Life.
    only_antz_node = no_bug_node.children["Produce Antz"]
    neither_node = no_bug_node.children["Not"]

    # If both studios produce a movie, Katzenberg chooses whether to release early.
    g.append_move(
        both_produce_node,
        player="K",
        actions=["Release early", "Not"]
    )

    early_node = both_produce_node.children["Release early"]
    not_early_node = both_produce_node.children["Not"]

    # Create terminal outcomes in the order (K, E), matching the textbook figure.
    stay_outcome = g.add_outcome([35, 100], label="Stay")
    only_bug_outcome = g.add_outcome([0, 140], label="Only A Bug's Life")
    only_antz_outcome = g.add_outcome([80, 0], label="Only Antz")
    neither_outcome = g.add_outcome([0, 0], label="Neither")
    early_outcome = g.add_outcome([40, 110], label="Both, release early")
    not_early_outcome = g.add_outcome([13, 120], label="Both, no early release")

    # Attach outcomes to the terminal nodes.
    g.set_outcome(stay_node, stay_outcome)
    g.set_outcome(only_bug_node, only_bug_outcome)
    g.set_outcome(only_antz_node, only_antz_outcome)
    g.set_outcome(neither_node, neither_outcome)
    g.set_outcome(early_node, early_outcome)
    g.set_outcome(not_early_node, not_early_outcome)

    return g


if __name__ == "__main__":
    g = build_katzenberg_movie_game()

    # Save the .efg next to this script, regardless of where Python is launched from.
    out_path = Path(__file__).with_name("katzenberg_movie_game.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
