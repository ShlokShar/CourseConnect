import flask
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_socketio import SocketIO
from flask_socketio import send, emit
import flask_socketio

database = SQLAlchemy()
