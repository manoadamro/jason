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

handler = token.TokenHandler()
```


### Generate Token

```python
from jason import token

handler = token.TokenHandler()

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

handler = token.TokenHandler()

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

```python

```

TODO

---

## Token Rules

```python

```

TODO

---
