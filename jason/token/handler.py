import json
import time
from typing import Any, Dict, NoReturn

import flask
import jwt
from jason import crypto

from . import base


class Handler(base.TokenHandlerBase):

    HEADER_KEY = "Authorization"
    CIPHER = crypto.ChaCha20

    DECODER_OPTIONS = {
        "require_exp": True,
        "require_nbf": True,
        "require_iat": True,
        "require_aud": True,
        "require_iss": True,
        "verify_exp": True,
        "verify_nbf": True,
        "verify_iat": True,
        "verify_aud": True,
        "verify_iss": True,
        "verify_signature": True,
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
        if not app:
            return
        self.app = app
        self.app.before_first_request(self.before_first_request)
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)
        app.extensions["token-handler"] = self

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
        self, token_data: Dict[str, Any], json_encoder: Any = json.JSONEncoder
    ) -> str:
        return jwt.encode(
            payload=token_data,
            key=self.key,
            algorithm=self.algorithm,
            json_encoder=json_encoder,
        )

    def _decode(self, token_string: str) -> Dict[str, Any]:
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
        missing = []
        if self.algorithm is None:
            self.algorithm = "HS256"
        if self.lifespan is None:
            missing.append("lifespan")
        if self.key is None:
            missing.append("key")
        if self.verify is None:
            self.verify = True
        if len(missing) > 0:
            raise ValueError(
                "Handler is missing the values for: " f"{', '.join(missing)}"
            )

    def before_request(self) -> NoReturn:
        token_string = flask.request.headers.get(self.HEADER_KEY, None)
        if not token_string:
            return
        if self.cipher:
            token_string = self.cipher.decrypt(token_string)
        token_data = self._decode(token_string)
        flask.g[self.G_KEY] = token_data

    def after_request(self, response: flask.Response) -> flask.Response:
        if not self.auto_update:
            return response
        token_data = flask.g[self.G_KEY]
        token_data["exp"] = time.time() + self.lifespan
        token_string = self._encode(token_data=token_data)
        if self.cipher:
            token_string = self.cipher.encrypt(token_string)
        response.headers[self.HEADER_KEY] = token_string
        return response

    def generate_token(self, user_id=None, scopes=(), token_data=None, not_before=None):
        token_data = token_data or {}
        token_data["nbf"] = not_before or time.time()
        token_data["uid"] = user_id
        token_data["scp"] = scopes
        token_data["exp"] = time.time() + self.lifespan
        if self.issuer:
            token_data["iss"] = self.issuer
        if self.audience:
            token_data["aud"] = self.audience
        token_string = self._encode(token_data=token_data)
        if self.cipher:
            token_string = self.cipher.encrypt(token_string)
        return token_string

    def __getattribute__(self, item):
        try:
            return super(Handler, self).__getattribute__(item)
        except AttributeError:
            if item in self.DECODER_OPTIONS:
                return self.DECODER_OPTIONS[item]
            raise
