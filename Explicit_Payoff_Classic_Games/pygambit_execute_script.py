import os
import importlib.util

# -------- CONFIGURATION --------
# Top-level source and destination root folders
#source_root = os.path.join(os.path.dirname(__file__), "pygambit_src/player2_action2_zerosum")

# Directories that contain pygambit builder scripts
source_dirs = [
    os.path.join(os.path.dirname(__file__), "pygambit_src/classic_2player_variant"),
    #os.path.join(os.path.dirname(__file__), "pygambit_src2"),
    # add more directories here if needed
]

dest_root = os.path.join(os.path.dirname(__file__), "EFG")
# --------------------------------

# Number of versions to generate for each builder script
n = 20

# Scan all immediate subdirectories under source_root
#source_dirs = [os.path.join(source_root, d) for d in os.listdir(source_root) if os.path.isdir(os.path.join(source_root, d))]

for src in source_dirs:
    #subfolder_name = os.path.basename(src)
    subfolder_name = os.path.basename(src.rstrip(os.sep))
    dest = os.path.join(dest_root, subfolder_name + "_efg")
    os.makedirs(dest, exist_ok=True)

    print(f"\n🔄 Processing from {src} → {dest}")

    for filename in os.listdir(src):
        if filename.endswith(".py"):
            script_path = os.path.join(src, filename)
            base_name = os.path.splitext(filename)[0]
            #export_path = os.path.join(dest, f"{base_name}.efg")

            # create a subdir for this script’s runs
            script_dest = os.path.join(dest, base_name)
            os.makedirs(script_dest, exist_ok=True)

            for version in range(1, n + 1):
                export_path = os.path.join(script_dest, f"{base_name}_v{version}.efg")

                try:
                    spec = importlib.util.spec_from_file_location("game_module", script_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, "g"):
                        with open(export_path, "w", encoding="utf-8") as f:
                            #f.write(module.g.write(format="efg"))
                            f.write(module.g.to_efg())

                        print(f"✅ Exported {export_path}")
                    else:
                        print(f"⚠️ Skipped {filename}: No 'g' object defined.")
                except Exception as e:
                    print(f"❌ Error processing {filename}: {e}")
