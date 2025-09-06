"""
Lightweight object loader/saver for TTFG instances.
"""

import os
import pickle
from pathlib import Path
from typing import List, Any


def save_objects(objects: List[Any], output_dir: str) -> None:
    """
    Save objects to individual .pkl files in the specified directory.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for i, obj in enumerate(objects):
        filepath = out / f"instance_{i}.pkl"
        with open(filepath, "wb") as f:
            pickle.dump(obj, f)


def load_objects(directory: str) -> List[Any]:
    """
    Load all .pkl objects from the specified directory (sorted by filename).
    Returns a list of deserialized objects.
    """
    d = Path(directory)
    if not d.exists():
        raise FileNotFoundError(f"Directory does not exist: {d}")

    files = sorted([f for f in d.iterdir() if f.suffix == ".pkl"])
    instances: List[Any] = []

    for filepath in files:
        with open(filepath, "rb") as f:
            instances.append(pickle.load(f))

    return instances