from packages.models import *
from packages.backend import *

app = flask.Flask(__name__)
app.secret_key = "shlok"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
socketio = SocketIO(app)
database.init_app(app)

with app.app_context():
    # create database
    database.create_all()
    pass


@app.route("/")
def main():
    email = flask.session.get("email")
    if email:
        return flask.redirect("/chats")
    # else return launch page
    return flask.render_template("launch.html")


@app.route("/chats")
@logged_in
def chats():
    # return website with user data
    email = flask.session.get("email")
    user = Users.get_user(email=email)
    if len(user.chatrooms) > 0:
        return flask.render_template("dashboard.html", user=user)
    else:
        return flask.redirect("/add-friends")


@logged_in
@app.route("/practice-problems")
def practice_problems():
    email = flask.session.get("email")
    user = Users.get_user(email=email)
    return flask.render_template("practice_problems.html", user=user)


@app.route("/add-friends", methods=["GET", "POST"])
@logged_in
def add_friends():
    email = flask.session.get("email")
    if flask.request.method == "POST":
        user = Users.get_user(email=email)
        # See which users are not already friends with the user
        all_users = Users.query.filter(Users.courses.contains("AP Calculus")).all()

        current_friends = user.get_friends()
        if current_friends:
            current_friends.append(user)
        else:
            current_friends = [user]
        available_friends = [user for user in all_users if user not in current_friends]
        # select random user to be their friend :)
        friend = random.choice(available_friends)
        user.add_friend(friend, commonality="AP Calculus")
        database.session.commit()

        return flask.redirect("/chats")
    return flask.render_template("add_friends.html")


@app.route("/add-practice-problem")
def add_practice_problem():
    email = flask.session.get("email")
    user = Users.get_user(email=email)

    return flask.render_template("add_practice_problem.html", user=user)


@app.route("/create-practice-problem/<category>/<friend_id>")
def create_practice_problem(category, friend_id):
    email = flask.session.get("email")
    user = Users.get_user(email=email)
    friend = Users.get_user(id=friend_id)
    practice_problem_question = generate_question(category)
    practice_problem = PracticeProblem(course=category, question=practice_problem_question)

    chatroom = Chatroom.get_chatroom(user_1=user.id, user_2=friend.id)
    chatroom.add_practice_problem(practice_problem)
    # move the chatroom to the top of the user's list (as it has just been updated)
    chatroom_index = user.chatrooms.index(chatroom)

    user.chatrooms.pop(chatroom_index)
    user.chatrooms.insert(0, chatroom)

    # move the chatroom to the top of the friend's list
    chatroom_index = friend.chatrooms.index(chatroom)
    friend.chatrooms.pop(chatroom_index)
    friend.chatrooms.insert(0, chatroom)

    database.session.commit()

    return flask.jsonify("yay")


@app.route("/submit-practice-problem/<practice_problem_id>/<chatroom_id>/<answer>/")
def submit_practice_problem(practice_problem_id, chatroom_id, answer):
    email = flask.session.get("email")
    user = Users.get_user(email=email)

    practice_problem = PracticeProblem.get_practice_problem(practice_problem_id)
    practice_problem.add_user_answer(user.id, chatroom_id, answer)

    database.session.commit()

    return flask.jsonify("done.")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # if user makes new account
    if flask.request.method == "POST":
        # get sign-in information
        name = flask.request.form["name"]
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        courses = flask.request.form.getlist("course")
        if len(password) < 8:
            return flask.render_template("signup.html",
                                         error="Please choose a password with 8+ characters")
        elif len(courses) == 0:  # checks if user has not selected a course
            return flask.render_template("signup.html", error="Please choose a course")
        elif not name:
            return flask.render_template("signup.html", error="Please include your name")

        if Users.get_user(email=email):  # if account already exists
            return flask.render_template("signup.html", error="Email in use!")
        else:
            # creates new user
            user = Users(name, email, password, courses)
            database.session.add(user)
            database.session.commit()

            # save login
            flask.session["email"] = email
            flask.session.permanent = True

            return flask.redirect("/")
    # if user simply visits page
    return flask.render_template("signup.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    # if user attempts to log in
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]

        user = Users.get_user(email=email)
        if not user:  # check if users exists
            return flask.render_template("login.html", error="invalid credentials")
        elif user.password != password:  # check if password is incorrect
            return flask.render_template("login.html", error="invalid credentials")
        else:
            # saves login
            flask.session["email"] = email
            flask.session.permanent = True

            return flask.redirect("/")
    # if user simply visits page
    return flask.render_template("login.html")


# CHAT ROUTES
@socketio.on('join')
def handle_join(data):
    # joins chat room
    sender_email = flask.session.get("email")
    if sender_email:
        sender = Users.get_user(email=sender_email)
        sender_id = sender.id
        receiver_id = data['receiver']
        room = Chatroom.get_chatroom(sender_id, receiver_id)
        flask_socketio.join_room(room.name)


@socketio.on('change')
def change_chatroom(data):
    sender_email = flask.session.get("email")
    if sender_email:
        sender = Users.get_user(email=sender_email)
        sender_id = sender.id

        print("sender: " + sender.name)
        print("receiver: " + Users.get_user(id=data["receiver"]).name)
        # old_chatroom = Chatroom.get_chatroom(sender_id, receiver_id)
        # flask_socketio.leave_room(old_chatroom.name)

        new_chatroom = Chatroom.get_chatroom(sender_id, data["receiver"])
        flask_socketio.join_room(new_chatroom.name)

        print("joined " + new_chatroom.name)


@socketio.on('send_message')
def handle_send_message(data):
    # get sender, receiver, and chatroom information
    sender_email = flask.session.get("email")
    sender = Users.get_user(email=sender_email)  # get sender from their email
    sender_id = sender.id

    receiver_id = data["user_id"]
    room = Chatroom.get_chatroom(sender_id, receiver_id)

    # show messages to user
    message_object = {"message": data["message"], "sender": sender.id}
    flask_socketio.send(message_object, room=room.name)

    # add message to database
    message = Message(sender.id, data["message"], chatroom=room)
    database.session.add(message)
    room.messages.append(message)
    database.session.add(room)
    database.session.commit()


if __name__ == '__main__':
    socketio.run(app, debug=True)
    app.run()
