import datetime
from json import JSONEncoder


class DtJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date | datetime.datetime):
            return o.isoformat()
        return super().default(o)
