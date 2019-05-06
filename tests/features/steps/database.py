import time
from datetime import datetime

from behave import given, then, when

from jason import make_config, service
from jason.ext.sqlalchemy import SQLAlchemy

EXPOSED_FIELDS = ["created", "name"]

db = SQLAlchemy()


@db.serializable(*EXPOSED_FIELDS)
class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String, nullable=False)


def postgres_container(env):
    return env.containers.run(
        "sameersbn/postgresql:10-1",
        name="postgresql",
        hostname="localhost",
        ports={"5432/tcp": 5432},
        environment=["PG_PASSWORD=postgres"],
        detach=True,
    )


@given("we have postgres running")
def step_impl(context):
    context.containers["postgres"] = postgres_container(context.docker)
    time.sleep(10)


@given("we have a postgres service")
def step_impl(context):
    config = make_config("postgres")
    config.DB_HOST = "postgres"

    @service(config)
    def my_simple_api(app):
        db.init_app(app=app, migrate=None)  # optional instance of flask_migrate.Migrate

    context.app = my_simple_api.test_app()
    with context.app.app_context():
        db.create_all()
    context.service = my_simple_api


@when("we create an instance of the model and serialise it")
def step_impl(context):
    with context.app.app_context():
        instance = MyModel(name="something")
        db.session.add(instance)
        db.session.commit()
        db.session.refresh(instance)
    context.instance = instance.to_dict()


@then("only the defined fields are exposed")
def step_impl(context):
    instance = context.instance
    assert len(instance) == len(EXPOSED_FIELDS)
    for field in instance:
        assert field in EXPOSED_FIELDS, f"field '{field}' should not have been exposed"
    assert isinstance(instance["created"], datetime)
    assert instance["name"] == "something"
