from typing import Any


class SchemaAttribute:
    """
    base class for all props props and rules

    """

    def load(self, value: Any) -> Any:
        """
        Must be overridden in sub-classes

        """
        raise NotImplementedError
