"""
To run this, you will need 'flask_sqlalchemy' and 'celery' installed.

to see config:
python3 -m jason service examples/simple_api:my_celery_api config

to see extension list:
python3 -m jason service examples/simple_api:my_celery_api extensions

to run the service:
python3 -m jason service examples/simple_api:my_celery_api run

"""
from datetime import datetime

from flask import Blueprint, jsonify

from jason import JSONEncoder, make_config, props, request_schema, service
from jason.ext.celery import Celery
from jason.ext.sqlalchemy import SQLAlchemy

blueprint = Blueprint("simple_api", __name__)
db = SQLAlchemy()
celery = Celery()


@JSONEncoder.encode_fields("created", "name")
class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String, nullable=False)


class CreateItemSchema:
    name = props.String(min_length=3, max_length=32)


def create_item(name):
    obj = MyModel(name=name)
    db.session.add(obj)
    db.session.commit()


@service(config_class=make_config("postgres", "celery", "rabbit"))
def my_celery_api(app):
    app.register_blueprint(blueprint)
    db.init_app(app=app, migrate=None)  # optional instance of flask_migrate.Migrate
    celery.init_app(app)


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
    return jsonify([obj.dict for obj in MyModel.query.all()])
