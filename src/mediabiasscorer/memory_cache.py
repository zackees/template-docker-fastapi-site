import atexit
import os
import pathlib

from filelock import FileLock

HERE = pathlib.Path(__file__).parent
LOCKPATH = HERE / "memory_cache.lock"

LOCK = FileLock(str(LOCKPATH), timeout=1)

# flake8: noqa: E402
os.environ["SHARED_MEMORY_USE_LOCK"] = "1"

from pydantic import BaseModel
from shared_memory_dict import SharedMemoryDict  # type: ignore

SHARED_MEMORY_NAME = "mediabiasscorer"
SHARED_MEMORY_SIZE = 1024 * 1024


class SharedMemoryData(BaseModel):
    initialized: bool = False


def _delete_shared_memory(smd: SharedMemoryDict):
    smd.shm.close()
    smd.shm.unlink()
    del smd


def _release(smd: SharedMemoryDict) -> None:
    smd.shm.close()
    del smd


@LOCK
def create_shared_memory(owner: bool) -> SharedMemoryDict:
    smd = SharedMemoryDict(name=SHARED_MEMORY_NAME, size=SHARED_MEMORY_SIZE)
    if owner:
        atexit.register(_delete_shared_memory, smd)
    else:
        atexit.register(_release, smd)
    return smd
