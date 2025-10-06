import os
import importlib.util
import fnmatch

# -------- CONFIGURATION --------
# Directories that contain pygambit builder scripts
source_dirs = [
    os.path.join(os.path.dirname(__file__), "pygambit_src"),
    # os.path.join(os.path.dirname(__file__), "pygambit_src2"),
    # add more directories here if needed
]

# Destination root
dest_root = os.path.join(os.path.dirname(__file__), "EFG")

# How many versions to generate per builder
N_VERSIONS = 20

# Choose which builders to run (match against base name or filename).
# Examples:
# SELECT_BUILDERS = ["pd_builder", "builder_*", "*rps*"]
SELECT_BUILDERS = ["stackelberg"]

# Builders to skip (applied after SELECT_BUILDERS).
# Examples:
# SKIP_BUILDERS = ["wip_*", "tmp*"]
SKIP_BUILDERS = []
# --------------------------------


def _matches_any(name, patterns):
    """Return True if name matches any of the fnmatch patterns in patterns."""
    return any(fnmatch.fnmatch(name, pat) for pat in patterns)


def _should_run(filename):
    """
    Decide whether to run a given filename based on SELECT_BUILDERS / SKIP_BUILDERS.
    Matches against both the full filename (with .py) and the base name (without .py).
    """
    base = os.path.splitext(filename)[0]

    # If SELECT_BUILDERS specified, require a match
    if SELECT_BUILDERS:
        if not (_matches_any(filename, SELECT_BUILDERS) or _matches_any(base, SELECT_BUILDERS)):
            return False

    # Always respect SKIP_BUILDERS if provided
    if SKIP_BUILDERS and (_matches_any(filename, SKIP_BUILDERS) or _matches_any(base, SKIP_BUILDERS)):
        return False

    return True


def main():
    for src in source_dirs:
        # subfolder_name = os.path.basename(src.rstrip(os.sep))
        # dest = os.path.join(dest_root, subfolder_name + "_efg")
        # os.makedirs(dest, exist_ok=True)

        print(f"\n🔄 Processing from {src} → {dest_root}")

        for filename in os.listdir(src):
            if not filename.endswith(".py"):
                continue

            if not _should_run(filename):
                print(f"⏭️  Skipping {filename} (filtered by config)")
                continue

            script_path = os.path.join(src, filename)
            base_name = os.path.splitext(filename)[0]

            # Create a subdir for this script’s runs so v1..vN live together
            script_dest = os.path.join(dest_root, f"{base_name}_efg")
            os.makedirs(script_dest, exist_ok=True)

            for version in range(1, max(1, int(N_VERSIONS)) + 1):
                export_path = os.path.join(script_dest, f"{base_name}_v{version}.efg")

                try:
                    spec = importlib.util.spec_from_file_location("game_module", script_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, "g"):
                        # Prefer to_efg() if provided; fallback to write(format="efg") if necessary
                        if hasattr(module.g, "to_efg"):
                            efg_text = module.g.to_efg()
                        else:
                            # Some pygambit versions expose write(format="efg")
                            efg_text = module.g.write(format="efg")

                        with open(export_path, "w", encoding="utf-8") as f:
                            f.write(efg_text)

                        print(f"✅ Exported {export_path}")
                    else:
                        print(f"⚠️ Skipped {filename}: No 'g' object defined.")
                except Exception as e:
                    print(f"❌ Error processing {filename}: {e}")


if __name__ == "__main__":
    main()
