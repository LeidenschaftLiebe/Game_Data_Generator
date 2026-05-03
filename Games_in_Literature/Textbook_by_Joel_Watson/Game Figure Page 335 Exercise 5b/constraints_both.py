import argparse
import pygambit


# Recover the sequence of action labels from the root to the given node.
def node_path(node):
    path = []
    while node.parent is not None:
        path.append(str(node.prior_action.label))
        node = node.parent
    return tuple(reversed(path))


# Return the payoff tuple assigned to a terminal node.
# If the node has no outcome, return None.
def node_payoff(node, game):
    if node.outcome is None:
        return None
    return tuple(node.outcome[player] for player in game.players)


# Collect all terminal paths and their corresponding payoff tuples.
def terminal_payoffs(game):
    infos = []
    for node in game.nodes:
        if node.is_terminal:
            infos.append((node_path(node), node_payoff(node, game)))
    return infos


# Find the payoff tuple at a specific terminal path.
# Return None if the path is not found.
def payoff_at_path(game, target_path):
    for node in game.nodes:
        if node.is_terminal and node_path(node) == target_path:
            return node_payoff(node, game)
    return None


# Check a payoff-seeding constraint between a reference EFG and a candidate EFG.
# The check passes if each player has at least one matching nonzero payoff
# along the same terminal path in both games.
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


# Identify whether a node belongs to the chance player.
def is_chance_node(node):
    return node.player is not None and node.player.is_chance


# Collect the path and probability distribution for every chance node in the game.
def chance_infos(game):
    infos = []

    for node in game.nodes:
        if is_chance_node(node):
            probs = tuple(action.prob for action in node.infoset.actions)
            infos.append((node_path(node), probs))

    return infos


# Return the chance probabilities at a specific chance-node path.
# Return None if no chance node exists at that path.
def chance_probs_at_path(game, target_path):
    for node in game.nodes:
        if is_chance_node(node) and node_path(node) == target_path:
            return tuple(action.prob for action in node.infoset.actions)
    return None


# Check whether all chance-node probability distributions in the candidate EFG
# match the corresponding chance-node probabilities in the reference EFG.
def check_all_chance_constraints(reference_efg, input_efg):
    reference_game = pygambit.read_efg(reference_efg)
    input_game = pygambit.read_efg(input_efg)

    reference_infos = chance_infos(reference_game)

    for path, reference_probs in reference_infos:
        input_probs = chance_probs_at_path(input_game, path)
        if input_probs is None:
            return False
        if reference_probs != input_probs:
            return False

    return True


# Command-line entry point.
# The script expects a reference EFG and an input candidate EFG, then prints the results
# of the payoff-seeding check and the chance-probability check.
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("reference_efg")
    parser.add_argument("input_efg")
    args = parser.parse_args()

    print(check_one_nonzero_payoff_per_player(args.reference_efg, args.input_efg))
    print(check_all_chance_constraints(args.reference_efg, args.input_efg))