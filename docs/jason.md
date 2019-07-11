# Jason

Jason is a framework for building flask based micro services.

### Table Of Contents:

- [Quick Start](#Quick-Start)
- [Services](#Services)
    - [Creating a Service](#Creating-a-Service)
    - [Configuring a Service](#Configuring-a-Service)
    - [Service Extensions](#Service-Extensions)
    - [Service Threads](#Service-Threads)
    - [Command Line Interface](#Command-Line-Interface)
    - [Testing a Service](#Testing-a-Service)
- [Schema](#Schema)
    - [Content Validation](#Content-Validation)
- [Request Tokens](#Request-Tokens)
- [Jsonification](#Jsonification)
- [Cryptography](#Cryptography)

---

## Quick Start

```python
# my_service.py

from jason import make_config, service


@service(make_config())
def awesome_service(app):
    # register blueprints
    app.register_blueprint(...)
```

The app can now be run with:
```bash
python3 -m jason service my_service run
```

More information on running a service can be found [here](#Command-Line-Interface)

---

## Services

---

### Creating a Service

Define a service using the decorator:
```python
from jason import make_config, service

@service(make_config())
def awesome_service(app):
    # ...app set up happens here...
    ...

```

...or sub-class the `Service` class.

NOTE: you will need to override the `_set_up` method

```python
from jason import make_config, Service

class MyAwesomeService(Service):
    def _set_up(self, app):
        # ...app set up happens here...
        ...

# you will still need an instance defined for the cli to find
awesome_service = MyAwesomeService(make_config())

```

Now, either one can be run with the following.

NOTE: the name you pass in to the CLI is the attribute that your service INSTANCE is assigned to

```bash
python3 -m jason service my_service
```

You can define multiple entry points in one file:
```python
from jason import make_config, service

@service(make_config())
def service_1(app):
    # ...app set up happens here...
    ...

@service(make_config())
def service_2(app):
    # ...app set up happens here...
    ...

```

And run them with the following:
```bash
python3 -m jason service service my_service:service_1 run
```
```bash
python3 -m jason service my_service:service_2 run
```

---

### Configuring a Service

To create a basic configuration, call `make_config` with flags for each required extension:
```python
from jason import make_config, service

@service(make_config("postgres", "redis"))
def awesome_service(app):
    ...
```

To include your custom_configuration

NOTE: you will need to sub-class `ServiceConfig`
```python
from jason import make_config, props, ServiceConfig, service


class MyConfig(ServiceConfig):
    SOME_VAR = props.Bool(default=True)
    OTHER_VAR = props.Int()

@service(make_config("postgres", "redis", base=MyConfig))
def awesome_service(app):
    ...
```

or build your own configuration:

NOTE: you will need to sub-class `ServiceConfig`
```python
from jason import props, ServiceConfig, service, mixins


class MyConfig(ServiceConfig, mixins.PostgresConfigMixin, mixins.RedisConfigMixin):
    SOME_VAR = props.Bool(default=True)
    OTHER_VAR = props.Int()


@service(MyConfig)
def awesome_service(app):
    ...
```

possible flags for `make_config`:

- redis
- rabbit
- postgres
- celery

see [here](#Schema) for more information about defining a config object

---

### Service Extensions

Jason will also initialise extensions (that have been imported from `jason.ext`) for you.
 
For each extension used, you will need to add the relevant mixin to yor config object.
This can be achieved either by using `make_config` or using the mix in in your class definition.
More info about config and mix ins can be found [here](#Configuring-a-Service)

#### `sqlalchemy`

```python

from jason import service, make_config
from jason.ext.sqlalchemy import SQLAlchemy  # you will need flask_sqlalchemy installed

db = SQLAlchemy()

@service(make_config("postgres"))
def awesome_service(app):
    db.init_app(app)
    
```

With migrations:

```python
from jason import service, make_config
from jason.ext.sqlalchemy import SQLAlchemy  # you will need flask_sqlalchemy installed
from jason.ext.migrate import Migrate # you will need flask_migrate installed

db = SQLAlchemy()
migrate = Migrate()

@service(make_config("postgres"))
def awesome_service(app):
    db.init_app(app, migrate=migrate)
    
awesome_service_app = awesome_service.app()

```

```bash
export FLASK_APP=path.to.file.awesome_service_app
```

models in `jason.ext.sqlalchemy` also provide a feature to serialise them to a dict.

```python
import datetime
from jason.ext.sqlalchemy import SQLAlchemy  # you will need flask_sqlalchemy installed

db = SQLAlchemy()

@db.serializable("created", "name")
class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    name = db.Column(db.String, nullable=False)
    
   
def some_method():
    obj = MyModel.query.first()
    return obj.dict

```


`PostgresConfigMixin`

| Name          | Type          | Default               | Nullable  |
| :-----------: | :------------:| :-------------------: | :-------: |
| TEST_DB_URL   | String        | sqlite:///:memory:    | False     |
| DB_DRIVER     | String        | postgresql            | False     |
| DB_HOST       | String        | localhost             | False     |
| DB_PORT       | Int           | 5432                  | False     |
| DB_USER       | String        | None                  | True      |
| DB_PASS       | String        | None                  | True      |

[flask_sqlalchemy docs](https://pypi.org/project/Flask-SQLAlchemy/)

#### `redis`

```python

from jason import service, make_config
from jason.ext.redis import Redis  # you will need flask_redis installed

redis = Redis()

@service(make_config("redis"))
def awesome_service(app):
    redis.init_app(app)
    
```

`RedisConfigMixin`

| Name             | Type          | Default               | Nullable  |
| :--------------: | :------------:| :-------------------: | :-------: |
| REDIS_DRIVER     | String        | redis                 | False     |
| REDIS_HOST       | String        | localhost             | False     |
| REDIS_PORT       | Int           | 6379                  | False     |
| REDIS_PASS       | String        | None                  | True      |

([flask_redis docs](https://pypi.org/project/Flask-Redis/))

#### `celery`

```python

from jason import service, make_config
from jason.ext.celery import Celery  # you will need celery installed

celery = Celery()

@service(make_config())
def awesome_service(app):
    celery.init_app(app)
    
```

`CeleryConfigMixin`

| Name                      | Type                        | Default               | Nullable  |
| :-----------------------: | :-------------------------: | :-------------------: | :-------: |
| CELERY_BROKER_BACKEND     | Choice (ampq, redis)        | ampq                  | False     |
| CELERY_RESULTS_BACKEND    | Choice (ampq, redis)        | ampq                  | False     |
| CELERY_REDIS_DATABASE_ID  | Int                         | 0                     | False     |


Backends:
    
- `redis`: uses redis, requires `RedisConfigMixin` (see above)
- `ampq`: uses rabbitmq, requires `RabbitConfigMixin` (see below)

([celery docs](https://pypi.org/project/celery/))

#### `rabbit`

This one isn't really an extension, it's just a mix in for rabbitmq

`RabbitConfigMixin`

| Name          | Type          | Default               | Nullable  |
| :-----------: | :------------:| :-------------------: | :-------: |
| RABBIT_DRIVER | String        | ampq                  | False     |
| RABBIT_HOST   | String        | localhost             | False     |
| RABBIT_PORT   | Int           | 5672                  | False     |
| RABBIT_USER   | String        | guest                 | False     |
| RABBIT_PASS   | String        | guest                 | False     |

#### `token_handler`

```python
from jason import service, make_config, token

token_handler = token.Handler()

@service(make_config())
def awesome_service(app):
    token_handler.init_app(app)
```

More information about request tokens can be found [here](#Request-Tokens)

---

### Service Threads

ServiceThreads allows you to have other processes running along side your flask service (eg. consumers)

```python

from jason import make_config, service, ServiceThreads

my_threads = ServiceThreads()

@service(make_config())
def awesome_service(app):
    my_threads.init_app(app)

# with no parameters
@my_threads.thread
def consumer_thread(app):
    # this is running on a thread.
    # use app_context to interact with flask
    ...
        
```

---

### Command Line Interface

Commands are run using `jason -m ...`
```python
# my_service.py

from jason import service

@service(...)
def awesome_service(app):
    ...
```
To invoke Jason CLI, run `python3 jason -m ...`

The first positional argument is the module containing the service:

assuming you have the following structure:

```
- root (cwd)
  - my_package/
    - module1
  - module2
```

to run a service in `./my_package/module1`:
```bash
python3 -m jason service my_package.module1
```

to run a service in `./module2`:
```bash
python3 -m jason service module2
```
If no service attribute is defined, jason will pick up the first one it finds.

If your module contains more than one service instances (eg. `my_service` and `my_other_service`), 
you can specify the service you wish to interact with:

```bash
python3 -m jason service my_package.module1:my_service
```
```bash
python3 -m jason service my_package.module1:my_other_service
```

### `run`

This will configure the service, call the set up method and run it.

```bash
python3 -m jason service my_package.module1:my_service run
```

`--debug`: 
- runs flask app in debug mode (not using waitress).
- uses `TEST_DB_URL` for database

`--no-serve`
- acts as a sort of "dry run". configures and calls set up, 
but does not serve the app. (threads will run as normal). 
This is useful if you only want to run the threads, with no flask app

`--detach`
- runs as daemon thead.
The app will is configured, set up and run as daemon.
The process will exit but everything will be running in the background.
 
`**config values`
- These are custom values that will override config values that were defined as defaults or in environment variables.

eg: `--my-var=123` would override `MY_VAR` in config with a value of `123`

```bash
python3 -m my_service config --debug --my-var=123
```

### `config`

This will configure the service, call the set up method and log the contents of config to the stdout.
This is useful to ensure that your service definition is producing the results expected

To ensure that the resulting config is identical to what would be produced when calling `run`,
you can pass in the following parameters from the `run` method. 

`--debug`, `**config values`

see `run` command for more info on these.

```bash
python3 -m my_service config --debug --my-var=123
```

### `extensions`

This will configure the service, call the set up method and log the initialised extension names as a comma separated list.

To ensure that the resulting list is identical to what would be produced when calling `run`,
you can pass in the following parameters from the `run` method. 

`--debug`, `**config values`

see `run` command for more info on these.

```bash
python3 -m my_service extensions --debug --my-var=123
```

---


### Testing a Service

```python
# my_service.py

from jason import service

@service(...)
def awesome_service(app):
    ...


# test_my_service.py
from flask import Flask
import pytest

@pytest.fixture
def my_awesome_service():
    config_values = {}  # dictionary of config values
    return awesome_service.test_app(**config_values)
    
def test_service(my_awesome_service):
    assert isinstance(my_awesome_service, Flask)

    
```


## Schema

Schema properties are used to validate bits of data. 

You can validate individual values:
```python
from jason import props

prop = props.Int()

prop.load(123)
# 123

prop.load("hello")
# props.PropertyValidationError
```

... or entire structures:
```python
from jason import props

class MySchema(props.Model):
    x = props.Int()
    y = props.String()

prop = props.Nested(MySchema)

prop.load({"x": 123, "y": "hello"})
```

Full documentation for `jason.props` can be found [here](./props.md)

---

### Content Validation

Used to validate `flask` requests.

request schemas can be defined in a few different ways.

using models:
```python
from jason import request_schema, props
from flask import Blueprint

blueprint = Blueprint("my-bp", __name__)


class MyRouteSchema:
    
    # using a nested class
    class Query(props.Model):
        q = props.String()
        id= props.Int()
    
    # using an inline model
    jason = props.Inline(props=dict(...))

    # from another model
    form = props.Nested(...)
    
    # from a compound object
    args = props.Compound(...) 
    
    

@blueprint.route("/")
@request_schema(MyRouteSchema)
def my_route():
    ...
```

... or inline:
```python
from jason import request_schema, props
from flask import Blueprint

blueprint = Blueprint("my-bp", __name__)


@blueprint.route("/")
@request_schema(json=props.Inline(props=dict(...)), form=props.Nested(...), args=props.Compound(...) )
def my_route():
    ...

```

`RequestSchema` used method inspection to work out what to pass to the decorated method.
you can have it pass through any of the following objects, simply by adding it to the method signature.
`args` are passed unpacked, the others are passed as objects. 
Objects don't have to be defined in the request_schema to be passed to the method 
and they don't have to be passed to the method if they are.

- json (json body of request)
- query (url query, eg. `?x=1&y=thing`)
- args (url variables, eg `/user/<user_id>`)
- form (form of passed in the request)

```python
from jason import request_schema, props
from flask import Blueprint

blueprint = Blueprint("my-bp", __name__)


@blueprint.route("/user/<user_id>")
@request_schema(json=props.Inline(props=dict(...)), args=props.Compound(...) )
def my_route(user_id, json):
    ...
    

@blueprint.route("/user/<user_id>")
@request_schema(args=props.Compound(...) )
def my_other_route(user_id, json):
    ...
```

Full documentation for `jason.props` can be found [here](./props.md)

---

## Request Tokens

Request tokens are used for authentication.

```python
from jason import token, service

handler = token.Handler()


@service(...)
def my_service(app):
    handler.configure(...)
    handler.init_app(app)
    

@token.protect(...)
def my_route():
    ...
```


```python
from jason import token
from flask import Blueprint

blueprint = Blueprint("my-bp", __name__)

@blueprint.route("/")
@token.protect(...)
def my_route():
    ...
```

Full documentation for `jason.token` can be found [here](./token.md)

---

## Jsonification

You can define custom json encoders with a decorator,

```python
from jason.service import JSONEncoder


class MyModel:
    x = 12
    y = "thing"
    z = True
    _n = "nope"


@JSONEncoder.encode_object(MyModel)
def serialise_my_model(obj):
    return {
        "x": obj.x,
        "y": obj.y,
        "z": obj.z
    }

'{"x": 12, "y": "thing", "z": true}'

```

you can also automatically serialise every field that doesn't start with `_`.

```python
from jason.service import JSONEncoder

@JSONEncoder.encode_all
class MyModel:
    x = 12
    y = "thing"
    z = True
    _n = "nope"

'{"x": 12, "y": "thing", "z": true}'

```

or define exactly which fields to serialise:

```python
from jason.service import JSONEncoder

@JSONEncoder.encode_fields("x", "y")
class MyModel:
    x = 12
    y = "thing"
    z = True
    _n = "nope"

'{"x": 12, "y": "thing"}'

```

Flasks `jsonify` method has been patched to be slightly extended.
If you pass jsonify an iterable, you can define a field to be used as a key and get back a dict (instead of a list)

```python

from jason.service import JSONEncoder

@JSONEncoder.encode_all
class Thing:
    def __init__(self, uuid, x):
        self.uuid = uuid
        self.x = x
                
"""
flask.jsonify([Thing("1", True), Thing("2", False), Thing("3", True)]).json

[
    {"uuid": "1", "x": True},
    {"uuid": "2", "x": False},
    {"uuid": "3", "x": True},
]
"""


"""
flask.jsonify([Thing("1", True), Thing("2", False), Thing("3", True)], key="uuid").json

{
    "1": {"uuid": "1", "x": True},
    "2": {"uuid": "2", "x": False},
    "3": {"uuid": "3", "x": True},
}
"""

```

---

## Cryptography

This is mostly used internally, but there is a `ChaCha20` cipher that can be used.
It is modified to receive and return strings (not bytes) and the nonce is handled automatically.

```python
from jason.crypto import ChaCha20

# create an instance
cipher = ChaCha20(key="some-secret-key")

# encrypt a messgae
encrypted = cipher.encrypt("a secret message")
# ksuUkdssZTuljO8ZGc829w==---0I3bCFYDPTM=

decrypted = cipher.decrypt(encrypted)
# 'a secret message'
```

---
