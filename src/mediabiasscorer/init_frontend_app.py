import os

import httpx
from fastapi import FastAPI  # type: ignore
from fastapi.staticfiles import StaticFiles
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import FileResponse, Response, StreamingResponse

from mediabiasscorer.settings import WWW_DIR

USE_GZIP = True
LOCAL_ANALYTICS_PATH = (
    "a95chh80w12o6ivpurgx"  # obfuscates analytics path so ad blockers don't block it
)


class InternalProxy:
    def __init__(self, target_url: str) -> None:
        self.target_url = target_url
        self.client = httpx.AsyncClient(base_url=target_url)

    async def proxy(self, request: Request) -> StreamingResponse:
        print(f"Proxying request to {self.target_url}{request.url.path}")
        url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
        rp_req = self.client.build_request(
            request.method,
            url,
            headers=request.headers.raw,
            content=await request.body(),
        )
        rp_resp = await self.client.send(rp_req, stream=True)
        return StreamingResponse(
            rp_resp.aiter_raw(),
            status_code=rp_resp.status_code,
            headers=rp_resp.headers,
            background=BackgroundTask(rp_resp.aclose),
        )


# PostHog is a great analytics platform, but it's blocked by many ad blockers.
# This proxy allows us to use PostHog without being blocked.
class PostHogProxy:
    def __init__(self, target_url: str = "https://app.posthog.com:443") -> None:
        self.target_url = target_url
        self.client = httpx.AsyncClient(base_url=target_url)

    async def proxy(self, request: Request) -> StreamingResponse:
        # remove the local endpoint from the path
        remote_path = request.url.path.replace(f"/{LOCAL_ANALYTICS_PATH}", "")

        print(f"Proxying request to {self.target_url}{remote_path}")
        url = httpx.URL(path=remote_path, query=request.url.query.encode("utf-8"))

        # Copy headers from the original request, but modify the 'Host' header
        modified_headers = dict(request.headers)
        modified_headers.pop("host", None)  # Remove the existing 'Host' header
        modified_headers["Host"] = "app.posthog.com"  # Set the correct 'Host' header

        rp_req = self.client.build_request(
            request.method,
            url,
            headers=modified_headers,
            content=await request.body(),
        )
        rp_resp = await self.client.send(rp_req, stream=True)

        # Optionally remove 'Access-Control-Allow-Origin' header from response
        modified_resp_headers = dict(rp_resp.headers)
        modified_resp_headers.pop("Access-Control-Allow-Origin", None)

        return StreamingResponse(
            rp_resp.aiter_raw(),
            status_code=rp_resp.status_code,
            headers=modified_resp_headers,
            background=BackgroundTask(rp_resp.aclose),
        )


def get_header_value(headers: list[tuple[bytes, bytes]], key: bytes) -> bytes | None:
    for header_key, header_value in headers:
        if header_key == key:
            return header_value
    return None


class GzippedStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope) -> Response:
        response = await super().get_response(path, scope)

        # Check if the client accepts gzip encoding
        headers = scope.get("headers", [])
        accept_encoding: bytes = get_header_value(headers, b"accept-encoding") or b""
        if b"gzip" in accept_encoding:
            path_dir = str(self.directory)
            gzipped_path = os.path.join(path_dir, path + ".gz")

            if os.path.exists(gzipped_path):
                response = FileResponse(
                    gzipped_path, headers={"Content-Encoding": "gzip"}
                )

        return response


def init_frontend_app(app: FastAPI) -> None:
    npm_server = os.environ.get("NPM_SERVER")

    # Analytics trampoline endpoint.
    post_hog_proxy = PostHogProxy()
    app.add_route(
        path="/a95chh80w12o6ivpurgx{path:path}",
        route=post_hog_proxy.proxy,
        methods=["GET", "POST"],
        include_in_schema=False,
    )
    if npm_server is not None:
        # NPM server will be running in a separate process. Proxy all file requests
        # to it. This allows us to have the live reload feature for quick development.
        internal_proxy = InternalProxy(npm_server)
        app.add_route(
            path="/{path:path}",
            route=internal_proxy.proxy,
            methods=["GET", "POST"],
            include_in_schema=False,
        )
    else:
        # In production, serve the static files directly from the server.
        if USE_GZIP:
            StaticFilesClass = GzippedStaticFiles  # type: ignore
        else:
            StaticFilesClass = StaticFiles  # type: ignore
        app.mount(
            "/",
            StaticFilesClass(directory=WWW_DIR, html=True, check_dir=True),  # type: ignore
            name="www",
        )
