# Verification status

This fork was checked on Linux with Python 3.12, Node.js 24, GCC 14, Rust
1.100, OpenVINO 2026.0 and SciPy 1.16.

## Reproducible checks

From the repository root, create a virtual environment, install
`AOS for Own Projects/requirements.txt`, and run:

```sh
python verify_core.py
```

The smoke test executes the supplied OpenVINO model on CPU, plans a route,
undistorts a synthetic image, and compiles the Unix drone communication
library. The Rust database server was checked with:

```sh
cd "AOS for Own Projects/SERV"
cargo check --workspace --locked
```

The WebGL simulator was installed with `npm ci`, checked with ESLint, and
served successfully over a local HTTP server. The waypoint planner now contains
the previously missing Node package files; both its Express UI and FastAPI
endpoint were smoke-tested locally.

## Platform-dependent checks

- The C++ light-field renderer reaches the link stage on Linux. Running it
  requires the system GLFW3 and Assimp libraries plus a working OpenGL display.
- The AOS ground station requires Windows, Visual Studio, the DJI SDK5 remote
  controller, FFmpeg/NVIDIA dependencies, Mosquitto and compatible DJI drones.
- Serial flight control requires a supported drone connected to the configured
  Unix serial device.
- The DJI Android application requires Android Studio, DJI SDK credentials and
  compatible DJI hardware.

These components cannot be honestly certified end-to-end without their target
hardware and operating system. Their source and portable subcomponents were
syntax-checked; the repository README files describe the required integration
environment.
