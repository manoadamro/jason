"""
To run this, you will need 'flask_sqlalchemy' and 'celery' installed.

to see config:
python3 -m jason service examples/simple_api:my_simple_api config

to see extension list:
python3 -m jason service examples/simple_api:my_simple_api extensions

to run the service:
python3 -m jason service examples/simple_api:my_simple_api run

"""
from jason import service, make_config, request_schema, props
from flask import Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

blueprint = Blueprint("simple_api", __name__)
db = SQLAlchemy()
celery = Celery()


class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)


class CreateItemSchema:
    name = props.String(min_length=3, max_length=32)


def create_item(name):
    obj = MyModel(name=name)
    db.session.add(obj)
    db.session.commit()


@service(config_class=make_config("postgres", "celery", "rabbit"))
def my_simple_api(app):
    app.register_blueprint(blueprint)
    app.init_sqlalchemy(database=db, migrate=None)  # optional instance of flask_migrate.Migrate
    app.init_celery(celery)


@celery.task
def my_task(item_name):
    create_item(name=item_name)


@blueprint.route("/", methods=["POST"])
@request_schema(json=CreateItemSchema)
def create_item(json):
    create_item(json["name"])
    return jsonify({"success": True}), 201


@blueprint.route("/", methods=["GET"])
def get_item_list():
    return jsonify(
        [{"id": obj.id, "name": obj.name} for obj in MyModel.query.all()]
    )
