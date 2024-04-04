"""
    app worker
"""

import hashlib
import sys

from fastapi.responses import PlainTextResponse
from fastapi_cache import FastAPICache

from mediabiasscorer.init_app import app
from mediabiasscorer.init_frontend_app import init_frontend_app
from mediabiasscorer.memory_cache import SharedMemoryData, create_shared_memory
from mediabiasscorer.settings import IS_TEST

SHARED_MEMORY = create_shared_memory(owner=False)


def load_shared_memory() -> SharedMemoryData:
    return SHARED_MEMORY["shared"]


def store_shared_memory(shared_memory_data: SharedMemoryData) -> None:
    SHARED_MEMORY["shared"] = shared_memory_data


def digest_equals(a: str, b: str) -> bool:
    buff_a = bytes(a, "utf-8")
    buff_b = bytes(b, "utf-8")
    return hashlib.md5(buff_a).digest() == hashlib.md5(buff_b).digest()


@app.on_event("startup")
async def startup():
    FastAPICache.init("fastapi-cache")


@app.get("/api/health", include_in_schema=IS_TEST)
async def health() -> PlainTextResponse:
    return PlainTextResponse(content="OK", status_code=200)


init_frontend_app(app)


def main() -> None:
    """Start the app."""
    sys.stderr.write("Use run_dev.py instead.\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
