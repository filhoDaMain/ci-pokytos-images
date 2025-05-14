import subprocess

REPO_TOOL_PATH = "/usr/local/bin/repo"

REPO_MANIFESTS_URL = "https://github.com/filhoDaMain/pokytos.git"
REPO_MANIFESTS_BRANCH = "nanbield"
REPO_MANIFESTS_MANIFESTFILE = "default.xml"

# repo init
subprocess.run([f"{REPO_TOOL_PATH}", "init", \
    "-b", f"{REPO_MANIFESTS_BRANCH}",\
    "-m", f"{REPO_MANIFESTS_MANIFESTFILE}",\
    "-u", f"{REPO_MANIFESTS_URL}"]
)

# repo sync
subprocess.run([f"{REPO_TOOL_PATH}", "sync"])
