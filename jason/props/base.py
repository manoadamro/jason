from typing import Any


class SchemaAttribute:
    def load(self, value: Any) -> Any:
        raise NotImplementedError


class SchemaRule(SchemaAttribute):
    def load(self, value: Any) -> Any:
        raise NotImplementedError
