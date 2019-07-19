import shlex
import subprocess
import time
from datetime import datetime

from behave import given, then, when

from jason import JSONEncoder, jsonify, make_config, service
from jason.ext.sqlalchemy import SQLAlchemy

EXPOSED_FIELDS = ["created", "name"]

db = SQLAlchemy()


@JSONEncoder.encode_fields(*EXPOSED_FIELDS)
class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String, nullable=False)


def create_postgres_container(context):
    if "postgres" in context.containers:
        return context.containers["postgres"]
    container = context.docker.containers.run(
        "sameersbn/postgresql:10-1",
        name="postgresql",
        hostname="localhost",
        ports={"5432/tcp": 5432},
        environment=["PG_PASSWORD=postgres"],
        detach=True,
    )
    context.host = "localhost"
    if not context.is_circle:
        command = shlex.split(f"sh scripts/wait_for_port.sh {context.host} 5432 10")
        subprocess.Popen(command)
    else:
        time.sleep(5)
    context.containers["postgres"] = container
    return container


@given("we have postgres running")
def step_impl(context):
    create_postgres_container(context)


@given("we have a postgres service")
def step_impl(context):
    config = make_config("postgres")
    config.DB_HOST = context.host

    @service(config)
    def my_simple_api(app):
        db.init_app(app=app, migrate=None)  # optional instance of flask_migrate.Migrate

    context.app = my_simple_api.test_app()
    with context.app.app_context():
        db.create_all()
    context.service = my_simple_api


@when("we create a row")
def step_impl(context):
    with context.app.app_context():
        instance = MyModel(name="something")
        db.session.add(instance)
        db.session.commit()


@then("we can select the row again")
def step_impl(context):
    with context.app.app_context():
        obj = MyModel.query.filter_by(name="something").first()
    assert obj is not None
