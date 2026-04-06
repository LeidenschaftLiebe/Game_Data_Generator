from pathlib import Path
import pygambit as gbt


def build_geb_peace_negotiation_fig2(mu: str = "1/2", x: str = "0") -> gbt.Game:
    """Construct the peace negotiation example in Fig. 2."""
    g = gbt.Game.new_tree(
        players=["A", "B", "C"],
        title="GEB Peace Negotiation Fig. 2"
    )

    mu_val = gbt.Rational(mu)
    x_val = gbt.Rational(x)

    # Nature chooses the state.
    g.append_move(g.root, g.players.chance, actions=["state_I", "state_II"])
    g.set_chance_probs(g.root.infoset, [mu_val, 1 - mu_val])

    node_I = g.root.children["state_I"]
    node_II = g.root.children["state_II"]

    # A moves without observing the state.
    g.append_move(node_I, player="A", actions=["war", "peace"])
    g.append_infoset(node_II, node_I.infoset)

    node_I_Awar = node_I.children["war"]
    node_I_Apeace = node_I.children["peace"]
    node_II_Awar = node_II.children["war"]
    node_II_Apeace = node_II.children["peace"]

    # B moves after A chose peace, without observing the state.
    g.append_move(node_I_Apeace, player="B", actions=["war", "peace"])
    g.append_infoset(node_II_Apeace, node_I_Apeace.infoset)

    node_I_Bwar = node_I_Apeace.children["war"]
    node_I_Bpeace = node_I_Apeace.children["peace"]
    node_II_Bwar = node_II_Apeace.children["war"]
    node_II_Bpeace = node_II_Apeace.children["peace"]

    # C reacts after failed negotiations in state I.
    # C knows the state, but within state I cannot tell whether A or B caused failure.
    g.append_move(node_I_Awar, player="C", actions=["p_A", "n", "p_B"])
    g.append_infoset(node_I_Bwar, node_I_Awar.infoset)

    # C reacts after successful peace.
    g.append_move(node_I_Bpeace, player="C", actions=["f_A", "f_B"])
    g.append_move(node_II_Bpeace, player="C", actions=["f_B", "f_A"])

    # C reacts after failed negotiations in state II.
    # C knows the state, but within state II cannot tell whether A or B caused failure.
    g.append_move(node_II_Awar, player="C", actions=["p_B", "n", "p_A"])
    g.append_infoset(node_II_Bwar, node_II_Awar.infoset)

    # State I, A chose war.
    out_I_Awar_pA = g.add_outcome([0, 10, 1], label="I_Awar_pA")
    out_I_Awar_n = g.add_outcome([6, 6, x_val], label="I_Awar_n")
    out_I_Awar_pB = g.add_outcome([10, 0, 0], label="I_Awar_pB")

    g.set_outcome(node_I_Awar.children["p_A"], out_I_Awar_pA)
    g.set_outcome(node_I_Awar.children["n"], out_I_Awar_n)
    g.set_outcome(node_I_Awar.children["p_B"], out_I_Awar_pB)

    # State I, B chose war.
    out_I_Bwar_pA = g.add_outcome([0, 10, 0], label="I_Bwar_pA")
    out_I_Bwar_n = g.add_outcome([6, 6, x_val], label="I_Bwar_n")
    out_I_Bwar_pB = g.add_outcome([10, 0, 1], label="I_Bwar_pB")

    g.set_outcome(node_I_Bwar.children["p_A"], out_I_Bwar_pA)
    g.set_outcome(node_I_Bwar.children["n"], out_I_Bwar_n)
    g.set_outcome(node_I_Bwar.children["p_B"], out_I_Bwar_pB)

    # State I, successful peace.
    out_I_peace_fA = g.add_outcome([5, 4, 4], label="I_peace_fA")
    out_I_peace_fB = g.add_outcome([4, 5, 4], label="I_peace_fB")

    g.set_outcome(node_I_Bpeace.children["f_A"], out_I_peace_fA)
    g.set_outcome(node_I_Bpeace.children["f_B"], out_I_peace_fB)

    # State II, A chose war.  CORRECTED
    out_II_Awar_pB = g.add_outcome([10, 0, 0], label="II_Awar_pB")
    out_II_Awar_n = g.add_outcome([6, 6, x_val], label="II_Awar_n")
    out_II_Awar_pA = g.add_outcome([0, 10, 1], label="II_Awar_pA")

    g.set_outcome(node_II_Awar.children["p_B"], out_II_Awar_pB)
    g.set_outcome(node_II_Awar.children["n"], out_II_Awar_n)
    g.set_outcome(node_II_Awar.children["p_A"], out_II_Awar_pA)

    # State II, B chose war.  CORRECTED
    out_II_Bwar_pB = g.add_outcome([10, 0, 1], label="II_Bwar_pB")
    out_II_Bwar_n = g.add_outcome([6, 6, x_val], label="II_Bwar_n")
    out_II_Bwar_pA = g.add_outcome([0, 10, 0], label="II_Bwar_pA")

    g.set_outcome(node_II_Bwar.children["p_B"], out_II_Bwar_pB)
    g.set_outcome(node_II_Bwar.children["n"], out_II_Bwar_n)
    g.set_outcome(node_II_Bwar.children["p_A"], out_II_Bwar_pA)

    # State II, successful peace.
    out_II_peace_fB = g.add_outcome([4, 5, 4], label="II_peace_fB")
    out_II_peace_fA = g.add_outcome([5, 4, 4], label="II_peace_fA")

    g.set_outcome(node_II_Bpeace.children["f_B"], out_II_peace_fB)
    g.set_outcome(node_II_Bpeace.children["f_A"], out_II_peace_fA)

    return g


if __name__ == "__main__":
    g = build_geb_peace_negotiation_fig2(mu="1/2", x="0")

    out_path = Path(__file__).with_name("v0.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")

