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
- [Incoming Requests](#Incoming-Requests)
    - [Content Validation](#Content-Validation)
    - [Request Tokens](#Tokens)
- [Schema](#Schema)
    - [Schema Properties](#Schema-Properties)

---

## Quick Start

```python
# my_service.py

from jason import make_config, service


@service(make_config())
def awesome_service(app, debug):

    if debug:
        print(f"running in debug mode")
    
    # register blueprints
    app.register_blueprint(...)
```

The app can now be run with:
```bash
python3 -m jason my_service run
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
def awesome_service(app, debug):
    # ...app set up happens here...
    ...

```

...or sub-class the `Service` class.

NOTE: you will need to override the `_set_up` method

```python
from jason import make_config, Service

class MyAwesomeService(Service):
    def _set_up(self, app, debug):
        # ...app set up happens here...
        ...

# you will still need an instance defined for the cli to find
awesome_service = MyAwesomeService(make_config())

```

Now, either one can be run with the following.

NOTE: the name you pass in to the CLI is the attribute that your service INSTANCE is assigned to

```bash
python3 -m jason my_service
```

You can define multiple entry points in one file:
```python
from jason import make_config, service

@service(make_config())
def service_1(app, debug):
    # ...app set up happens here...
    ...

@service(make_config())
def service_2(app, debug):
    # ...app set up happens here...
    ...

```

And run them with the following:
```bash
python3 -m jason my_service:service_1
```
```bash
python3 -m jason my_service:service_2
```

---

### Configuring a Service

To create a basic configuration, call `make_config` with flags for each required extension:
```python
from jason import make_config, service

@service(make_config(postgres=True, redis=True))
def awesome_service(app, debug):
    ...
```

To include your custom_configuration
```python
from jason import make_config, props, ServiceConfig, service


class MyConfig(ServiceConfig):
    SOME_VAR = props.Bool(default=True)
    OTHER_VAR = props.Int()

@service(make_config(base=MyConfig, postgres=True, redis=True))
def awesome_service(app, debug):
    ...
```

or build your own configuration:
```python
from jason import props, ServiceConfig, service, mixins


class MyConfig(ServiceConfig, mixins.PostgresConfigMixin, mixins.RedisConfigMixin):
    SOME_VAR = props.Bool(default=True)
    OTHER_VAR = props.Int()


@service(MyConfig)
def awesome_service(app, debug):
    ...
```

see [here](#Schema) for more information about defining a config object

---

### Service Extensions

Jason will also initialise extensions for you. 
The only pre-requisite is that your config either uses the relevant mixin, 
or you use `make_config` 

```python

from jason import ServiceConfig, service, mixins
from flask_sqlalchemy import SQLAlchemy

class MyConfig(ServiceConfig, mixins.PostgresConfigMixin):
    ...

db = SQLAlchemy()

@service(MyConfig)
def awesome_service(app, debug):
    app.init_sqlalchemy(db)
```
Now your app is using SqlAlchemy!

### Extensions

For each extension used, you will need to add the relevant mixin to yor config object.
This can be achieved either by using `make_config` or using the mix in in your class definition.
More info about config and mix ins can be found [here](#Configuring-a-Service)

#### `jason.AppThreads`

Adds threads to the flask app (intended mostly for consumers, see [kombu](https://pypi.org/project/kombu/))

no mix in required. (yet)

([jason.AppThreads docs](#Service-Threads))

#### `flask_sqlalchemy`

```python

from jason import service, make_config
import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

@service(make_config())
def awesome_service(app, debug):
    app.init_sqlalchemy(db)
    
```

NOTE: don't use `db.init_app()`, it won't initialise properly. (it's on the ToDo list)

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

#### `flask_redis`

```python

from jason import service, make_config
import flask_redis

cache = flask_redis.FlaskRedis()

@service(make_config())
def awesome_service(app, debug):
    app.init_redis(cache)
    
```

NOTE: don't use `cache.init_app()`, it won't initialise properly. (it's on the ToDo list)


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
import celery

cel = celery.Celery()

@service(make_config())
def awesome_service(app, debug):
    app.init_celery(cel)
    
```

`CeleryConfigMixin`

| Name                      | Type                        | Default               | Nullable  |
| :-----------------------: | :-------------------------: | :-------------------: | :-------: |
| CELERY_BROKER_BACKEND     | Choice (ampq, redis)        | ampq                  | False     |
| CELERY_RESULTS_BACKEND    | String (ampq, redis)        | ampq                  | False     |
| CELERY_REDIS_DATABASE_ID  | Int                         | 0                     | False     |


Backends:
    
- `ampq`: uses rabbitmq, requires `RabbitConfigMixin` (see below)
- `redis`: uses redis, requires `RedisConfigMixin` (see below)

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

---

### Service Threads

AppThreads allows you to have other processes running along side your flask service (eg. consumers)

```python

from jason import make_config, service, AppThreads

my_threads = AppThreads()

@service(make_config())
def awesome_service(app, debug):
    app.init_threads(my_threads)

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
def awesome_service(app, debug):
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

to run a service in `./my_package/module1`, you would run:
```bash
python3 -m jason my_package.module1
```

to run a service in `./module2`, you would run:
```bash
python3 -m jason module2
```
If not service attribute is defined, jason will pick up the first one it finds.

If your module contains more than one service instances (eg. `my_service` and `my_other_service`), 
you can specify the service you wish to interact with:

```bash
python3 -m jason my_package.module1:my_service
```
```bash
python3 -m jason my_package.module1:my_other_service
```

So, jason can find our services, great, but they don't actually do anything...

introducing service methods!
(following on from the above examples)

### `run`

This will configure the service, call the set up method and run it.

```bash
python3 -m jason my_package.module1:my_service run
```

`--debug`: 
- runs flask app in debug mode (not using waitress).
- uses in memory sqlite database instead of postgres (if database is being used)

`--no-serve`
- acts as a sort of "dry run". configures and calls set up, 
but does not serve the app. (app threads are run as normal)

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

## Incoming Requests

---

### Content Validation

TODO

```python


```

---

### Tokens

TODO

```python


```

---


## Schema

---

### Schema Properties

TODO

```python

```

---
