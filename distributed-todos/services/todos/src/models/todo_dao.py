import json


class MockDao:
    def __init__(self, path, schema):
        self._path = path
        self._schema = schema
        try:
            with open(self._path, "r") as f:
                self._items = self._schema.load(json.load(f))
        except:
            self._items = []

    def get_all(self):
        return self._items

    def get_by_uuid(self, uuid):
        item = [t for t in self._items if t.uuid == uuid]
        return item[0] if item else None

    def add_item(self, item):
        self._items.append(item)
        self._replace_file()

    def delete_by_uuid(self, uuid):
        item = [t for t in self._items if t.uuid == uuid]
        if item:
            self._items.pop(self._items.index(item[0]))
            self._replace_file()
            return item[0].uuid

    def update_item_by_uuid(self, uuid, data):
        item = self.get_by_uuid(uuid)
        for k, v in data.items():
            setattr(item, k, v)
        self._replace_file()

    def _replace_file(self):
        with open(self._path, "w") as f:
            serialized = self._schema.dump(self._items)
            json.dump(serialized, f)

    def clear(self):
        self._items = []
        self._replace_file()
