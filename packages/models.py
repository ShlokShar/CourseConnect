from packages.imports import *


class Users(database.Model):
    id = database.Column("id", database.Integer, primary_key=True)
    email = database.Column(database.String(100))
    password = database.Column(database.String(100))

    courses = database.Column(database.JSON)
    friends = database.Column(database.JSON)
    past_problems = database.Column(database.JSON)

    def __init__(self, email, password, courses):
        self.email = email
        self.password = password
        self.courses = courses


class Message(database.Model):
    id = database.Column("id", database.Integer, primary_key=True)
    sender = database.Column(database.String(100))
    content = database.Column(database.String(200))

    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
