import os
import importlib.util

# -------- CONFIGURATION --------
# Top-level source and destination root folders
source_root = r"D:\Research Game Data Generator\Generated_Data\pygambit_src"
dest_root = r"D:\Research Game Data Generator\Generated_Data\EFG"
# --------------------------------

# Scan all immediate subdirectories under source_root
source_dirs = [os.path.join(source_root, d) for d in os.listdir(source_root) if os.path.isdir(os.path.join(source_root, d))]

for src in source_dirs:
    subfolder_name = os.path.basename(src)
    dest = os.path.join(dest_root, subfolder_name + "_efg")
    os.makedirs(dest, exist_ok=True)

    print(f"\n🔄 Processing from {src} → {dest}")

    for filename in os.listdir(src):
        if filename.endswith(".py"):
            script_path = os.path.join(src, filename)
            base_name = os.path.splitext(filename)[0]
            export_path = os.path.join(dest, f"{base_name}.efg")

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
