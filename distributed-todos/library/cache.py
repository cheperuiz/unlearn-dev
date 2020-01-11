import json
from library.utils import make_jsend_response


def redis_cachable(r, name, timeout=30):
    def _set_name(f):
        def _redis_cachable(self, uuid):
            key_name = name + "-" + uuid
            if r.exists(key_name):
                s = r.get(key_name)
                return make_jsend_response(data=json.loads(s))
            result = f(self, uuid)
            s = json.dumps(result[0]["data"])
            r.set(key_name, s, ex=timeout)
            return result

        return _redis_cachable

    return _set_name


def invalidate_key(r, name):
    def _set_name(f):
        def _invalidate_key(self, uuid):
            key_name = name + "-" + uuid
            r.delete(key_name)
            return f(self, uuid)

        return _invalidate_key

    return _set_name
