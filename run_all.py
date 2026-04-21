import subprocess
import sys


CATEGORIES = [
    "bottle",
    "cable",
    "capsule",
    "carpet",
    "grid",
    "hazelnut",
    "leather",
    "metal_nut",
    "pill",
    "screw",
    "tile",
    "toothbrush",
    "transistor",
    "wood",
    "zipper",
]

failures = []

for category in CATEGORIES:
    print(f"\n{'='*50}")
    print(f"  Running: {category}")
    print(f"{'='*50}\n")

    try:
        subprocess.run(
            [sys.executable, "-m", "src.build_memory", "--category", category],
            check=True,
        )
        subprocess.run(
            [sys.executable, "-m", "src.evaluate", "--category", category],
            check=True,
        )
        print(f"\n[DONE] {category} completed successfully.\n")
    except subprocess.CalledProcessError as exc:
        failures.append((category, exc.returncode))
        print(f"\n[ERROR] {category} failed with exit code {exc.returncode}. Continuing...\n")

print(f"\n{'='*50}")
if failures:
    print(f"Completed with {len(failures)} failure(s):")
    for category, returncode in failures:
        print(f"  - {category}: exit code {returncode}")
    sys.exit(1)
else:
    print(f"All {len(CATEGORIES)} categories completed successfully.")
print(f"{'='*50}\n")
