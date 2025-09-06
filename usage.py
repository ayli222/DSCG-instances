"""
Minimal entrypoint for Temporal Team Formation Games (TTFG).

Purpose:
- Demonstrate how to load instances.
- Provide a scaffold for others to add their own schedulers/agents.
"""

import argparse
from pathlib import Path
import objectLoader as loader


def parse_args():
    parser = argparse.ArgumentParser(description="TTFG minimal runner (scaffold only).")
    parser.add_argument(
        "--instances-dir", type=str, required=True,
        help="Directory containing pickled Instance objects (e.g., ./Instances/M-PREF2025_instances/10-agents-biasSTDEV-0)"
    )
    parser.add_argument(
        "--index", type=int, default=0,
        help="Which instance index to load from the directory (default: 0)."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Load instances from the specified directory
    instances = loader.load_objects(args.instances_dir)
    if not instances:
        raise FileNotFoundError(f"No .pkl instances found in {args.instances_dir}")

    idx = min(max(args.index, 0), len(instances) - 1)
    inst = instances[idx]

    # Print a lightweight summary for users
    print("==== TTFG Minimal Scaffold ====")
    print(f"Loaded instance from: {Path(args.instances_dir).resolve()}")
    print(f"Instance index: {idx}")
    print("Instance object summary:")
    inst.print_all()
    print("\nNext steps for contributors:")
    print("  - Import your own scheduler/agent here.")
    print("  - Use the loaded Instance object as input.")
    print("  - Save results in your preferred format.")


if __name__ == "__main__":
    main()