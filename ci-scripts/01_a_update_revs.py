# MIT License
#
# Copyright (c) 2025 André Temprilho
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
import re
import subprocess

# List of recipes to update SRCREV
# (path is specified from WORKSPACE root dir)
recipes = [
    "pokytos/meta-pokytos/recipes-extended/helloc/helloc_1.0.bb",
    "pokytos/meta-pokytos/recipes-extended/hellocpp/hellocpp_1.8.bb"
]

# Tokens - which strings to look for in each recipe
TOKEN_REPO_URL  = "REPO_URL\s*=\s*"
TOKEN_BRANCH    = "BRANCH\s*=\s*"
TOKEN_SRCREV    = "SRCREV\s*=\s*"

CMD_GIT = "/usr/bin/git"
CMD_CUT = "/usr/bin/cut"



# Searches for TOKEN_REPO_URL and TOKEN_BRANCH inside recipe and returns their values
def _get_url_and_branch(recipe):
    recipe_url = "undefined"
    recipe_branch = "undefined"

    with open (recipe, 'r') as file:
        for line in file:
            match_url = re.match(f'{TOKEN_REPO_URL}"([^"]+)"', line)
            match_branch = re.match(f'{TOKEN_BRANCH}"([^"]+)"', line)

            if match_url:
                recipe_url = match_url.group(1)

            if match_branch:
                recipe_branch = match_branch.group(1)

    # Sanity checks - url and branch must have been found
    if recipe_url == "undefined" or recipe_branch == "undefined":
        print("   ERROR - Missing mandatory recipe variables")
        print("   REPO_URL =")
        print("   BRANCH =")
        print()
        sys.exit(1)

    # Prefix url with https
    recipe_url = f"https://{recipe_url}"
    return recipe_url, recipe_branch



# Returns the latest SRCREV for the recipe's specified BRANCH
def get_latest_srcrev(recipe):
    print(f"Updating {recipe}")
    url, branch = _get_url_and_branch(recipe)

    # git ls-remote to get commit hash from branch's HEAD
    ls_remote = subprocess.Popen(
        [f"{CMD_GIT}", "ls-remote", "--heads", f"{url}", f"{branch}"], stdout=subprocess.PIPE
    )

    pipe_cut = subprocess.Popen(
        [f"{CMD_CUT}", "-f", "1"], stdin=ls_remote.stdout, stdout=subprocess.PIPE
    )

    ls_remote.stdout.close()
    commit, _ = pipe_cut.communicate()
    commit_hash = commit.decode().replace("\n", "")
    return commit_hash



# Writes srcrev in TOKEN_SRCREV variable from recipe
def write_latest_srcrev(recipe, srcrev):

    updated_srcrev_line = f"SRCREV = \"{srcrev}\""

    with open(recipe, 'r') as file:
        lines = file.readlines()

    with open(recipe, 'w') as file:
        for line in lines:
            line = line.replace("\n", "")
            match_srcrev = re.match(f'{TOKEN_SRCREV}"([^"]+)"', line)

            if match_srcrev:
                # Line starts with token.
                # Let's check if the SRCREV diffs from previous value
                if line != updated_srcrev_line:
                    file.write(updated_srcrev_line + '\n')
                    print("-> Updated")
                    print(f"    [OLD] : {line}")
                    print(f"    [NEW] : {updated_srcrev_line}")
                    print()
                else:
                    file.write(line + '\n')
                    print("   No change")
            else:
                file.write(line + '\n')



# "Main()"
# -------------------------------------------------------------------
n_args = len(sys.argv)

if (n_args != 2):
    print("Usage Error!")
    print("")
    print("Usage:")
    print("  python3 01_a_update_revs.py <path-to-host-pokytos-dir>")
    print("")
    sys.exit(1)

# 1st argument: workspace location
workspace = sys.argv[1]

# Iterate over each specified recipe and update its SRCREV to latest
for recipe in recipes:
    recipe_abs_path = f"{workspace}/{recipe}"

    srcrev = get_latest_srcrev(recipe_abs_path)
    write_latest_srcrev(recipe_abs_path, srcrev)
