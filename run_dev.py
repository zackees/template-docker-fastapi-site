"""
Setup development environment
"""

import atexit
import os
import subprocess
import sys
import threading
import time
import webbrowser

import requests  # type: ignore
import uvicorn  # pylint: disable=import-error

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

os.environ["IS_TEST"] = "1"

FASTAPI_PORT = 8000
APP_NAME = "mediabiasscorer"
FASTAPI_APP = f"{APP_NAME}.app:app"
FASTAPI_RELOAD = False  # Reload doesn't work well with VSCode auto-save feature.

NPM_SERVER_PORT = 4999


def run_uvicorn() -> None:
    """Run the Uvicorn server."""
    uvicorn.run(FASTAPI_APP, host="localhost", port=FASTAPI_PORT, reload=FASTAPI_RELOAD)


def run_open_browser() -> None:
    time.sleep(1)
    # Wait for the server to start
    while True:
        try:
            requests.get(f"http://localhost:{FASTAPI_PORT}", timeout=60)
            break
        except requests.exceptions.ConnectionError:
            pass

    webbrowser.open(f"http://localhost:{FASTAPI_PORT}")


def run_npm_server() -> None:
    """Run the npm server."""
    proc = subprocess.Popen(f"npm run start -- --port {NPM_SERVER_PORT}", shell=True, cwd="www")
    atexit.register(proc.kill)

    time.sleep(10)
    rtn = proc.poll()
    if rtn is not None:
        sys.stderr.write("npm server failed to start.\n")
        sys.exit(1)


def run_background_tasks() -> None:
    """Run the background tasks."""
    data: list[subprocess.Popen] = list()

    def kill_proc() -> None:
        if data:
            proc = data[0]
            proc.kill()

    atexit.register(kill_proc)
    while True:
        proc = subprocess.Popen(f"python -m {APP_NAME}.background_tasks", shell=True, cwd=HERE)
        if len(data) == 0:
            data.append(proc)
        else:
            data[0] = proc
        while proc.poll() is None:
            time.sleep(1)


def check_python_dependencies() -> bool:
    """Check all dependencies."""
    # get requirements from requirements.txt
    with open("requirements.txt", encoding="utf-8", mode="r") as f:
        requirements = f.read().splitlines()
    # now add in requirements from requirements.testing.txt
    with open("requirements.testing.txt", encoding="utf-8", mode="r") as f:
        requirements += f.read().splitlines()
    # remove comments
    requirements = [r.split("#")[0].strip() for r in requirements]
    # parse out all the package names
    packages = [r.split("==")[0].strip() for r in requirements]
    packages = [p.strip() for p in packages if p.strip()]
    # clear out empty strings
    packages = [p for p in packages if p]
    # check each package
    import pkg_resources  # pylint: disable=import-outside-toplevel
    any_uninstalled = False
    for package in packages:
        try:
            _ = pkg_resources.get_distribution(package)
            # print(f"{dist.key} ({dist.version}) is installed")
        except pkg_resources.DistributionNotFound:
            print(f"{package} is NOT installed")
            any_uninstalled = True
    return any_uninstalled

def install_deps() -> None:
    python_exe = sys.executable
    subprocess.run(f"{python_exe} -m pip install -e .", shell=True, cwd=HERE, check=False)

ANY_PYTHON_DEPS_UNINSTALLED = check_python_dependencies()
if ANY_PYTHON_DEPS_UNINSTALLED:
    print("Installing dependencies...")
    install_deps()

os.system("cd www && npm install")

# Set environmental variable for internal proxy
os.environ["NPM_SERVER"] = f"http://localhost:{NPM_SERVER_PORT}"

# Manager server processes in a separate thread.
threading.Thread(target=run_npm_server, daemon=True).start()
threading.Thread(target=run_open_browser, daemon=True).start()
threading.Thread(target=run_background_tasks, daemon=True).start()
time.sleep(7)  # give time for the npm server to start.
threading.Thread(target=run_uvicorn, daemon=True).start()

while True:
    time.sleep(10)
