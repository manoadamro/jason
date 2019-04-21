# jason.api.schema

```python

import flask
from jason.api import token

app = flask.Flask(__name__)
handler = token.TokenHandler(app=app, key="secret", issuer="someone", audience="someone")


@app.route('/')
@token.protect(token.HasScopes("read:index"))
def index():
    ...
    

@app.route('/user/<user_id>')
@token.protect(token.HasScopes("read:user"), token.MatchValues("jwt:user_id", "url:user_id"))
def index(user_id):
    ...
    
    
```

### Token Handler

```python
import flask
from jason.api import token

app = flask.Flask(__name__)

handler = token.TokenHandler(app=app, key="secret", issuer="someone", audience="someone")

# or

handler = token.TokenHandler(key="secret", issuer="someone", audience="someone")
handler.init_app(app=app)

# or

handler = token.TokenHandler()
handler.init_app(app=app)
handler.configure(key="secret", issuer="someone", audience="someone")

```

#### `__init__`

takes all parameters from `configure` and `init_app`. None are required

#### `init_app`

__app__: instance of a flask app.


#### `configure`

__key__: string key for signing tokens. if the flask app is started before this is configured, an exception is raised

__lifespan__: number of seconds a token lasts for before being considered expired .if the flask app is started before this is configured, an exception is raised

__issuer__: the token issuer. if the flask app is started before this is configured, an exception is raised

__audience__: the token audience. if the flask app is started before this is configured, an exception is raised

__algorithm__: the signing algorithm. (defaults `HS256`)

__verify__: (for testing mode) will not verify tokens if `False` (default `True`)

__auto_update__: if `True`, after each valid request, a token with an updated expiry is returned to the client. (default `False`)

__require_exp__: require an `exp` field in the token (default `True`)

__require_nbf__: require an `nbf` field in the token (default `True`)

__require_iat__: require an `iat` field in the token (default `True`)

__require_aud__: require an `aud` field in the token (default `True`)

__require_iss__: require an `iss` field in the token (default `True`)
 
__verify_signature__: should the tokens signature be verified? (default `True`)

__verify_exp__: should the tokens expiry be verified? (default `True`)

__verify_nbf__: should the tokens "not-before" be verified? (default `True`)

__verify_iat__:  should the tokens "issued-at" be verified? (default `True`)

__verify_aud__:  should the tokens audience be verified? (default `True`)

__verify_iss__:  should the tokens issuer be verified? (default `True`)

---

### Protect

```python
from jason.api import token


@token.protect(token.HasScopes("read:index"))
def index():
    ...
    

@token.protect(token.HasScopes("read:user"), token.MatchValues("jwt:user_id", "json:user/uuid", "url:user_id"))
def index():
    ...
    
    
```

__rules__: one or more token rules to validate tokens against


### Rules

#### `AllOf`

All rules will have to pass in order for the token to be considered valid

__rules__: two or more token rules to validate tokens against. 
 
#### `AnyOf`

At least one rule will have to pass in order for the token to be considered valid

__rules__: two or more token rules to validate tokens against. 

#### `NoneOf`

None of the rules can pass in order for the token to be considered valid

__rules__: two or more token rules to validate tokens against. 

#### `HasScopes`

All scopes will have to exist in the token for it to be considered valid

__scopes__: one or more scopes to check.

#### `HasKeys`

All keys will have to exist in the token for it to be considered valid

__keys__: one or more keys to check.

#### `HasValue`

Value must exist at pointer

__pointer__: json pointer path to a value in the token

__value__: the expected value at the defined pointer


#### `MatchValues`

all values at defined paths must match.
paths are prefixed with object names.

__paths__: one or more prefixed paths, eg. `jwt:path/to/object` or `url:path/to/object`
options are:
- header (request headers)
- json (request json)
- url (url view args)
- query (url query)
- form (request form)
- token

---
