import sys
import os
import subprocess

n_args = len(sys.argv)

if (n_args != 2):
    print("Usage Error!")
    print("")
    print("Usage:")
    print("  python3 02_build_image.py <path-to-host-pokytos-dir>")
    print("")
    sys.exit(1)

# 1st argument: workspace location
workspace = sys.argv[1]

# export HOST_POKYTOS_DIR (base repo dir to build)
os.environ['HOST_POKYTOS_DIR'] = workspace

# bitbake image
DOCKER_CONTAINER_LAUNCHER_PATH = "/usr/local/bin/pokytos-builder.sh"
IMAGE = "pokytos-console-image"

subprocess.run([f"{DOCKER_CONTAINER_LAUNCHER_PATH}", "bitbake", f"{IMAGE}"])

