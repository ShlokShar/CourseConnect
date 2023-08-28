from packages.imports import *

user_chatroom_association = database.Table('user_chatroom_association',
                                           database.Column('user_id', database.Integer,
                                                           database.ForeignKey('users.id')),
                                           database.Column('chatroom_id', database.Integer,
                                                           database.ForeignKey('chatroom.id'))
                                           )


class Users(database.Model):
    id = database.Column("id", database.Integer, primary_key=True)
    email = database.Column(database.String(100))
    password = database.Column(database.String(100))

    courses = database.Column(database.JSON)
    chatrooms = database.relationship('Chatroom', secondary=user_chatroom_association, back_populates='users')

    def __init__(self, email, password, courses):
        self.email = email
        self.password = password
        self.courses = courses


class Chatroom(database.Model):
    id = database.Column("id", database.Integer, primary_key=True)
    name = database.Column(database.String(100))
    messages = database.relationship("Message", back_populates="chatroom")
    users = database.relationship('Users', secondary=user_chatroom_association, back_populates='chatrooms')

    def __init__(self, user_1, user_2):
        user_a = min(user_1, user_2)
        user_b = max(user_1, user_2)
        self.name = f"{str(user_a)}x{str(user_b)}"
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    @staticmethod
    def get_name(user_1, user_2):
        user_a = min(user_1, user_2)
        user_b = max(user_1, user_2)

        return f"{str(user_a)}x{str(user_b)}"


class Message(database.Model):
    id = database.Column("id", database.Integer, primary_key=True)
    sender = database.Column(database.String(100))
    content = database.Column(database.String(200))

    chatroom_id = database.Column(database.Integer, database.ForeignKey('chatroom.id'))
    chatroom = database.relationship('Chatroom', back_populates='messages')  # Define the relationship here

    def __init__(self, sender, content, chatroom):
        self.sender = sender
        self.content = content
        self.chatroom = chatroom
