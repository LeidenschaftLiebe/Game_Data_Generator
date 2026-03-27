from pathlib import Path
import pygambit as gbt


def build_page_466_exercise_1() -> gbt.Game:
    """Construct Page 466 Exercise 1: simplest poker game."""
    g = gbt.Game.new_tree(
        players=["1", "2"],
        title="Page 466 Exercise 1"
    )

    # Chance deals Player 1 either an Ace or a King.
    g.append_move(g.root, g.players.chance, actions=["Ace", "King"])
    g.set_chance_probs(g.root.infoset, [0.5, 0.5])

    node_ace = g.root.children["Ace"]
    node_king = g.root.children["King"]

    # Player 1 observes the card and chooses Bid or Fold.
    g.append_move(node_ace, player="1", actions=["Bid_A", "Fold_A"])
    g.append_move(node_king, player="1", actions=["Bid_K", "Fold_K"])

    ace_bid = node_ace.children["Bid_A"]
    ace_fold = node_ace.children["Fold_A"]
    king_bid = node_king.children["Bid_K"]
    king_fold = node_king.children["Fold_K"]

    # If Player 1 folds, the game ends.
    out_ace_fold = g.add_outcome([-1, 1], label="Ace_Fold")
    out_king_fold = g.add_outcome([-1, 1], label="King_Fold")
    g.set_outcome(ace_fold, out_ace_fold)
    g.set_outcome(king_fold, out_king_fold)

    # Player 2 responds after a bid, without observing Player 1's card.
    g.append_move(ace_bid, player="2", actions=["Bid", "Fold"])
    g.append_infoset(king_bid, ace_bid.infoset)

    ace_bid_bid = ace_bid.children["Bid"]
    ace_bid_fold = ace_bid.children["Fold"]
    king_bid_bid = king_bid.children["Bid"]
    king_bid_fold = king_bid.children["Fold"]

    # Distinct outcomes for each terminal node.
    out_ace_bid_bid = g.add_outcome([2, -2], label="Ace_Bid_Bid")
    out_ace_bid_fold = g.add_outcome([1, -1], label="Ace_Bid_Fold")

    out_king_bid_bid = g.add_outcome([-2, 2], label="King_Bid_Bid")
    out_king_bid_fold = g.add_outcome([1, -1], label="King_Bid_Fold")

    g.set_outcome(ace_bid_bid, out_ace_bid_bid)
    g.set_outcome(ace_bid_fold, out_ace_bid_fold)
    g.set_outcome(king_bid_bid, out_king_bid_bid)
    g.set_outcome(king_bid_fold, out_king_bid_fold)

    return g


if __name__ == "__main__":
    g = build_page_466_exercise_1()

    out_path = Path(__file__).with_name("game_page466_exercise1.efg")
    g.to_efg(str(out_path))

    print(f"Saved to: {out_path}")