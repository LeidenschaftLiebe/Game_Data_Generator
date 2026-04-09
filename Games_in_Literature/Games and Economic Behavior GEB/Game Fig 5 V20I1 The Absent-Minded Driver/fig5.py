from pathlib import Path
import pygambit as gbt


def build_clear_headed_or_absent_minded_v0():
    g = gbt.Game.new_tree(
        players=["Driver"],
        title="Clear-Headed or Absent-Minded V0"
    )

    # Start choice
    g.append_move(g.root, "Driver", actions=["ClearHeaded", "AbsentMinded"])

    clear_branch = g.root.children["ClearHeaded"]
    absent_branch = g.root.children["AbsentMinded"]

    # Use chance nodes to represent the behavioral probabilities shown in the figure

    # Clear-headed branch: at X
    g.append_move(clear_branch, g.players.chance, actions=["EXIT", "CONT"])
    g.set_chance_probs(clear_branch.infoset, [gbt.Rational(3, 7), gbt.Rational(4, 7)])

    clear_x = clear_branch
    clear_x_cont = clear_x.children["CONT"]

    # Clear-headed branch: at Y
    g.append_move(clear_x_cont, g.players.chance, actions=["EXIT", "CONT"])
    g.set_chance_probs(clear_x_cont.infoset, [gbt.Rational(3, 7), gbt.Rational(4, 7)])

    # Absent-minded branch: at X
    g.append_move(absent_branch, g.players.chance, actions=["EXIT", "CONT"])
    g.set_chance_probs(absent_branch.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    absent_x = absent_branch
    absent_x_cont = absent_x.children["CONT"]

    # Absent-minded branch: at Y
    g.append_move(absent_x_cont, g.players.chance, actions=["EXIT", "CONT"])
    g.set_chance_probs(absent_x_cont.infoset, [gbt.Rational(1, 2), gbt.Rational(1, 2)])

    # Distinct terminal outcomes
    out_clear_exit_x = g.add_outcome([0], label="clear_exit_at_X")
    out_clear_exit_y = g.add_outcome([0], label="clear_exit_at_Y")
    out_clear_continue_past_y = g.add_outcome([1], label="clear_continue_past_Y")

    out_absent_exit_x = g.add_outcome([0], label="absent_exit_at_X")
    out_absent_exit_y = g.add_outcome([0], label="absent_exit_at_Y")
    out_absent_continue_past_y = g.add_outcome([1], label="absent_continue_past_Y")

    # Assign outcomes on clear-headed branch
    g.set_outcome(clear_x.children["EXIT"], out_clear_exit_x)
    g.set_outcome(clear_x_cont.children["EXIT"], out_clear_exit_y)
    g.set_outcome(clear_x_cont.children["CONT"], out_clear_continue_past_y)

    # Assign outcomes on absent-minded branch
    g.set_outcome(absent_x.children["EXIT"], out_absent_exit_x)
    g.set_outcome(absent_x_cont.children["EXIT"], out_absent_exit_y)
    g.set_outcome(absent_x_cont.children["CONT"], out_absent_continue_past_y)

    return g


if __name__ == "__main__":
    game = build_clear_headed_or_absent_minded_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



    