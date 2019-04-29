"""
api.token

"""
import functools
import time
from typing import Any, Callable, Dict, List, NoReturn

import flask
import jsonpointer
import jwt

from . import json
from .crypto import ChaCha20


class TokenValidationError(Exception):
    """
    raised when a token rule fails to validate a token

    """

    ...


class TokenHandlerBase:
    """
    base class for anything needing access to the decoded token
    """

    G_KEY = "_ACCESS_TOKEN"


class TokenHandler(TokenHandlerBase):
    """
    handles the encoding, decoding and generation of jwt tokens

    >>> import flask
    >>> app = flask.Flask(__name__)


    configure all in one
    >>> handler = TokenHandler(app=app, lifespan=600, key="secret", issuer="someone", audience="something")


    configure bit by bit
    >>> handler = TokenHandler()
    >>> handler.init_app(app=app)
    >>> handler.configure(lifespan=600, key="secret", issuer="someone", audience="something")

    """

    HEADER_KEY = "Authorization"
    CIPHER = ChaCha20

    DECODER_OPTIONS = {
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
        self.cipher = None
        self.init_app(app)
        self.configure(**kwargs)

    def init_app(self, app: flask.Flask) -> NoReturn:
        """
        initialises flask app and registers callbacks

        """
        if not app:
            return
        self.app = app
        self.app.before_first_request(self.before_first_request)
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)

    def configure(
        self,
        key: str = None,
        lifespan: int = None,
        issuer: str = None,
        audience: str = None,
        algorithm: str = None,
        verify: bool = None,
        auto_update: bool = None,
        encryption_key: str = None,
        **kwargs: Any,
    ) -> NoReturn:
        """
        sets config values where possible

        """
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
        if encryption_key is not None:
            self.cipher = self.CIPHER(encryption_key)
        for key, value in kwargs.items():
            if key not in self.DECODER_OPTIONS:
                raise ValueError(f"invalid keyword argument {key}")
            self.DECODER_OPTIONS[key] = value

    def _encode(
        self, token_data: Dict[str, Any], json_encoder: Any = json.JsonEncoder
    ) -> str:
        """
        encodes a token from dict to string

        """
        return jwt.encode(
            payload=token_data,
            key=self.key,
            algorithm=self.algorithm,
            json_encoder=json_encoder,
        )

    def _decode(self, token_string: str) -> Dict[str, Any]:
        """
        decodes a token from string to dict

        """
        return jwt.decode(
            jwt=token_string,
            key=self.key,
            verify=self.verify,
            algorithms=[self.algorithm],
            options=self.DECODER_OPTIONS,
            issuer=self.issuer,
            audience=self.audience,
        )

    def before_first_request(self) -> NoReturn:
        """
        ensures that everything is set up correctly

        """
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
        if len(missing) > 0:
            raise ValueError(
                "TokenHandler is missing the values for: " f"{', '.join(missing)}"
            )

    def before_request(self) -> NoReturn:
        """
        gets jwt from header if possible and decodes

        """
        token_string = flask.request.headers.get(self.HEADER_KEY, None)
        if not token_string:
            return
        if self.cipher:
            token_string = self.cipher.decrypt(token_string)
        token_data = self._decode(token_string)
        flask.g[self.G_KEY] = token_data

    def after_request(self, response: flask.Response) -> flask.Response:
        """
        if auto_update is set to true, sends back a token with an updated expiry

        """
        if not self.auto_update:
            return response
        token_data = flask.g[self.G_KEY]
        token_data["exp"] = time.time() + self.lifespan
        token_string = self._encode(token_data=token_data)
        if self.cipher:
            token_string = self.cipher.encrypt(token_string)
        response.headers[self.HEADER_KEY] = token_string
        return response

    def generate_token(self, user_id, scopes, token_data=None, not_before=None):
        """
        generates a token based on current config

        """
        token_data = token_data or {}
        token_data["nbf"] = not_before or time.time()
        token_data["uid"] = user_id
        token_data["scp"] = scopes
        token_data["exp"] = time.time() + self.lifespan
        token_data["iss"] = self.issuer
        token_data["aud"] = self.audience
        token_string = self._encode(token_data=token_data)
        if self.cipher:
            token_string = self.cipher.encrypt(token_string)
        return token_string


class TokenRule:
    """
    base class for all token validation rules

    """

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        raise NotImplementedError


class AllOf(TokenRule):
    """
    raises an error if one or more of the defined rules fails

    """

    def __init__(self, *rules: TokenRule):
        self.rules = rules

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        for rule in self.rules:
            try:
                rule.validate(token)
            except TokenValidationError as ex:
                raise TokenValidationError(
                    f"token did not conform to one or more of the defined rules. {ex}"
                )
        return


class AnyOf(TokenRule):
    """
    raises an error if all of the defined rules fails

    """

    def __init__(self, *rules: TokenRule):
        self.rules = rules

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        for rule in self.rules:
            try:
                rule.validate(token)
            except TokenValidationError:
                continue
            else:
                return
        raise TokenValidationError("token did not conform to any of the defined rules")


class NoneOf(TokenRule):
    """
    raises an error unless all of the defined rules fails

    """

    def __init__(self, *rules: TokenRule):
        self.rules = rules

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        for rule in self.rules:
            try:
                rule.validate(token)
            except TokenValidationError:
                continue
            else:
                raise TokenValidationError(
                    "token conformed to one or more of the defined rules"
                )
        return


class HasScopes(TokenRule):
    """
    raises an error unless all of the defined scopes exist in the current jwt

    """

    def __init__(self, *scopes: str):
        self.scopes = scopes

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        if not all(scope in token["scp"] for scope in self.scopes):
            raise TokenValidationError(f"token is missing a required scope")


class HasKeys(TokenRule):
    """
    raises an error unless all of the defined keys exist in the current jwt

    """

    def __init__(self, *keys: str):
        self.keys = keys

    def validate(self, token: Dict[str, Any]) -> NoReturn:

        if not all(key in token for key in self.keys):
            raise TokenValidationError(f"token is missing a required key")


class HasValue(TokenRule):
    """
    raises an error unless all the defined value exists in the current jwt under the defined key

    """

    def __init__(self, pointer: str, value: str):
        if not pointer.startswith("/"):
            pointer = f"/{pointer}"
        self.pointer = pointer
        self.value = value

    def validate(self, token: Dict[str, Any]) -> NoReturn:
        try:
            v = jsonpointer.resolve_pointer(token, self.pointer)
            if v != self.value:
                raise TokenValidationError(
                    f"token value at defined path does not match defined value"
                )
        except jsonpointer.JsonPointerException:
            raise TokenValidationError(f"token is missing a required value")


class MatchValues(TokenRule):
    """
    raises an error unless all of the defined values match

    """

    def __init__(self, *paths: str):
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
            raise TokenValidationError(f"path to value does not exist in token")
        except AssertionError:
            raise TokenValidationError("one or more values do not match")

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


class Protect(TokenHandlerBase):
    """
    intended for use on flask endpoints
    ensures that the current token (stored in g) passes all of the defined rules

    >>> @token_protect(HasScopes("some:thing", "other:thing"), MatchValues("token:user_id", "url:user_id"))
    ... def some_route():
    ...     ...
    """

    def __init__(self, *rules: TokenRule):
        self.rules = AllOf(*rules)

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def call(*args: Any, **kwargs: Any) -> Any:
            token = flask.g[self.G_KEY]
            self.rules.validate(token)
            return func(*args, **kwargs)

        return call


token_protect = Protect
