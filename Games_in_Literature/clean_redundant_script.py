from pathlib import Path
import argparse


TARGET_FILENAME = "constraints.txt"


def find_target_files(root: Path) -> list[Path]:
    """
    Find every constraints.txt file under root.
    """
    return sorted(root.rglob(TARGET_FILENAME))


def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"Remove {TARGET_FILENAME} files under game entry folders."
    )
    parser.add_argument(
        "root",
        type=Path,
        help="Root directory to scan, e.g. Watson-Textbook, GEB, or the whole dataset root.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete files. Without this flag, only prints planned deletions.",
    )

    args = parser.parse_args()
    root = args.root.resolve()
    dry_run = not args.apply

    if not root.exists():
        raise FileNotFoundError(f"Root directory does not exist: {root}")

    target_files = find_target_files(root)

    print(f"Root scanned: {root}")
    print(f"{TARGET_FILENAME} files found: {len(target_files)}")

    if not target_files:
        return

    print("\nDeletion plan:" if dry_run else "\nDeleting files:")

    deleted = 0

    for file_path in target_files:
        rel_path = file_path.relative_to(root)
        print(f"  DELETE: {rel_path}")

        if not dry_run:
            file_path.unlink()

        deleted += 1

    print("\nSummary")
    print(f"  Files matched: {'':<5} {len(target_files)}")
    print(f"  Files deleted: {'':<5} {deleted if not dry_run else 0}")

    if dry_run:
        print("\nDry run only. Re-run with --apply to actually delete files.")


if __name__ == "__main__":
    main()



    