#!/bin/sh
python main.py
python manager.py db init
python manager.py db migrate
python manager.py db upgrade