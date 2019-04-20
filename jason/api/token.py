import time
from typing import Any, NoReturn

import flask
import jwt


class TokenHandler:
    HEADER_KEY = "Authorization"
    TOKEN_PREFIX = "Bearer "
    G_KEY = "_ACCESS_TOKEN"

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
                f"TokenHandler is missing the values for: {', '.join(missing)}"
            )

    def _before_request(self) -> NoReturn:
        token_string = flask.request.headers.get(self.HEADER_KEY, None)
        if not token_string or not token_string.startswith(self.TOKEN_PREFIX):
            return
        token_string = token_string[len(self.TOKEN_PREFIX) :]
        token_data = self._decode(token_string)
        flask.g[self.G_KEY] = token_data

    def _after_request(self, response: flask.Response) -> flask.Response:
        if not self.auto_update:
            return response
        token_data = flask.g[self.G_KEY]
        token_data["exp"] = time.time() + self.lifespan
        token_string = self._encode(token_data=token_data)
        token_string = f"{self.TOKEN_PREFIX}{token_string}"
        response.headers[self.HEADER_KEY] = token_string
        return response
