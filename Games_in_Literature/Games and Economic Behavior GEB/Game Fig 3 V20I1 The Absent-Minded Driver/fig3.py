from pathlib import Path
import pygambit as gbt


def build_absent_minded_driver_fig3_v0():
    g = gbt.Game.new_tree(
        players=["Driver"],
        title="More Challenging Absent-Minded Driver Example V0"
    )

    # First indistinguishable decision point: X
    g.append_move(g.root, "Driver", actions=["EXIT", "CONT"])
    x_node = g.root

    # If continue from X, reach Y in the same information set
    y_node = x_node.children["CONT"]
    g.append_infoset(y_node, x_node.infoset)

    # Continue from Y leads to Z, also in the same information set
    z_node = y_node.children["CONT"]
    g.append_infoset(z_node, x_node.infoset)

    # Distinct outcomes for each terminal node
    out_exit_x = g.add_outcome([7], label="exit_at_X")
    out_exit_y = g.add_outcome([0], label="exit_at_Y")
    out_exit_z = g.add_outcome([22], label="exit_at_Z")
    out_continue_past_z = g.add_outcome([2], label="continue_past_Z")

    # Assign outcomes
    g.set_outcome(x_node.children["EXIT"], out_exit_x)
    g.set_outcome(y_node.children["EXIT"], out_exit_y)
    g.set_outcome(z_node.children["EXIT"], out_exit_z)
    g.set_outcome(z_node.children["CONT"], out_continue_past_z)

    return g


if __name__ == "__main__":
    game = build_absent_minded_driver_fig3_v0()
    out_path = Path(__file__).with_name("v0.efg")
    game.to_efg(str(out_path))
    print(f"Saved to: {out_path}")


    