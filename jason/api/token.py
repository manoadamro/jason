import functools
import time
from typing import Any, Callable, Dict, List, NoReturn

import flask
import jsonpointer
import jwt


class TokenValidationError(Exception):
    ...


class TokenHandlerBase:
    G_KEY = "_ACCESS_TOKEN"


class TokenHandler(TokenHandlerBase):
    HEADER_KEY = "Authorization"
    TOKEN_PREFIX = "Bearer "

    DECODER_OPTIONS = {
        "require_signature": True,
        "require_exp": True,
        "require_nbf": True,
        "require_iat": True,
        "require_aud": True,
        "require_iss": True,
        "verify_signature": True,
        "verify_exp": True,
        "verify_nbf": True,
        "verify_iat": True,
        "verify_aud": True,
        "verify_iss": True,
    }

    def __init__(self, app: flask.Flask = None, **kwargs: Any):
        self.app = app
        self.key = None
        self.lifespan = None
        self.issuer = None
        self.audience = None
        self.algorithm = None
        self.verify = None
        self.auto_update = None
        self.init_app(app)
        super(TokenHandler, self).__init__(**kwargs)

    def init_app(self, app: flask.Flask) -> NoReturn:
        if not app:
            return
        self.app = app
        self.app.before_first_request(self._before_first_request)
        self.app.before_request(self._before_request)
        self.app.after_request(self._after_request)

    def configure(
        self,
        key: str = None,
        lifespan: int = None,
        issuer: str = None,
        audience: str = None,
        algorithm: str = None,
        verify: bool = None,
        auto_update: bool = None,
        **kwargs,
    ) -> NoReturn:
        if key is not None:
            self.key = key
        if lifespan is not None:
            self.lifespan = lifespan
        if issuer is not None:
            self.issuer = issuer
        if audience is not None:
            self.audience = audience
        if algorithm is not None:
            self.algorithm = algorithm
        if verify is not None:
            self.verify = verify
        if auto_update is not None:
            self.auto_update = auto_update
        for key, value in kwargs.items():
            if key not in self.DECODER_OPTIONS:
                raise KeyError  # TODO
            self.DECODER_OPTIONS[key] = value

    def generate_token(self, token_data, user_id, scopes, not_before=None):
        token_data["nbf"] = not_before or time.time()
        token_data["uid"] = user_id
        token_data["scp"] = scopes
        token_data["exp"] = time.time() + self.lifespan
        token_data["iss"] = self.issuer
        token_data["aud"] = self.audience
        return self._encode(token_data=token_data)

    def _encode(self, token_data):
        return jwt.encode(
            payload=token_data,
            key=self.key,
            algorithm=self.algorithm,
            json_encoder=None,  # TODO
        )

    def _decode(self, token_string):
        return jwt.decode(
            jwt=token_string,
            key=self.key,
            verify=self.verify,
            algorithms=[self.algorithm],
            options=self.DECODER_OPTIONS,
            issuer=self.issuer,
            audience=self.audience,
        )

    def _before_first_request(self) -> NoReturn:
        missing = []
        if self.algorithm is None:
            self.algorithm = "HS256"
        if self.lifespan is None:
            missing.append("lifespan")
        if self.key is None:
            missing.append("key")
        if self.issuer is None:
            missing.append("issuer")
        if self.audience is None:
            missing.append("audience")
        if len(missing):
            raise ValueError(
                "TokenHandler is missing the values for: " f"{', '.join(missing)}"
            )

    def _before_request(self) -> NoReturn:
        token_string = flask.request.headers.get(self.HEADER_KEY, None)
        if not token_string or not token_string.startswith(self.TOKEN_PREFIX):
            return
        token_string = token_string[len(self.TOKEN_PREFIX) :]
        # TODO decrypt
        token_data = self._decode(token_string)
        flask.g[self.G_KEY] = token_data

    def _after_request(self, response: flask.Response) -> flask.Response:
        if not self.auto_update:
            return response
        token_data = flask.g[self.G_KEY]
        token_data["exp"] = time.time() + self.lifespan
        token_string = self._encode(token_data=token_data)
        token_string = f"{self.TOKEN_PREFIX}{token_string}"
        # TODO encrypt
        response.headers[self.HEADER_KEY] = token_string
        return response


class TokenRule:
    def validate(self, token):
        raise NotImplementedError


class AllOf(TokenRule):
    def __init__(self, *rules):
        self.rules = rules

    def validate(self, token):
        for rule in self.rules:
            rule.validate(token)
        return


class AnyOf(TokenRule):
    def __init__(self, *rules):
        self.rules = rules

    def validate(self, token):
        for rule in self.rules:
            try:
                rule.validate(token)
            except TokenValidationError:  # TODO
                continue
            else:
                return
        raise TokenValidationError  # TODO


class NoneOf(TokenRule):
    def __init__(self, *rules):
        self.rules = rules

    def validate(self, token):
        for rule in self.rules:
            try:
                rule.validate(token)
            except TokenValidationError:  # TODO
                continue
            else:
                raise TokenValidationError  # TODO
        return


class HasScopes(TokenRule):
    def __init__(self, *scopes):
        self.scopes = scopes

    def validate(self, token):
        if not all(scope in token["scp"] for scope in self.scopes):
            raise TokenValidationError  # TODO


class HasKeys(TokenRule):
    def __init__(self, *keys: str):
        self.keys = keys

    def validate(self, token):
        if not all(key in token for key in self.keys):
            raise TokenValidationError  # TODO


class HasValue(TokenRule):
    def __init__(self, pointer, value):
        if not pointer.startswith("/"):
            pointer = f"/{pointer}"
        self.pointer = pointer
        self.value = value

    def validate(self, token):
        try:
            v = jsonpointer.resolve_pointer(token, self.pointer)
            return v == self.value
        except jsonpointer.JsonPointerException:
            return False


class MatchValue(TokenRule):
    def __init__(self, *paths: str):
        self.matchers: List[(Callable, str)] = [
            self._resolve_path(path) for path in paths
        ]
        if len(self.matchers) < 2:
            raise ValueError(f"MatchValue requires two or more paths")

    def validate(self, token):
        try:
            equal = self._check_equal(
                [matcher[0](matcher[1], token) for matcher in self.matchers]
            )
        except jsonpointer.JsonPointerException:
            raise TokenValidationError  # TODO
        else:
            if not equal:
                raise TokenValidationError  # TODO
        return

    def _resolve_path(self, path: str) -> (Callable, str):
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
    def param(path: str, _: Any) -> Any:
        return jsonpointer.resolve_pointer(flask.request.args, path)

    @staticmethod
    def form(path: str, _: Any) -> Any:
        return jsonpointer.resolve_pointer(flask.request.form, path)

    @staticmethod
    def jwt(path: str, token: Dict) -> Any:
        return jsonpointer.resolve_pointer(token, path)


class TokenProtect(TokenHandlerBase):
    def __init__(self, *rules):
        self.rules = AllOf(*rules)

    def __call__(self, func):
        @functools.wraps(func)
        def call(*args, **kwargs):
            token = flask.g[self.G_KEY]
            if not token:
                raise TokenValidationError  # TODO
            self.rules.validate(token)
            return func(*args, **kwargs)

        return call


token_protect = TokenProtect
