# pylint: disable=import-error
from uuid import uuid4
from dataclasses import dataclass, field

from marshmallow import Schema, fields, post_load, post_dump


def make_uuid(prefix):
    def _make_uuid():
        return "-".join([prefix, str(uuid4())])

    return _make_uuid


@dataclass(order=True)
class Todo:
    user_id: int = field()
    _id: int = field(compare=False, repr=False)
    uuid: str = field()
    title: str = field()
    completed: bool = field(compare=False)


class TodoSchema(Schema):
    user_id = fields.Integer()
    _id = fields.String(missing="-1")
    uuid = fields.String(missing=make_uuid("TODO"))
    title = fields.String()
    completed = fields.Boolean(missing=False)

    @post_load
    def make_todo(self, data, **kwargs):
        return Todo(**data)

    @post_dump
    def maybe_remove_id(self, data, **kwargs):
        if "_id" in data and data["_id"] == "-1":
            data.pop("_id")
        return data
