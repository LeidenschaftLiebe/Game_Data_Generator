import argparse
import pygambit


def node_path(node):
    path = []
    while node.parent is not None:
        path.append(str(node.prior_action.label))
        node = node.parent
    return tuple(reversed(path))


def node_payoff(node, game):
    if node.outcome is None:
        return None
    return tuple(node.outcome[player] for player in game.players)


def terminal_payoffs(game):
    infos = []
    for node in game.nodes:
        if node.is_terminal:
            infos.append((node_path(node), node_payoff(node, game)))
    return infos


def payoff_at_path(game, target_path):
    for node in game.nodes:
        if node.is_terminal and node_path(node) == target_path:
            return node_payoff(node, game)
    return None


def check_one_nonzero_payoff_per_player(reference_efg, input_efg):
    reference_game = pygambit.read_efg(reference_efg)
    input_game = pygambit.read_efg(input_efg)

    num_players = len(reference_game.players)
    matched = [False] * num_players
    remaining = num_players

    # Precompute input terminal payoffs by path
    input_payoffs = {
        node_path(node): node_payoff(node, input_game)
        for node in input_game.nodes
        if node.is_terminal
    }

    for node in reference_game.nodes:
        if not node.is_terminal:
            continue

        path = node_path(node)
        reference_payoff = node_payoff(node, reference_game)
        input_payoff = input_payoffs.get(path)

        if input_payoff is None:
            continue

        for i, (ref_value, inp_value) in enumerate(zip(reference_payoff, input_payoff)):
            if matched[i]:
                continue
            if ref_value != 0 and ref_value == inp_value:
                matched[i] = True
                remaining -= 1

        if remaining == 0:
            return True

    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("reference_efg")
    parser.add_argument("input_efg")
    args = parser.parse_args()

    print(check_one_nonzero_payoff_per_player(args.reference_efg, args.input_efg))
