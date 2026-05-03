from pathlib import Path
import re
import argparse


VERSION_PATTERN = re.compile(r"(?i)(?:^|[_\-\s])v([0-5])(?:$|[_\-\s.]|\.efg$)")


def extract_version(filename: str) -> str | None:
    """
    Extract version number from filenames such as:
    - game_figure_2_7_c_v0.efg
    - v0.efg
    - Game V3.efg
    """
    match = VERSION_PATTERN.search(filename)
    if match:
        return f"v{match.group(1)}"
    return None


def rename_efg_files(root_dir: Path, dry_run: bool = True) -> None:
    efg_dirs = [p for p in root_dir.rglob("EFG") if p.is_dir()]

    if not efg_dirs:
        print(f"No EFG/ folders found under: {root_dir}")
        return

    renamed = 0
    unchanged = 0
    skipped = 0

    for efg_dir in efg_dirs:
        efg_files = sorted(efg_dir.glob("*.efg"))

        if not efg_files:
            continue

        print(f"\nEFG folder: {efg_dir}")

        planned_renames = []

        for efg_file in efg_files:
            version = extract_version(efg_file.name)

            if version is None:
                print(f"  SKIP: cannot detect version number in {efg_file.name}")
                skipped += 1
                continue

            target = efg_dir / f"{version}.efg"

            if efg_file.name == target.name:
                print(f"  KEEP: {efg_file.name}")
                unchanged += 1
                continue

            planned_renames.append((efg_file, target))

        # Safety check: avoid overwriting existing files accidentally.
        for source, target in planned_renames:
            if target.exists() and target != source:
                print(
                    f"  SKIP: cannot rename {source.name} -> {target.name} "
                    f"because {target.name} already exists"
                )
                skipped += 1
                continue

            print(f"  RENAME: {source.name} -> {target.name}")

            if not dry_run:
                source.rename(target)

            renamed += 1

    print("\nSummary")
    print(f"  Renamed:   {renamed}")
    print(f"  Unchanged: {unchanged}")
    print(f"  Skipped:   {skipped}")

    if dry_run:
        print("\nDry run only. Re-run with --apply to actually rename files.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename .efg files inside every EFG/ folder to v0.efg ... v5.efg."
    )
    parser.add_argument(
        "root",
        type=Path,
        help="Root dataset directory, e.g. EFG-Dataset",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually rename files. Without this flag, only prints planned changes.",
    )

    args = parser.parse_args()

    if not args.root.exists():
        raise FileNotFoundError(f"Root directory does not exist: {args.root}")

    rename_efg_files(args.root, dry_run=not args.apply)


if __name__ == "__main__":
    main()
    