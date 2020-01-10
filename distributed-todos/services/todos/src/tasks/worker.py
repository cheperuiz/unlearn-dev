import yaml

from celery import Celery

from pymongo import MongoClient
from models.todo_dao import MongoDAO
from models.todo import TodoSchema
from library.utils import replace_env, make_url

with open("/config/todos/default_config.yml", "r") as f:
    config = yaml.load(f, yaml.SafeLoader)
replace_env(config)
url = make_url(config["database"]["mongo"], include_db=False)
client = MongoClient(url)
collection = client.todos.todos_collection


broker_url = make_url(config["celery"]["broker"])
results_backend_url = make_url(config["celery"]["results_backend"])
celery = Celery(__name__, broker=broker_url, backend=results_backend_url)


@celery.task(name="tasks.worker.get_all_todos")
def get_all_todos(dao=MongoDAO(collection, TodoSchema)):
    return TodoSchema(many=True).dump(dao.get_all())
