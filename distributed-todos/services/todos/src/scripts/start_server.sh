#!/bin/bash

gunicorn --config=$GUNICORN_CONFIG --chdir=$TODOS_ROOT/app api:flask_app