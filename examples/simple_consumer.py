"""
To run this, you will need 'flask_sqlalchemy' installed.

to see config:
python3 -m jason examples/simple_api:my_simple_api config

to see extension list:
python3 -m jason examples/simple_api:my_simple_api extensions

to run the service:
python3 -m jason examples/simple_api:my_simple_api run

"""
from jason import service, make_config, request_schema, props, AppThreads
from flask import Blueprint, jsonify, current_app
from kombu import Connection, Consumer, Queue, Exchange
from flask_sqlalchemy import SQLAlchemy


blueprint = Blueprint("simple-api", __name__)
db = SQLAlchemy()
threads = AppThreads()


class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)


class CreateItemSchema:
    name = props.String(min_length=3, max_length=32)


def create_item(name):
    obj = MyModel(name=name)
    db.session.add(obj)
    db.session.commit()


@service(config_class=make_config("postgres", "rabbit"))
def my_simple_api(app):
    app.register_blueprint(blueprint)
    app.init_sqlalchemy(database=db, migrate=None)
    app.init_threads(threads)


@threads.thread
def my_consumer():
    host = current_app.config.RABBIT_HOST
    port = current_app.config.RABBIT_PORT
    username = current_app.config.RABBIT_USER
    password = current_app.config.RABBIT_PASS

    my_exchange = Exchange('media', 'direct', durable=True)
    my_queue = Queue('video', exchange=my_exchange, routing_key='my_thingy')

    def on_message(body, message):
        with current_app.app_context():
            create_item(**body)
        message.ack()

    with Connection(hostname=host, port=port, userid=username, password=password) as conn:
        with conn.Consumer(my_queue, callbacks=[on_message]):
            while True:
                conn.drain_events()


@blueprint.route("/", methods=["POST"])
@request_schema(json=CreateItemSchema)
def create_item(json):
    create_item(name=json["name"])
    return jsonify({"success": True}), 201


@blueprint.route("/", methods=["GET"])
def get_item_list():
    return jsonify(
        [{"id": obj.id, "name": obj.name} for obj in MyModel.query.all()]
    )
