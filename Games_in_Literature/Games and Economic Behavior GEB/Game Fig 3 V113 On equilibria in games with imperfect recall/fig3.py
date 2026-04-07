from pathlib import Path
import pygambit as gbt


def build_absentminded_driver_policeman_extension():
    g = gbt.Game.new_tree(
        players=["Driver", "Policeman"],
        title="GEB Extension of the Absentminded Driver and the Policeman Fig. 3"
    )

    # Driver's initial choice: try to escape or surrender
    g.append_move(g.root, player="Driver", actions=["T", "S"])
    node_T = g.root.children["T"]
    node_S = g.root.children["S"]

    out_S = g.add_outcome([0, 0], label="S")
    g.set_outcome(node_S, out_S)

    # Policeman's early choice after the driver tries to escape
    g.append_move(node_T, player="Policeman", actions=["W", "I"])
    node_W = node_T.children["W"]
    node_I = node_T.children["I"]

    out_I = g.add_outcome([-1, -1], label="T_I")
    g.set_outcome(node_I, out_I)

    # Driver's absentminded highway choice:
    # first time on the highway
    g.append_move(node_W, player="Driver", actions=["C", "E"])
    first_continue = node_W.children["C"]
    first_exit = node_W.children["E"]

    # second time on the highway: same infoset as the first driver highway choice
    g.append_infoset(first_continue, node_W.infoset)
    second_continue = first_continue.children["C"]
    second_exit = first_continue.children["E"]

    # If the driver exits at the later exit, payoff is (0,0)
    out_second_exit = g.add_outcome([0, 0], label="T_W_C_E")
    g.set_outcome(second_exit, out_second_exit)

    # Policeman's later choice, at one shared infoset
    # Branch 1: driver exited at the first exit
    g.append_move(first_exit, player="Policeman", actions=["H", "E"])
    # Branch 2: driver continued twice
    g.append_infoset(second_continue, first_exit.infoset)

    # Outcomes if the driver exited at the first exit
    out_first_exit_H = g.add_outcome([1, -1], label="T_W_E_H")
    out_first_exit_E = g.add_outcome([0, 0], label="T_W_E_E")
    g.set_outcome(first_exit.children["H"], out_first_exit_H)
    g.set_outcome(first_exit.children["E"], out_first_exit_E)

    # Outcomes if the driver continued twice
    out_second_continue_H = g.add_outcome([0, 0], label="T_W_C_C_H")
    out_second_continue_E = g.add_outcome([1, -1], label="T_W_C_C_E")
    g.set_outcome(second_continue.children["H"], out_second_continue_H)
    g.set_outcome(second_continue.children["E"], out_second_continue_E)

    return g


if __name__ == "__main__":
    g = build_absentminded_driver_policeman_extension()
    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))
    print(f"Saved to: {out_path}")



