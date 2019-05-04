from typing import Any, Callable, Dict, List, NoReturn

import flask
import jsonpointer

from .. import base, error


class MatchValues(base.TokenRule):
    def __init__(self, *paths: str):
        self.paths = paths
        self.matchers: List[(Callable, str)] = [
            self._resolve_path(path) for path in paths
        ]
        if len(self.matchers) < 2:
            raise ValueError(f"MatchValues requires two or more paths")

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        try:
            assert self._check_equal(
                [matcher[0](matcher[1], token) for matcher in self.matchers]
            )
        except jsonpointer.JsonPointerException:
            raise error.TokenValidationError(f"path to value does not exist in token")
        except AssertionError:
            raise error.TokenValidationError(
                f"one or more values at paths {', '.join(self.paths)} do not match"
            )

    def _resolve_path(self, path: str) -> (Callable, str):
        if ":" not in path:
            raise ValueError(f"invalid path: {path}")
        object_name, pointer = path.split(":")
        if not pointer.startswith("/"):
            pointer = f"/{pointer}"
        if object_name.startswith("_") or not hasattr(self, object_name):
            raise AttributeError(f"invalid match object {object_name}")
        obj: Callable = getattr(self, object_name)
        return obj, pointer

    @staticmethod
    def _check_equal(values: List[Any]) -> bool:
        return all(str(values[0]) == str(rest) for rest in values[1:])

    @staticmethod
    def header(path: str, _: Any) -> Any:
        return jsonpointer.resolve_pointer(flask.request.headers, path)

    @staticmethod
    def json(path: str, _: Any) -> Any:
        return jsonpointer.resolve_pointer(flask.request.json, path)

    @staticmethod
    def url(path: str, _: Any) -> Any:
        return jsonpointer.resolve_pointer(flask.request.view_args, path)

    @staticmethod
    def query(path: str, _: Any) -> Any:
        return jsonpointer.resolve_pointer(flask.request.args, path)

    @staticmethod
    def form(path: str, _: Any) -> Any:
        return jsonpointer.resolve_pointer(flask.request.form, path)

    @staticmethod
    def token(path: str, token: Dict) -> Any:
        return jsonpointer.resolve_pointer(token, path)
