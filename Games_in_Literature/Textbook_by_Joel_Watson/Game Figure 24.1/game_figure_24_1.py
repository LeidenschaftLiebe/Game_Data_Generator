from pathlib import Path
import pygambit as gbt


def build_figure_24_1(p: float = 0.5) -> gbt.Game:
    """Construct Watson Figure 24.1: the gift game, with Nature probability p."""
    if not (0.0 <= p <= 1.0):
        raise ValueError("p must be between 0 and 1")

    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Watson Figure 24.1 - Gift Game"
    )

    # Nature chooses whether Player 1 is Friend or Enemy.
    g.append_move(g.root, g.players.chance, actions=["Friend", "Enemy"])
    g.set_chance_probs(g.root.infoset, [p, 1 - p])

    friend_node = g.root.children["Friend"]
    enemy_node = g.root.children["Enemy"]

    # Player 1 knows his type, so these are separate information sets.
    g.append_move(friend_node, player="1", actions=["No gift", "Gift"])
    g.append_move(enemy_node, player="1", actions=["No gift", "Gift"])

    friend_no = friend_node.children["No gift"]
    friend_gift = friend_node.children["Gift"]
    enemy_no = enemy_node.children["No gift"]
    enemy_gift = enemy_node.children["Gift"]

    # If Player 1 offers a gift, Player 2 chooses Accept or Reject.
    # Player 2 cannot observe Player 1's type, so these two nodes are in one infoset.
    g.append_move(friend_gift, player="2", actions=["Accept", "Reject"])
    g.append_infoset(enemy_gift, friend_gift.infoset)

    friend_accept = friend_gift.children["Accept"]
    friend_reject = friend_gift.children["Reject"]
    enemy_accept = enemy_gift.children["Accept"]
    enemy_reject = enemy_gift.children["Reject"]

    # Terminal rewards in the order (Player 1, Player 2).
    outcome_no_gift = g.add_outcome([0, 0], label="No gift")
    outcome_friend_accept = g.add_outcome([1, 1], label="Friend gift accepted")
    outcome_friend_reject = g.add_outcome([-1, 0], label="Friend gift rejected")
    outcome_enemy_accept = g.add_outcome([1, -1], label="Enemy gift accepted")
    outcome_enemy_reject = g.add_outcome([-1, 0], label="Enemy gift rejected")

    # Attach rewards.
    g.set_outcome(friend_no, outcome_no_gift)
    g.set_outcome(enemy_no, outcome_no_gift)
    g.set_outcome(friend_accept, outcome_friend_accept)
    g.set_outcome(friend_reject, outcome_friend_reject)
    g.set_outcome(enemy_accept, outcome_enemy_accept)
    g.set_outcome(enemy_reject, outcome_enemy_reject)

    return g


if __name__ == "__main__":
    g = build_figure_24_1(p=0.5)

    out_path = Path(__file__).with_name("figure_24_1.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")
    