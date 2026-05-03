from pathlib import Path
import pygambit as gbt


def build_wesley_humperdinck_game(c: float = 0.5) -> gbt.Game:
    """Construct the Princess Bride signaling game."""
    g = gbt.Game.new_tree(
        players=["Wesley", "Prince"],
        title="Wesley and Humperdinck"
    )

    # Chance selects Wesley's type.
    g.append_move(g.root, g.players.chance, actions=["Strong", "Weak"])
    g.set_chance_probs(g.root.infoset, [0.5, 0.5])

    strong_node = g.root.children["Strong"]
    weak_node = g.root.children["Weak"]

    # Wesley observes his type and chooses whether to stay in bed or get out.
    g.append_move(strong_node, player="Wesley", actions=["Bed_strong", "Out_strong"])
    g.append_move(weak_node, player="Wesley", actions=["Bed_weak", "Out_weak"])

    strong_bed = strong_node.children["Bed_strong"]
    strong_out = strong_node.children["Out_strong"]
    weak_bed = weak_node.children["Bed_weak"]
    weak_out = weak_node.children["Out_weak"]

    # The prince observes Bed versus Out, but not Wesley's type.
    # One infoset after Bed and one infoset after Out.
    g.append_move(strong_bed, player="Prince", actions=["Surrender", "Fight"])
    g.append_infoset(weak_bed, strong_bed.infoset)

    g.append_move(strong_out, player="Prince", actions=["Surrender", "Fight"])
    g.append_infoset(weak_out, strong_out.infoset)

    # Terminal nodes after Bed.
    sb_s = strong_bed.children["Surrender"]
    sb_f = strong_bed.children["Fight"]
    wb_s = weak_bed.children["Surrender"]
    wb_f = weak_bed.children["Fight"]

    # Terminal nodes after Out.
    so_s = strong_out.children["Surrender"]
    so_f = strong_out.children["Fight"]
    wo_s = weak_out.children["Surrender"]
    wo_f = weak_out.children["Fight"]

    # Distinct outcomes.
    out_sb_s = g.add_outcome([1, 0], label="Strong_Bed_Surrender")
    out_sb_f = g.add_outcome([0, -2], label="Strong_Bed_Fight")

    out_wb_s = g.add_outcome([1, 0], label="Weak_Bed_Surrender")
    out_wb_f = g.add_outcome([-1, 1], label="Weak_Bed_Fight")

    out_so_s = g.add_outcome([1, 0], label="Strong_Out_Surrender")
    out_so_f = g.add_outcome([0, -2], label="Strong_Out_Fight")

    out_wo_s = g.add_outcome([1 - c, 0], label="Weak_Out_Surrender")
    out_wo_f = g.add_outcome([-1 - c, 1], label="Weak_Out_Fight")

    # Attach outcomes.
    g.set_outcome(sb_s, out_sb_s)
    g.set_outcome(sb_f, out_sb_f)

    g.set_outcome(wb_s, out_wb_s)
    g.set_outcome(wb_f, out_wb_f)

    g.set_outcome(so_s, out_so_s)
    g.set_outcome(so_f, out_so_f)

    g.set_outcome(wo_s, out_wo_s)
    g.set_outcome(wo_f, out_wo_f)

    return g


if __name__ == "__main__":
    g = build_wesley_humperdinck_game(c=0.5)

    out_path = Path(__file__).with_name("game_figure_page389.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    