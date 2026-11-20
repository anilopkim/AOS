"""Headless smoke tests for the portable AOS components.

Run from the repository root with a Python environment containing the packages
from ``AOS for Own Projects/requirements.txt``.
"""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_detector() -> None:
    detector_module = load_module(
        "aos_detector", ROOT / "AOS for Own Projects" / "DET" / "detector.py"
    )
    weights = ROOT / "AOS for Own Projects" / "DET" / "weights" / "yolov4-tiny.xml"
    detector = detector_module.Detector()
    detector.init(str(weights), device="CPU")
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    rendered, objects = detector.detect(image)
    assert rendered.shape == image.shape
    assert isinstance(objects, tuple)


def verify_planner() -> None:
    planner_module = load_module(
        "aos_planner", ROOT / "AOS for Own Projects" / "PLAN" / "Planner.py"
    )
    with tempfile.TemporaryDirectory() as results:
        planner = planner_module.Planner(
            (449000.0, 5340000.0, 33, "U"),
            (90.0, 90.0),
            tile_distance=30,
            results_folder=results,
        )
        current = tuple(planner._gps_grid[0, 0])
        points = planner.planpoints(current)
        assert points


def verify_undistortion() -> None:
    camera_module = load_module(
        "aos_undistort", ROOT / "AOS for Own Projects" / "CAM" / "Undistort.py"
    )
    undistort = camera_module.Undistort(new_size=(32, 32))
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    result = undistort.undistort(image)
    assert result.shape == (32, 32, 3)


def verify_drone_library_compiles() -> None:
    source = ROOT / "AOS for Own Projects" / "DRONE" / "dronecommunication.c"
    with tempfile.TemporaryDirectory() as output_dir:
        output = Path(output_dir) / "dronecommunication.so"
        subprocess.run(
            ["cc", "-fPIC", "-shared", "-std=c17", "-o", str(output), str(source)],
            check=True,
        )
        assert output.exists()


if __name__ == "__main__":
    checks = [
        ("OpenVINO detector", verify_detector),
        ("path planner", verify_planner),
        ("camera undistortion", verify_undistortion),
        ("drone C library", verify_drone_library_compiles),
    ]
    for label, check in checks:
        check()
        print(f"PASS: {label}")
