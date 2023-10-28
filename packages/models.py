import sqlalchemy.orm.attributes

from packages.imports import *

user_chatroom_association = database.Table('user_chatroom_association',
                                           database.Column('user_id', database.Integer,
                                                           database.ForeignKey('users.id')),
                                           database.Column('chatroom_id', database.Integer,
                                                           database.ForeignKey('chatroom.id')),

                                           )


class Users(database.Model):
    id = database.Column("id", database.Integer, primary_key=True)
    name = database.Column(database.String(100))
    email = database.Column(database.String(100))
    password = database.Column(database.String(100))

    courses = database.Column(database.JSON)
    chatrooms = database.relationship('Chatroom', secondary=user_chatroom_association, back_populates='users')
    chatroom_ordering = database.Column(database.JSON)

    def __init__(self, name, email, password, courses):
        self.name = name
        self.email = email
        self.password = password
        self.courses = courses

    def add_chatroom(self, chatroom):
        if not self.chatroom_ordering:
            self.chatroom_ordering = []

        if chatroom in self.chatrooms and chatroom.name in self.chatroom_ordering:
            chatroom_index = self.chatroom_ordering.index(chatroom.name)
            self.chatroom_ordering.pop(chatroom_index)
            # new_chatroom_order = []
            # for chatroom_name in self.chatroom_ordering:
            #     if chatroom_name != chatroom.name:
            #         new_chatroom_order.append(chatroom_name)
            # self.chatroom_ordering = new_chatroom_order

        self.chatrooms.insert(0, chatroom)
        self.chatroom_ordering.insert(0, chatroom.name)
        sqlalchemy.orm.attributes.flag_modified(self, "chatroom_ordering")
        database.session.commit()

    def get_chatrooms(self):
        chatrooms_list = []
        for chatroom_name in self.chatroom_ordering:
            chatrooms_list.append(Chatroom.query.filter_by(name=chatroom_name).first())
        return chatrooms_list

    def get_friends(self):
        friends = []
        for chatroom in self.chatrooms:
            friends.append(chatroom.get_friend(self))

        return friends

    def add_friend(self, friend, commonality):
        chatroom = Chatroom(self.id, friend.id, commonality)
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

    user_1_answer = database.Column(database.String(100))
    user_2_answer = database.Column(database.String(100))

    user_1_status = database.Column(database.String(100), default="open")
    user_2_status = database.Column(database.String(100), default="open")

    def __init__(self, course, question):
        self.course = course
        self.question = question

    def get_user_answer(self, user, chatroom):
        user_id = user.id
        chatroom_id = chatroom.id
        chatroom = Chatroom.query.filter_by(id=chatroom_id).first()
        user_1, user_2 = map(int, chatroom.name.split("x"))

        if user_id == user_1:
            return self.user_1_answer
        else:
            return self.user_2_answer

    def get_status(self, user, chatroom):
        user_id = user.id
        chatroom_id = chatroom.id
        chatroom = Chatroom.query.filter_by(id=chatroom_id).first()
        user_1, user_2 = map(int, chatroom.name.split("x"))

        if user_id == user_1:
            return self.user_1_status
        else:
            return self.user_2_status

    def get_friend_answer(self, chatroom, user):
        chatroom_id = chatroom.id
        user_id = user.id
        chatroom = Chatroom.query.filter_by(id=chatroom_id).first()
        user_1, user_2 = map(int, chatroom.name.split("x"))

        if user_id == user_1:
            return self.user_2_answer
        else:
            return self.user_1_answer

    def add_user_answer(self, user, chatroom, answer):
        user_id = user.id
        chatroom_id = chatroom.id
        chatroom = Chatroom.query.filter_by(id=chatroom_id).first()
        user_1, user_2 = map(int, chatroom.name.split("x"))

        if user_id == user_1:
            self.user_1_status = "grading"
            self.user_1_answer = answer
        else:
            self.user_2_status = "grading"
            self.user_2_answer = answer

    def grade_user_answer(self, user, status, chatroom):
        user_id = user.id
        user_1, user_2 = map(int, chatroom.name.split("x"))

        if user_id == user_1:
            if status == "1":
                self.user_1_status = "correct"
            else:
                self.user_1_status = "incorrect"
        else:
            if status == "1":
                self.user_2_status = "correct"
            else:
                self.user_2_status = "incorrect"
        database.session.commit()

    @staticmethod
    def get_practice_problem(practice_problem_id):
        return PracticeProblem.query.filter_by(id=practice_problem_id).first()


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
    commonality = database.Column(database.String(100))
    messages = database.relationship("Message", back_populates="chatroom")
    users = database.relationship('Users', secondary=user_chatroom_association, back_populates='chatrooms')

    user_1_open = database.Column(database.Boolean, default=False)
    user_2_open = database.Column(database.Boolean, default=False)

    def __init__(self, user_1, user_2, commonality):
        user_a = min(user_1, user_2)
        user_b = max(user_1, user_2)
        self.name = f"{str(user_a)}x{str(user_b)}"
        self.commonality = commonality
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def add_practice_problem(self, practice_problem):
        self.practice_problems.insert(0, practice_problem)

    def clear(self):
        self.messages = []

    def get_friend(self, user):
        user_a, user_b = map(int, self.name.split("x"))
        if user_a == user.id:
            return Users.get_user(id=user_b)
        else:
            return Users.get_user(id=user_a)

    def get_message_status(self, user):
        user_a, user_b = map(int, self.name.split("x"))
        if user_a != user.id:
            if self.user_1_open:
                return True
            else:
                return False
        elif user_b != user.id:
            if self.user_2_open:
                return True
            else:
                return False

    def set_message_status(self, user):
        user_a, user_b = map(int, self.name.split("x"))
        if user.id == user_a:
            self.user_2_open = True
        else:
            self.user_1_open = True

    @staticmethod
    def get_chatroom(user_1, user_2):
        user_a = min(user_1, user_2)
        user_b = max(user_1, user_2)

        chatroom_name = f"{str(user_a)}x{str(user_b)}"

        return Chatroom.query.filter_by(name=chatroom_name).first()
