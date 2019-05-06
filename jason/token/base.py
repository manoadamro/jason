from typing import Any, Dict, NoReturn


class TokenHandlerBase:
    G_KEY = "_ACCESS_TOKEN"


class TokenRule:
    def validate(self, token: Dict[str, Any]) -> NoReturn:
        raise NotImplementedError
