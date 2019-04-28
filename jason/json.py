import datetime
import json

dump = json.dump
dumps = json.dumps

load = json.load
loads = json.loads


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        super(JsonEncoder, self).default(obj)


class JsonDecoder(json.JSONDecoder):
    ...
