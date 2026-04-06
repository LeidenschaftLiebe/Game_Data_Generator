from pathlib import Path
import pygambit as gbt


def build_geb_inequality_game_risky_exit() -> gbt.Game:
    """Construct Fig. 2(a): Risky treatment with exit and a Strong-player infoset."""
    g = gbt.Game.new_tree(
        players=["Weak", "Strong"],
        title="GEB Inequality Game Risky Exit Fig. 2a"
    )

    # Weak chooses first in the tree representation of the simultaneous game.
    g.append_move(g.root, player="Weak", actions=["Exploit", "Exit", "Collaborate"])

    node_exploit = g.root.children["Exploit"]
    node_exit = g.root.children["Exit"]
    node_collab = g.root.children["Collaborate"]

    # Strong's three decision nodes are in one infoset, because Strong chooses
    # without observing whether Weak selected Exploit, Exit, or Collaborate.
    g.append_move(node_exploit, player="Strong", actions=["Exit", "Defensive", "Generous"])
    g.append_infoset(node_exit, node_exploit.infoset)
    g.append_infoset(node_collab, node_exploit.infoset)

    # Distinct terminal outcomes for every leaf.
    out_exploit_exit = g.add_outcome([0, 0], label="Exploit_StrongExit")
    out_exploit_def = g.add_outcome([0, 10], label="Exploit_Defensive")
    out_exploit_gen = g.add_outcome([9, 1], label="Exploit_Generous")

    out_exit_exit = g.add_outcome([0, 0], label="WeakExit_StrongExit")
    out_exit_def = g.add_outcome([0, 0], label="WeakExit_Defensive")
    out_exit_gen = g.add_outcome([0, 0], label="WeakExit_Generous")

    out_collab_exit = g.add_outcome([0, 0], label="Collaborate_StrongExit")
    out_collab_def = g.add_outcome([1, 9], label="Collaborate_Defensive")
    out_collab_gen = g.add_outcome([5, 5], label="Collaborate_Generous")

    # Outcomes after Weak chooses Exploit.
    g.set_outcome(node_exploit.children["Exit"], out_exploit_exit)
    g.set_outcome(node_exploit.children["Defensive"], out_exploit_def)
    g.set_outcome(node_exploit.children["Generous"], out_exploit_gen)

    # Outcomes after Weak chooses Exit.
    g.set_outcome(node_exit.children["Exit"], out_exit_exit)
    g.set_outcome(node_exit.children["Defensive"], out_exit_def)
    g.set_outcome(node_exit.children["Generous"], out_exit_gen)

    # Outcomes after Weak chooses Collaborate.
    g.set_outcome(node_collab.children["Exit"], out_collab_exit)
    g.set_outcome(node_collab.children["Defensive"], out_collab_def)
    g.set_outcome(node_collab.children["Generous"], out_collab_gen)

    return g


if __name__ == "__main__":
    g = build_geb_inequality_game_risky_exit()

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")



