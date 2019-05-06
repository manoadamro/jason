from .. import error

BatchValidationError = error.BatchValidationError


class PropertyValidationError(Exception):
    ...


class RequestValidationError(PropertyValidationError):
    ...
