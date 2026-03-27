from pathlib import Path
import pygambit as gbt


def build_page_441_exercise_5() -> gbt.Game:
    """Construct Page 441 Exercise 5."""
    g = gbt.Game.new_tree(
        players=["Amy", "Bart", "Chris"],
        title="Page 441 Exercise 5"
    )

    # Amy moves first.
    g.append_move(g.root, player="Amy", actions=["H", "F"])

    node_AH = g.root.children["H"]
    node_AF = g.root.children["F"]

    # Bart observes Amy and then chooses.
    g.append_move(node_AH, player="Bart", actions=["H", "F"])
    g.append_move(node_AF, player="Bart", actions=["H_prime", "F_prime"])

    node_AH_BH = node_AH.children["H"]
    node_AH_BF = node_AH.children["F"]
    node_AF_BH = node_AF.children["H_prime"]
    node_AF_BF = node_AF.children["F_prime"]

    # If Bart puts his hat on his head, game ends.
    out_top_stop = g.add_outcome([0, 0, 0], label="AmyH_BartH")
    out_bottom_stop = g.add_outcome([0, 0, 0], label="AmyF_BartH")

    g.set_outcome(node_AH_BH, out_top_stop)
    g.set_outcome(node_AF_BH, out_bottom_stop)

    # If Bart puts his hat on the floor, Chris guesses.
    g.append_move(node_AH_BF, player="Chris", actions=["Y", "N"])
    g.append_infoset(node_AF_BF, node_AH_BF.infoset)

    node_top_Y = node_AH_BF.children["Y"]
    node_top_N = node_AH_BF.children["N"]
    node_bottom_Y = node_AF_BF.children["Y"]
    node_bottom_N = node_AF_BF.children["N"]

    # Payoff order: Amy, Bart, Chris.
    out_top_Y = g.add_outcome([-1, 0, 1], label="AmyH_ChrisYes")
    out_top_N = g.add_outcome([1, 0, -1], label="AmyH_ChrisNo")

    out_bottom_Y = g.add_outcome([1, 0, -1], label="AmyF_ChrisYes")
    out_bottom_N = g.add_outcome([-1, 0, 1], label="AmyF_ChrisNo")

    g.set_outcome(node_top_Y, out_top_Y)
    g.set_outcome(node_top_N, out_top_N)
    g.set_outcome(node_bottom_Y, out_bottom_Y)
    g.set_outcome(node_bottom_N, out_bottom_N)

    return g


if __name__ == "__main__":
    g = build_page_441_exercise_5()

    out_path = Path(__file__).with_name("game_page441_exercise5.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")