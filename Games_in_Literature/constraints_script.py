from pathlib import Path
import json
import argparse
import pygambit


def is_chance_node(node):
    """Return True if the node belongs to Chance."""
    return node.player is not None and node.player.is_chance


def node_type(node):
    """Return the node type used in the constraint JSON."""
    return "Chance" if is_chance_node(node) else "Decision"


def player_label(node):
    """Return the player label used in the EFG."""
    if is_chance_node(node):
        return "Chance"
    return str(node.player.label)


def json_payoff_value(value):
    """
    Convert a PyGambit payoff value into a JSON-friendly value.
    Integer-looking values are stored as integers.
    Other values are stored as floats or strings.
    """
    text = str(value)

    try:
        return int(text)
    except ValueError:
        pass

    try:
        return float(text)
    except ValueError:
        return text


def is_nonzero(value):
    """Return True if a payoff value is non-zero."""
    return str(value) not in {"0", "0.0", "0/1"}


def terminal_path(node):
    """
    Return the path from the root to a terminal node.
    Each step records the acting node type, player, and action.
    """
    steps = []

    while node.parent is not None:
        parent = node.parent
        action = str(node.prior_action.label)

        steps.append({
            "type": node_type(parent),
            "player": player_label(parent),
            "action": action
        })

        node = parent

    return list(reversed(steps))


def terminal_payoffs(node, game):
    """Return terminal payoffs as a dictionary keyed by player label."""
    return {
        str(player.label): json_payoff_value(node.outcome[player])
        for player in game.players
    }


def has_nonzero_payoff_for_all_players(node, game):
    """Return True if every player receives a non-zero payoff at this terminal node."""
    if node.outcome is None:
        return False

    return all(is_nonzero(node.outcome[player]) for player in game.players)


def find_first_terminal_with_outcome(game):
    """Return the first terminal node that has an assigned outcome."""
    for node in game.nodes:
        if node.is_terminal and node.outcome is not None:
            return node
    return None


def find_first_seed_terminal(game):
    """
    Return the first terminal node where all players have non-zero payoffs.
    If none exists, return None.
    """
    for node in game.nodes:
        if node.is_terminal and has_nonzero_payoff_for_all_players(node, game):
            return node
    return None


def build_payoff_seed_constraint(efg_path):
    """
    Build a Type 1 payoff-seeding constraint from a V0 EFG file.

    Preference:
    1. First terminal node where all players have non-zero payoffs.
    2. If none exists, first terminal node with any assigned outcome.
    """
    game = pygambit.read_efg(str(efg_path))

    terminal = find_first_seed_terminal(game)
    used_fallback = False

    if terminal is None:
        terminal = find_first_terminal_with_outcome(game)
        used_fallback = True

    if terminal is None:
        return None, False

    path_steps = terminal_path(terminal)

    if used_fallback:
        comment = (
            "Type 1 is a payoff-seeding constraint for one terminal path. "
            "No terminal path with non-zero payoffs for all players was found, "
            "so the first terminal path with an assigned outcome was used."
        )
    else:
        comment = "Type 1 is a payoff-seeding constraint for one terminal path."

    constraint = {
        "Cst Type": 1,
        "Path": {
            str(i + 1): step
            for i, step in enumerate(path_steps)
        },
        "Payoffs": terminal_payoffs(terminal, game),
        "Comments": comment
    }

    return constraint, used_fallback


def generate_constraint_for_entry(v0_efg_path, indent=4, overwrite=True):
    """
    Generate constraints/cst1_payoff_seed.json for one game entry.
    The input path should be something like Game_Example/EFG/v0.efg.
    """
    game_dir = v0_efg_path.parent.parent
    constraints_dir = game_dir / "constraints"
    output_path = constraints_dir / "constraint1.json"

    if output_path.exists() and not overwrite:
        return {
            "status": "skipped_existing",
            "input": v0_efg_path,
            "output": output_path,
            "fallback": False,
            "error": None
        }

    try:
        constraint, used_fallback = build_payoff_seed_constraint(v0_efg_path)
    except Exception as exc:
        return {
            "status": "error",
            "input": v0_efg_path,
            "output": output_path,
            "fallback": False,
            "error": str(exc)
        }

    if constraint is None:
        return {
            "status": "no_terminal_outcome",
            "input": v0_efg_path,
            "output": output_path,
            "fallback": False,
            "error": None
        }

    constraints_dir.mkdir(exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(constraint, f, indent=indent, ensure_ascii=False)

    return {
        "status": "written",
        "input": v0_efg_path,
        "output": output_path,
        "fallback": used_fallback,
        "error": None
    }


def generate_constraints_for_dataset(dataset_root, indent=4, overwrite=True):
    """Find every EFG/v0.efg under the dataset root and generate constraint JSON files."""
    dataset_root = Path(dataset_root)
    v0_files = sorted(dataset_root.rglob("EFG/v0.efg"))

    results = []

    for v0_efg in v0_files:
        result = generate_constraint_for_entry(
            v0_efg_path=v0_efg,
            indent=indent,
            overwrite=overwrite
        )
        results.append(result)

    return results


def print_summary(results):
    """Print a concise summary of generation results."""
    total = len(results)
    written = sum(1 for r in results if r["status"] == "written")
    skipped = sum(1 for r in results if r["status"] == "skipped_existing")
    fallback = sum(1 for r in results if r["fallback"])
    no_terminal = sum(1 for r in results if r["status"] == "no_terminal_outcome")
    errors = sum(1 for r in results if r["status"] == "error")

    print("\nSummary")
    print("-------")
    print(f"V0 EFG files found: {total}")
    print(f"Constraint JSON files written: {written}")
    print(f"Skipped existing files: {skipped}")
    print(f"Fallback paths used: {fallback}")
    print(f"No terminal outcome found: {no_terminal}")
    print(f"Errors: {errors}")

    if fallback:
        print("\nEntries using fallback path:")
        for r in results:
            if r["fallback"]:
                print(f"- {r['input']}")

    if no_terminal:
        print("\nEntries with no terminal outcome:")
        for r in results:
            if r["status"] == "no_terminal_outcome":
                print(f"- {r['input']}")

    if errors:
        print("\nEntries with errors:")
        for r in results:
            if r["status"] == "error":
                print(f"- {r['input']}: {r['error']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dataset_root",
        help="Path to the dataset root folder or a source subdirectory."
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=4,
        help="JSON indentation level. Default is 4."
    )
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="Do not overwrite existing constraint JSON files."
    )

    args = parser.parse_args()

    results = generate_constraints_for_dataset(
        dataset_root=args.dataset_root,
        indent=args.indent,
        overwrite=not args.no_overwrite
    )

    for r in results:
        if r["status"] == "written":
            note = " fallback" if r["fallback"] else ""
            print(f"written{note}: {r['output']}")
        elif r["status"] == "skipped_existing":
            print(f"skipped existing: {r['output']}")
        elif r["status"] == "no_terminal_outcome":
            print(f"no terminal outcome: {r['input']}")
        elif r["status"] == "error":
            print(f"error: {r['input']} -> {r['error']}")

    print_summary(results)


    