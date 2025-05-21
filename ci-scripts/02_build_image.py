# MIT License
#
# Copyright (c) 2025 Andre Temprilho
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


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

