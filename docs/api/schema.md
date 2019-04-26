# jason.api.schema

Used for validating content in flask requests.

documentation for schema properties and models is [here](../core/schema.md)

### `request_schema(...)`

```python
from jason.schema import *


# Schemas can be defined with either a model or inline.

class MyRequestSchema:
  
    class Args(Model):
        q = String(default="something")
        i = Int(nullable=True)

    json = Inline(props={"q": String(default="something")})


@request_schema(model=MyRequestSchema)
def some_route(q, json):
    ...


@request_schema(
    args=Nested(MyRequestSchema.Args),
    json=Inline(props={"q": String(default="something")})
)
def some_route(q, json):
    ...

# the decorated method will work like pytest fixtures
# in the way that you can have validatable elements passed to it, regardless of validation rules.
# simply by adding it to the signature.

# NOTE: view_args (args) will not be packaged as a dict but passed individually.

# example:

@request_schema(
    args=Nested(MyRequestSchema.Args),
    json=Inline(props={"something": String(default="hello")})
)
def some_route(q, i, json):
    ...


@request_schema(
    args=Nested(MyRequestSchema.Args),
    json=Inline(props={"something": String(default="hello")})
)
def some_route(q, i, json):  # this will receive the url args and json
    ...

@request_schema(
    args=Nested(MyRequestSchema.Args),
    json=Inline(props={"something": String(default="hello")})
)
def some_route(json):  # this will receive only the json
    ...

@request_schema(
    args=Nested(MyRequestSchema.Args),
    json=Inline(props={"something": String(default="hello")})
)
def some_route(q, i, query, form, json):  # this will receive everything (form and query will be un-validated)
    ...

```
