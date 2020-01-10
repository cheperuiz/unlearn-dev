import os
from http.client import responses


def make_url(db_config, include_db=True):
    url = db_config["type"]
    url += "://" + db_config["user"]
    url += ":" + db_config["password"]
    url += "@" + db_config["host"]
    url += ":" + db_config["port"]
    if include_db:
        url += "/" + db_config["db"]
    return url


def replace_env(d):
    for k, v in d.items():
        if type(v) is dict:
            d[k] = replace_env(v)
        elif type(v) is str:
            env_var = find_env(v)
            if env_var:
                value = os.environ[env_var[2:-1]]
                d[k] = v.replace(env_var, value)
    return d


def find_env(s):
    start = s.find("${")
    if start < 0:
        return None
    end = s.find("}")
    if end < 0:
        return None
    return s[start : end + 1]


def make_jsend_response(code=200, status="success", data=None, message=None):
    if message is None:
        message = responses[code]
    response = {}
    if 400 <= code < 500:
        status = "fail"
    elif code >= 500:
        status = "error"
    if data is not None:
        response["data"] = _make_response(data)
    response["status"] = status
    response["message"] = message
    return response, code


def _make_response(data):
    resp = {}
    if isinstance(data, list):
        resp["count"] = len(data)
        resp["values"] = data
    else:
        resp = data
    return resp
