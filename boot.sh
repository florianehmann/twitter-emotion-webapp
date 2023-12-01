#!/bin/bash

source venv/bin/activate
exec gunicorn app_entry:app
