from pathlib import Path
import pygambit as gbt


def build_page_440_exercise_1() -> gbt.Game:
    """Construct Page 440 Exercise 1."""
    g = gbt.Game.new_tree(
        players=["Liz", "Monty", "Janet"],
        title="Page 440 Exercise 1"
    )

    # Liz chooses a door first.
    g.append_move(g.root, player="Liz", actions=["A", "B"])

    node_A = g.root.children["A"]
    node_B = g.root.children["B"]

    # Monty observes Liz's choice.
    g.append_move(node_A, player="Monty", actions=["Red_after_A", "Green_after_A"])
    g.append_move(node_B, player="Monty", actions=["Red_after_B", "Green_after_B"])

    node_AR = node_A.children["Red_after_A"]
    node_AG = node_A.children["Green_after_A"]
    node_BR = node_B.children["Red_after_B"]
    node_BG = node_B.children["Green_after_B"]

    # Janet hears Monty's message, so she has one infoset after Red and one after Green.
    g.append_move(node_AR, player="Janet", actions=["ChooseA", "ChooseB"])
    g.append_infoset(node_BR, node_AR.infoset)

    g.append_move(node_AG, player="Janet", actions=["ChooseA", "ChooseB"])
    g.append_infoset(node_BG, node_AG.infoset)

    # Janet's terminal nodes after Red.
    ar_a = node_AR.children["ChooseA"]
    ar_b = node_AR.children["ChooseB"]
    br_a = node_BR.children["ChooseA"]
    br_b = node_BR.children["ChooseB"]

    # Janet's terminal nodes after Green.
    ag_a = node_AG.children["ChooseA"]
    ag_b = node_AG.children["ChooseB"]
    bg_a = node_BG.children["ChooseA"]
    bg_b = node_BG.children["ChooseB"]

    # Payoff order: (Liz, Monty, Janet)
    out_ar_a = g.add_outcome([0, 10, 100], label="LizA_Red_JanetA")
    out_ar_b = g.add_outcome([100, 0, 0], label="LizA_Red_JanetB")

    out_ag_a = g.add_outcome([0, 10, 100], label="LizA_Green_JanetA")
    out_ag_b = g.add_outcome([100, 0, 0], label="LizA_Green_JanetB")

    out_br_a = g.add_outcome([100, 10, 0], label="LizB_Red_JanetA")
    out_br_b = g.add_outcome([0, 0, 100], label="LizB_Red_JanetB")

    out_bg_a = g.add_outcome([100, 10, 0], label="LizB_Green_JanetA")
    out_bg_b = g.add_outcome([0, 0, 100], label="LizB_Green_JanetB")

    g.set_outcome(ar_a, out_ar_a)
    g.set_outcome(ar_b, out_ar_b)

    g.set_outcome(ag_a, out_ag_a)
    g.set_outcome(ag_b, out_ag_b)

    g.set_outcome(br_a, out_br_a)
    g.set_outcome(br_b, out_br_b)

    g.set_outcome(bg_a, out_bg_a)
    g.set_outcome(bg_b, out_bg_b)

    return g


if __name__ == "__main__":
    g = build_page_440_exercise_1()

    out_path = Path(__file__).with_name("game_page440_exercise1.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
