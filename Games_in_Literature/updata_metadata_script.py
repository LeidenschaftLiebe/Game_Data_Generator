from pathlib import Path
import argparse
import re


ASSETS_BLOCK = """assets:
  - original game tree figure
  - V0-V5 description.txt
  - Pygambit Source Code
  - V0-V5.efg
  - metadata.yml
  - constraints.json
"""


GAME_DIR_MARKERS = {
    "EFG",
    "Game Descriptions",
    "constraints",
    "GameTree.png",
}


def looks_like_game_dir(path: Path) -> bool:
    """
    Treat a directory as a game directory if it contains common game-entry files/folders.
    """
    if not path.is_dir():
        return False

    if (path / "metadata.yml").exists():
        return True

    return any((path / marker).exists() for marker in GAME_DIR_MARKERS)


def find_game_dirs(root: Path) -> list[Path]:
    """
    Recursively find likely game directories under root.
    """
    game_dirs = []

    for path in root.rglob("*"):
        if looks_like_game_dir(path):
            game_dirs.append(path)

    # Also include root itself if it is a game directory.
    if looks_like_game_dir(root):
        game_dirs.append(root)

    # Remove nested duplicates only if needed.
    return sorted(set(game_dirs))


def replace_assets_block(text: str) -> tuple[str, bool]:
    """
    Replace top-level assets: block if present.
    Otherwise append it at the end.
    """
    pattern = re.compile(
        r"(?ms)^assets:\n(?:^[ \t]+.*\n|^\s*-\s+.*\n|^\s*$)*"
    )

    if re.search(r"(?m)^assets:\s*$", text):
        new_text, count = pattern.subn(ASSETS_BLOCK, text, count=1)
        return new_text.rstrip() + "\n", count > 0

    # If no assets field exists, append one.
    new_text = text.rstrip() + "\n" + ASSETS_BLOCK
    return new_text.rstrip() + "\n", True


def update_watson_year(text: str) -> tuple[str, bool]:
    """
    If a source line contains Watson 2002 Strategy..., change only 2002 to 2013.
    Other parts of the source field are preserved.
    """
    changed = False
    lines = []

    for line in text.splitlines(keepends=True):
        if re.match(r"^source:\s*", line) and "Watson, J." in line and "2002" in line and "Strategy:" in line:
            new_line = line.replace("2002", "2013", 1)
            if new_line != line:
                changed = True
            lines.append(new_line)
        else:
            lines.append(line)

    return "".join(lines), changed


def process_metadata_file(path: Path, dry_run: bool) -> dict:
    original = path.read_text(encoding="utf-8")

    updated, source_changed = update_watson_year(original)
    updated, assets_changed = replace_assets_block(updated)

    changed = updated != original

    if changed and not dry_run:
        path.write_text(updated, encoding="utf-8")

    return {
        "path": path,
        "changed": changed,
        "source_changed": source_changed,
        "assets_changed": assets_changed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Check game directories for metadata.yml, count metadata files, "
            "rewrite assets field, and fix Watson source year from 2002 to 2013."
        )
    )
    parser.add_argument(
        "root",
        type=Path,
        help="Root directory to scan, e.g. Watson-Textbook, GEB, or the whole dataset root.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually rewrite files. Without this flag, only prints planned changes.",
    )

    args = parser.parse_args()
    root = args.root.resolve()
    dry_run = not args.apply

    if not root.exists():
        raise FileNotFoundError(f"Root directory does not exist: {root}")

    game_dirs = find_game_dirs(root)

    metadata_files = []
    missing_metadata_dirs = []

    for game_dir in game_dirs:
        metadata_path = game_dir / "metadata.yml"
        if metadata_path.exists():
            metadata_files.append(metadata_path)
        else:
            missing_metadata_dirs.append(game_dir)

    print(f"Root scanned: {root}")
    print(f"Likely game directories found: {len(game_dirs)}")
    print(f"metadata.yml files found: {len(metadata_files)}")
    print(f"Game directories missing metadata.yml: {len(missing_metadata_dirs)}")

    if missing_metadata_dirs:
        print("\nDirectories missing metadata.yml:")
        for d in missing_metadata_dirs:
            print(f"  - {d.relative_to(root)}")

    changed_count = 0
    source_changed_count = 0
    assets_changed_count = 0

    print("\nMetadata update plan:" if dry_run else "\nApplying metadata updates:")

    for metadata_path in sorted(metadata_files):
        result = process_metadata_file(metadata_path, dry_run=dry_run)

        if result["changed"]:
            changed_count += 1

            if result["source_changed"]:
                source_changed_count += 1

            if result["assets_changed"]:
                assets_changed_count += 1

            rel = metadata_path.relative_to(root)
            changes = []

            if result["source_changed"]:
                changes.append("source year 2002 -> 2013")

            if result["assets_changed"]:
                changes.append("assets block")

            print(f"  UPDATE: {rel} ({', '.join(changes)})")
        else:
            print(f"  KEEP:   {metadata_path.relative_to(root)}")

    print("\nSummary")
    print(f"  Likely game directories:        {len(game_dirs)}")
    print(f"  metadata.yml found:             {len(metadata_files)}")
    print(f"  metadata.yml missing:           {len(missing_metadata_dirs)}")
    print(f"  metadata.yml changed:           {changed_count}")
    print(f"  source year fields changed:     {source_changed_count}")
    print(f"  assets fields rewritten/added:  {assets_changed_count}")

    if dry_run:
        print("\nDry run only. Re-run with --apply to actually rewrite files.")


if __name__ == "__main__":
    main()
    