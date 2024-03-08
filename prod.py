import os
import signal
import subprocess
from contextlib import contextmanager

from pathlib import Path

HERE = Path(__file__).parent
WWW = HERE / "www"


# Function to clean up background processes
def cleanup(pro: subprocess.Popen):
    print("Cleaning up background processes...")
    pro.terminate()  # Attempt graceful termination
    try:
        pro.wait(timeout=5)  # Wait up to 5 seconds for process to terminate
    except subprocess.TimeoutExpired:
        pro.kill()  # Force kill if not terminated after timeout


# Context manager to handle process start and cleanup
@contextmanager  # type: ignore
def run_background_process() -> subprocess.Popen:  # type: ignore
    pro: subprocess.Popen | None = None
    try:
        # Switch to using the script's current directory:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Start background processes
        pro = subprocess.Popen(
            [
                "uvicorn",
                "--host",
                "0.0.0.0",
                "--port",
                "80",
                "--workers",
                "8",
                "--forwarded-allow-ips=*",
                "mediabiasscorer.app:app",  # TODO: programmatically pull this name
            ]
        )
        # Trap SIGINT (Ctrl-C) to call the cleanup function
        signal.signal(signal.SIGINT, lambda signum, frame: lambda: cleanup(pro))
        yield pro
    finally:
        if pro:
            cleanup(pro)


def main() -> None:
    os.chdir(str(HERE))
    # run npm build first
    subprocess.run(["npm", "run", "build"], shell=True, check=True, cwd=str(WWW))
    # Use the context manager to run and manage the background process
    process: subprocess.Popen
    with run_background_process() as process:
        # Wait for the background process to finish
        assert process is not None
        try:
            process.wait()
        except KeyboardInterrupt:
            # Handle Ctrl-C
            pass


# Main function
if __name__ == "__main__":
    main()
