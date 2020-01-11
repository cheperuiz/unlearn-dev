# pylint: disable=import-error
# pylint: disable=no-name-in-module
from uuid import uuid4

import yaml
from redis import Redis
from flask import Flask, request, g
from flask_cors import CORS
from flask_restplus import Resource, Api, Namespace, reqparse
from marshmallow.exceptions import ValidationError
from pymongo import MongoClient

from models.todo import Todo, TodoSchema
from models.todo_dao import MockDao, MongoDAO
from library.utils import make_url, replace_env, make_jsend_response
from library.cache import redis_cachable, invalidate_key

TODOS_DB = "/todos/database/todos_db.json"

todo_schema = TodoSchema(only=["uuid", "title", "completed", "user_id"])
todos_schema = TodoSchema(only=["uuid", "title", "completed", "user_id"], many=True)


with open("/config/todos/default_config.yml", "r") as f:
    config = yaml.load(f, yaml.SafeLoader)
replace_env(config)
url = make_url(config["database"]["mongo"], include_db=False)
client = MongoClient(url)
collection = client.todos.todos_collection


dao = MongoDAO(collection, TodoSchema)

redis_config = config["database"]["redis"]
r = Redis(
    host=redis_config["host"],
    port=redis_config["port"],
    db=redis_config["db"],
    password=redis_config["password"],
)


# Create resource namespace:
todos_ns = Namespace("todos", description="REST API for TODO resources.")
example_dict = {"title": "A TODO title string.", "completed": False}


@todos_ns.route("/")
class TodosList(Resource):
    def get(self):
        todos = dao.get_all()
        return make_jsend_response(data=todos_schema.dump(todos))

    @todos_ns.param(
        "data", "Todo data (title & completed status).", _in="body", required=True, example=example_dict,
    )
    def post(self):
        parser = reqparse.RequestParser()
        parser = parser.add_argument("title")
        parser = parser.add_argument("completed", default=False)
        params = parser.parse_args()
        try:
            todo = TodoSchema().load(
                {"user_id": 0, "title": params["title"], "completed": params["completed"]}
            )
            dao.add_item(todo)
        except ValidationError as e:
            return make_jsend_response(message=e.args, code=422)
        return make_jsend_response(data=todo.uuid)


@todos_ns.route("/<string:uuid>")
@todos_ns.param("uuid", "Receipt uuid")
class TodosDetails(Resource):
    @redis_cachable(r, "TODO-DETAILS", timeout=10)
    def get(self, uuid):
        todo = dao.get_by_uuid(uuid)
        return make_jsend_response(data=todo_schema.dump(todo)) if todo else make_jsend_response(404)

    @invalidate_key(r, "TODO-DETAILS")
    def delete(self, uuid):
        r = dao.delete_by_uuid(uuid)
        return make_jsend_response(data=uuid) if r else make_jsend_response(code=404)

    @todos_ns.param(
        "data", "Todo data (title & completed status).", _in="body", required=True, example=example_dict,
    )
    @invalidate_key(r, "TODO-DETAILS")
    def put(self, uuid):
        data = request.get_json()
        try:
            data["user_id"] = 0  # should come from g
            e = todo_schema.validate(data)
            if e:
                raise ValidationError(e)
            r = dao.update_by_uuid(uuid, data)
        except ValidationError as e:
            return make_jsend_response(message=e.args, code=422)
        return make_jsend_response(data=uuid) if r else make_jsend_response(code=404)


# Create flask app:
flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = str(uuid4())


# Create API
api = Api(prefix="/todos-api/v1", title="Distributed TODOs REST API", version="0.1", catch_all_404s=True)
api.add_namespace(todos_ns)
api.init_app(flask_app)

CORS(flask_app)
