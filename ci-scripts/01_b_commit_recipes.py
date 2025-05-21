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

# Git repos where to commit changes
# (path is specified from WORKSPACE root dir)
repos = [
    "pokytos/meta-pokytos/"
]

REMOTE_BRANCH = "debug-ci"
REMOTE_NAME = "filhoDaMain"
COMMIT_MESAGE = f"{REMOTE_BRANCH}-nightly"

CMD_GIT = "/usr/bin/git"



# Commit and push all changes from pevious stage
def commit_with_message(repo, message):
    subprocess.run(
        [f"{CMD_GIT}", "-C", f"{repo}","add", "."]
    )
    subprocess.run(
        [f"{CMD_GIT}", "-C", f"{repo}", "commit", "-m" f"{message}"]
    )

    # Push (from detached HEAD) to remote branch REMOTE_BRANCH
    subprocess.run(
        [f"{CMD_GIT}", "-C", f"{repo}", "push", f"{REMOTE_NAME}", f"HEAD:refs/heads/{REMOTE_BRANCH}"]
    )



# "Main()"
# -------------------------------------------------------------------
n_args = len(sys.argv)

if (n_args != 2):
    print("Usage Error!")
    print("")
    print("Usage:")
    print("  python3 01_b_commit_recipes.py <path-to-host-pokytos-dir>")
    print("")
    sys.exit(1)

# 1st argument: workspace location
workspace = sys.argv[1]

for repo in repos:
    repo_abs_path = f"{workspace}/{repo}"
    commit_with_message(repo_abs_path, COMMIT_MESAGE)
