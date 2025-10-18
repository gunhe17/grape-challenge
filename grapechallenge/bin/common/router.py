from fastapi import FastAPI, APIRouter
from typing import Any, Callable, List


class Router:
    def __init__(
        self, path: str, methods: List[str], endpoint: Callable[..., Any]
    ):
        self._path = path
        self._methods = methods
        self._endpoint = endpoint

    def register(self, app: FastAPI):
        router = APIRouter()
        router.add_api_route(
            path=self._path,
            methods=self._methods,
            endpoint=self._endpoint,
        )
        app.include_router(router)