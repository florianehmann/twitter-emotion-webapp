#!/bin/bash

source venv/bin/activate
flask db upgrade
exec gunicorn app_entry:app
