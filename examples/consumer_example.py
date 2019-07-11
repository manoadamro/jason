"""
To run this, you will need 'flask_sqlalchemy' and 'kombu' installed.

to see config:
python3 -m jason service examples/simple_consumer:my_consumer_api config

to see extension list:
python3 -m jason service examples/simple_consumer:my_consumer_api extensions

to run the service:
python3 -m jason service examples/simple_consumer:my_consumer_api run

"""
from datetime import datetime

from flask import Blueprint, current_app, jsonify
from kombu import Connection, Exchange, Queue

from jason import ServiceThreads, make_config, props, request_schema, service
from jason.ext.sqlalchemy import SQLAlchemy

blueprint = Blueprint("simple-api", __name__)
db = SQLAlchemy()
threads = ServiceThreads()


@db.serializable("created", "name")
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


@service(config_class=make_config("postgres", "rabbit"))
def my_consumer_api(app):
    app.register_blueprint(blueprint)
    db.init_app(app, migrate=None)
    threads.init_app(app)


@threads.thread
def my_consumer():
    # rabbit config is available because we passed "rabbit" to make_config()
    host = current_app.config.RABBIT_HOST
    port = current_app.config.RABBIT_PORT
    username = current_app.config.RABBIT_USER
    password = current_app.config.RABBIT_PASS

    my_exchange = Exchange("thing_exchange", "direct", durable=True)
    my_queue = Queue("thing_queue", exchange=my_exchange, routing_key="my_thingy")

    def on_message(body, message):
        with current_app.app_context():
            create_item(**body)
        message.ack()

    with Connection(
        hostname=host, port=port, userid=username, password=password
    ) as conn:
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
    return jsonify([obj.dict for obj in MyModel.query.all()])
