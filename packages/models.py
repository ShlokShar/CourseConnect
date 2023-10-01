from packages.imports import *

user_chatroom_association = database.Table('user_chatroom_association',
                                           database.Column('user_id', database.Integer,
                                                           database.ForeignKey('users.id')),
                                           database.Column('chatroom_id', database.Integer,
                                                           database.ForeignKey('chatroom.id'))
                                           )


class Users(database.Model):
    id = database.Column("id", database.Integer, primary_key=True)
    name = database.Column(database.String(100))
    email = database.Column(database.String(100))
    password = database.Column(database.String(100))

    courses = database.Column(database.JSON)
    chatrooms = database.relationship('Chatroom', secondary=user_chatroom_association, back_populates='users')

    def __init__(self, name, email, password, courses):
        self.name = name
        self.email = email
        self.password = password
        self.courses = courses

    def add_chatroom(self, chatroom):
        self.chatrooms.append(chatroom)

    def get_friends(self):
        friends = []
        for chatroom in self.chatrooms:
            friends.append(chatroom.get_friend(self))

        return friends

    def add_friend(self, friend):
        chatroom = Chatroom(self.id, friend.id)
        self.add_chatroom(chatroom)
        friend.add_chatroom(chatroom)

        database.session.add(chatroom)

    @staticmethod
    def get_user(email=None, id=None):
        if email:
            return Users.query.filter_by(email=email).first()
        if id:
            return Users.query.filter_by(id=id).first()


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


class PracticeProblem(database.Model):

    __tablename__ = "practiceproblem"

    id = database.Column("id", database.Integer, primary_key=True)
    chatroom = database.relationship("Chatroom", secondary="chatroom_practiceproblem")

    course = database.Column(database.String(100))
    question = database.Column(database.String(100))
    choices = database.JSON()
    correct_answer = database.Column(database.String(100))

    user_1_answer = database.Column(database.String(100))
    user_2_answer = database.Column(database.String(100))

    def __init__(self, course, question, choices, answer):
        self.course = course
        self.question = question
        self.choices = choices
        self.correct_answer = answer

    def get_user_answer(self, chatroom_id, user_id):
        chatroom = Chatroom.query.filter_by(id=chatroom_id)
        user_1, user_2 = map(int, chatroom.name.split("x"))

        if user_id == user_1:
            return self.user_1_answer
        else:
            return self.user_2_answer

    def get_friend_answer(self, chatroom_id, user_id):
        chatroom = Chatroom.query.filter_by(id=chatroom_id)
        user_1, user_2 = map(int, chatroom.name.split("x"))

        if user_id == user_1:
            return self.user_2_answer
        else:
            return self.user_1_answer

    def add_user_answer(self, user_id, chatroom_id, answer):
        chatroom = Chatroom.query.filter_by(id=chatroom_id)
        user_1, user_2 = map(int, chatroom.name.split("x"))

        if user_id == user_1:
            self.user_1_answer = answer
        else:
            self.user_2_answer = answer


chatroom_practiceproblem = database.Table(
    "chatroom_practiceproblem",
    database.Column("chatroom_id", database.Integer, database.ForeignKey("chatroom.id")),
    database.Column("practiceproblem_id", database.Integer, database.ForeignKey("practiceproblem.id"))
)


class Chatroom(database.Model):
    id = database.Column("id", database.Integer, primary_key=True)
    practice_problems = database.relationship("PracticeProblem", secondary=chatroom_practiceproblem)

    # noinspection PyRedeclaration
    practice_problems = database.relationship(
        "PracticeProblem",
        secondary=chatroom_practiceproblem,
        overlaps="chatroom",
    )

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

    def add_practice_problem(self, practice_problem):
        self.practice_problems.append(practice_problem)

    def clear(self):
        self.messages = []

    def get_friend(self, user):
        user_a, user_b = map(int, self.name.split("x"))
        if user_a == user.id:
            return Users.get_user(id=user_b)
        else:
            return Users.get_user(id=user_a)

    @staticmethod
    def get_chatroom(user_1, user_2):
        user_a = min(user_1, user_2)
        user_b = max(user_1, user_2)

        chatroom_name = f"{str(user_a)}x{str(user_b)}"

        return Chatroom.query.filter_by(name=chatroom_name).first()
