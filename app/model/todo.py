import datetime
import enum

from app.application import db
from app.libs.utils import DateUtils


class Status(enum.Enum):
    STARTED = 'STARTED'
    COMPLETED = 'COMPLETED'

    @staticmethod
    def values():
        return [s.value for s in Status]


class Todo(db.Document):
    name = db.StringField(required=True, unique=True)
    status = db.StringField(default=Status.STARTED.value, choices=Status.values())
    start_date = db.DateTimeField(default=datetime.date.today().strftime("%Y-%m-%d"))
    end_date = db.DateTimeField(required=True)
    modified_at = db.DateTimeField(null=True, default=None, onupdate=datetime.date)
    description = db.StringField(null=True, default=None)

    def to_dict(self):
        dict_obj = {}

        for column, value in self._fields.items():
            if column == 'id':
                dict_obj[column] = str(getattr(self, column))
            elif column in ('start_date', 'end_date', 'modified_at'):
                dict_obj[column] = DateUtils.format_date(getattr(self, column)) if getattr(self, column) is not None else None
            else:
                dict_obj[column] = getattr(self, column)

        return dict_obj
