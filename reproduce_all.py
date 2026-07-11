from pathlib import Path
import runpy
import traceback

root = Path(__file__).parent

scripts = sorted(root.glob("fig*.py"))

for script in scripts:

    print(f"Generating {script.stem}...")

    try:
        runpy.run_path(script, run_name="__main__")

    except Exception:
        
        print(f"Failed: {script.name}")
        traceback.print_exc()