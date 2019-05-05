"""
To run this, you will need 'flask_sqlalchemy' installed.

to see config:
python3 -m jason service examples/simple_api:my_simple_api config

to see extension list:
python3 -m jason service examples/simple_api:my_simple_api extensions

to run the service:
python3 -m jason service examples/simple_api:my_simple_api run

"""
from jason import service, make_config, props, request_schema
from flask import Blueprint, jsonify
from jason.ext.sqlalchemy import SQLAlchemy

blueprint = Blueprint("simple_api", __name__)
db = SQLAlchemy()


class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)


class CreateItemSchema:
    name = props.String(min_length=3, max_length=32)


@service(config_class=make_config("postgres"))
def my_simple_api(app):
    app.register_blueprint(blueprint)
    db.init_app(app=app, migrate=None)  # optional instance of flask_migrate.Migrate


@blueprint.route("/", methods=["POST"])
@request_schema(json=CreateItemSchema)
def create_item(json):
    obj = MyModel(name=json["name"])
    db.session.add(obj)
    db.session.commit()
    return jsonify({"success": True}), 201


@blueprint.route("/", methods=["GET"])
def get_item_list():
    return jsonify(
        [{"id": obj.id, "name": obj.name} for obj in MyModel.query.all()]
    )
