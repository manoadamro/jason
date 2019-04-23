from flask import Blueprint

from jason.api.schema import props, request_schema

blueprint = Blueprint("logging", __name__)


class LogQuery(props.Model):
    logger = props.String(nullable=True)
    level = props.String(default="DEBUG")
    start = props.Datetime(nullable=True)
    end = props.Datetime(nullable=True)
    service = props.String(nullable=True)
    module = props.String(nullable=True)
    func = props.String(nullable=True)
    lineno = props.Int(nullable=True)
    message = props.String(nullable=True)
    limit = props.Int(default=-1)
    index = props.Int(default=-1)


@blueprint.route("/", methods=["GET"])
@request_schema(query=LogQuery, json=False, form=False)
def get_logs(query):
    ...
