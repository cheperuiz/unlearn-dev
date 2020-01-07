# pylint: disable=import-error
from uuid import uuid4

from flask import Flask
from flask_restplus import Resource, Api, Namespace, reqparse
from marshmallow.exceptions import ValidationError

from models.todo import Todo, TodoSchema
from models.todo_dao import MockDao

TODOS_DB = "/todos/database/todos_db.json"

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
dao = MockDao(TODOS_DB, todos_schema)

# Create resource namespace:
todos_ns = Namespace("todos", description="REST API for TODO resources.")
example_dict = {"title": "A TODO title string.", "completed": False}


@todos_ns.route("/")
class TodosList(Resource):
    def get(self):
        todos = dao.get_all()
        return todos_schema.dump(todos)

    @todos_ns.param(
        "data", "Todo data (title & completed status).", _in="body", required=True, example=example_dict,
    )
    def post(self):
        parser = reqparse.RequestParser()
        parser = parser.add_argument("title")
        parser = parser.add_argument("completed", default=False)
        params = parser.parse_args()
        try:
            todo = todo_schema.load(
                {"user_id": 0, "title": params["title"], "completed": params["completed"]}
            )
            dao.add_item(todo)
        except ValidationError as e:
            return (e.args, 422)
        return todo.uuid


@todos_ns.route("/<string:uuid>")
@todos_ns.param("uuid", "Receipt uuid")
class TodosDetails(Resource):
    def get(self, uuid):
        todo = dao.get_by_uuid(uuid)
        return todo_schema.dump(todo) if todo else ("Not found.", 404)

    def delete(self, uuid):
        uuid = dao.delete_by_uuid(uuid)
        return uuid if uuid else ("Not found", 404)

    @todos_ns.param(
        "data", "Todo data (title & completed status).", _in="body", required=True, example=example_dict,
    )
    def put(self, uuid):
        parser = reqparse.RequestParser()
        parser = parser.add_argument("title")
        parser = parser.add_argument("completed")
        params = parser.parse_args()
        try:
            data = {"user_id": 0, "title": params["title"], "completed": params["completed"]}
            data = {k: v for k, v in data.items() if v is not None}
            dao.update_item_by_uuid(uuid, data)
        except ValidationError as e:
            return (e.args, 422)
        return uuid


# Create flask app:
flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = str(uuid4())

# Create API
api = Api(prefix="/todos-api/v1", title="Distributed TODOs REST API", version="0.1", catch_all_404s=True)
api.add_namespace(todos_ns)
api.init_app(flask_app)
