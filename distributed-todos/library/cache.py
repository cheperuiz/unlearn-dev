import json


def redis_cachable(r, name, timeout=30):
    def _set_name(f):
        def _redis_cachable(self, uuid):
            key_name = name + "-" + uuid
            if r.exists(key_name):
                s = r.get(key_name)
                return json.loads(s)
            result = f(self, uuid)
            s = json.dumps(result)
            r.set(key_name, s, ex=timeout)
            return result

        return _redis_cachable

    return _set_name

