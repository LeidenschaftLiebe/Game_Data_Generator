import os
import time
import json
from pathlib import Path
import pygambit.gambit as gbt  # use pygambit directly

class EFGValidator:
    def __init__(self):
        # Config path and default root
        self.config_path = Path(__file__).parent / "validator_config.json"
        self._create_config()
        self.results = {}

    def _create_config(self):
        """Create or overwrite the config file each time"""
        default_config = {
            "scan_root": str((Path(__file__).parent / "../Generated_Data/EFG").resolve()),
            "file_patterns": ["*.efg"],
            "report_path": str((Path(__file__).parent / "validation_report.json").resolve())
        }
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)

    def _load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def run(self):
        start_time = time.time()
        config = self._load_config()
        root = Path(config["scan_root"])

        efg_files = []
        if root.exists():
            for pattern in config["file_patterns"]:
                efg_files.extend(root.rglob(pattern))

        print(f"🔍 Found {len(efg_files)} EFG files under {root}...")

        for idx, file in enumerate(efg_files, 1):
            self._validate(file)
            print(f"✅ Validating ({idx}/{len(efg_files)}): {file.name}", end="\r")

        self._save_report(config["report_path"], start_time)
        print(f"\n✅ Validation complete. Report saved to: {config['report_path']}")
        print(f"✅ Summary: {sum(1 for r in self.results.values() if r['valid'])}/{len(self.results)} valid")
        print(f"✅ Summary: {len(self.results) - sum(1 for r in self.results.values() if r['valid'])} invalid")

    def _validate(self, file_path):
        result = {
            "valid": False,
            "error": None,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            gbt.read_efg(str(file_path))  # Validate file
            result["valid"] = True
        except IOError as e:
            result["error"] = f"File read error: {str(e)}"
        except ValueError as e:
            result["error"] = f"Format error: {str(e)}"
        except Exception as e:
            result["error"] = f"Unknown error: {str(e)}"

        self.results[str(file_path)] = result

    def _save_report(self, report_path, start_time):
        report = {
            "metadata": {
                "start_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)),
                "duration": round(time.time() - start_time, 2),
                "total_files": len(self.results),
                "valid_files": sum(1 for r in self.results.values() if r["valid"])
            },
            "details": self.results
        }
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    EFGValidator().run()
