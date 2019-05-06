# jason.token

[back to jason docs](./jason.md)

---

### Table Of Contents:

- [Token Handler](#Token-Handler)
- [Token Protect](#Token-Protect)
- [Token Rules](#Token-Rules)

---

## Token Handler

```python
from jason import token

handler = token.Handler()
```


### Generate Token

```python
from jason import token

handler = token.Handler()

handler.generate_token(...)
```

#### `user_id` (default: None)

Users unique identifier

#### `scopes` (default: [])

a list or tuple of scopes, usually something like `read:thing`, `write:thing`

#### `token_data` (default: None)

A dictionary of data to be stored in the token

#### `not_before` (default: None)

Timestamp representing the earliest time that a token can be used.

### Config Options

```python
from jason import token

handler = token.Handler()

handler.configure(...)
```

#### `key` (default: None)

Key used to sign the tokens. Must be populated before app is run or an error is raised

#### `lifespan` (default: None)

lifespan of tokens, in seconds. Must be populated before app is run or an error is raised

#### `issuer` (default: None)

The tokens issuer.

#### `audience` (default: None)

The tokens audience.

#### `algorithm` (default: HS256)

Algorithm used to sign tokens.

#### `verify` (default: True)

Verify token fields when decoding

#### `auto_update` (default: None)

If true, a token with an upgraded expiry is returned in the headers of each response.

#### `encryption_key` (default: None)

If not `None`, the token is encrypted using `ChaCha20` and the defined key.

#### `require_exp` (default: True)

An error is raised if a token is received without an expiry

#### `require_nbf` (default: True)

An error is raised if a token is received without a "not before"

#### `require_iat` (default: True)

An error is raised if a token is received without an issued time

#### `require_aud` (default: True)

An error is raised if a token is received without an audience

#### `require_iss` (default: True)

An error is raised if a token is received without an issuer

#### `verify_exp` (default: True)

If false, verification of the expiry will be skipped

#### `verify_nbf` (default: True)

If false, verification of the "not before" will be skipped

#### `verify_iat` (default: True)

If false, verification of the "issued at" time will be skipped

#### `verify_aud` (default: True)

If false, verification of the audience will be skipped

#### `verify_iss` (default: True)

If false, verification of the issuer will be skipped

#### `verify_signature` (default: True)

If false, verification of the token signature will be skipped

---

## Token Protect

Used to decorate flask routes.
Takes an unpacked tuple of rules, pulls the token from the request header, decrypts, decodes and validates.

If not rules are provides, it will still ensure that any token string is present

NOTE: a `Handler` will need to have been initialised. 
see [Token Handler](#Token-Handler) and [Service Extensions](./jason.md#Service-Extensions)

```python
from flask import Blueprint
from jason import token

blueprint = Blueprint("my-blueprint", __name__)

@blueprint.route("/")
@token.protect(...)
def my_route():
    ...
```

#### `*rules` (required)

an unpacked tuple of token rules.

---

## Token Rules

Rules used to validate tokens

- [AllOf](#AllOf)
- [AnyOf](#AnyOf)
- [HasKeys](#HasKeys)
- [HasScopes](#HasScopes)
- [HasValue](#HasValue)
- [MatchValues](#MatchValues)
- [NoneOf](#NoneOf)

### AllOf

The token must conform to all of the defined rules.

```python
from jason import token

@token.protect(token.AllOf(..., ...))
def my_route():
    ...
```

#### `*rules` (required)

An unpacked tuple of token rules.

### AnyOf

The token must conform to at least one of the defined rules.

```python
from jason import token

@token.protect(token.AnyOf(..., ...))
def my_route():
    ...
```

#### `*rules` (required)

An unpacked tuple of token rules.

### HasKeys

Ensures that the token body contains all of the defined keys

```python
from jason import token

@token.protect(token.HasKeys("some-key", "another-key"))
def my_route():
    ...
```

#### `*keys` (required)

An unpacked tuple of string keys.

### HasScopes

Ensures that the token contains all of the defined scopes

```python
from jason import token

@token.protect(token.HasScopes("read:thing", "write:thing"))
def my_route():
    ...
```

#### `*scopes` (required)

An unpacked tuple of string scopes.

### HasValue

Ensures that a values is present and valid at a given pointer

If a property or rule from `jason.props` is given as a value, whatever value is found at the pointer will be validated agaisnt it.
Otherwise, the value found must match the value defined.

```python
from jason import token, props

@token.protect(token.HasValue("/thing/id", 123))  # value found must == 123
def my_route():
    ...

@token.protect(token.HasValue("/thing/id", props.Int()))  # value will be validated against defined property
def my_route():
    ...
```

#### `pointer` (required)

A pointer to a value within the token body.

see [jsonpointer](https://pypi.org/project/jsonpointer/) for more info

#### `value` (required)

either a value or a property to match with or validate against.

### MatchValues

ensures that the values at all defined pointers are the same

```python
from jason import token

@token.protect(token.MatchValues("url:user_id", "jwt:user_id"))
def my_route():
    ...
```

Matchers:

#### header

`header:path/to/value`

flask request header

#### json

`json:path/to/value`

flask request json

#### url

`url:path/to/value`

flask request url args eg. `/user/<user_id>`

#### query

`query:path/to/value`

flask request url query eg. `?thing=123&other=something`

#### form

`form:path/to/value`

flask request form

#### token

`token:path/to/value`

flask request token

see [jsonpointer](https://pypi.org/project/jsonpointer/) for more info on pointers

### NoneOf

The token must conform to none of the defined rules.

```python
from jason import token

@token.protect(token.NoneOf(..., ...))
def my_route():
    ...
```

#### `*rules` (required)

An unpacked tuple of token rules.

---
