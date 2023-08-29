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
    # user = Users.query.all()[0]
    # user.chatrooms[0].messages = []
    # database.session.commit()
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
    return flask.render_template("dashboard.html", user=user)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # if user makes new account
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        courses = flask.request.form.getlist("course")

        if len(password) < 8:
            return flask.render_template("signup.html",
                                         error="Please input a valid email and password with 8 characters of more.")
        elif len(courses) == 0:  # checks if user has not selected a course
            return flask.render_template("signup.html", error="Please choose a course")

        if Users.get_user(email=email):  # if account already exists
            return flask.render_template("signup.html", error="Email in use!")
        else:
            # creates new user
            user = Users(email, password, courses)
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
    sender = Users.get_user(email=sender_email)
    sender_id = sender.id
    receiver_id = data['receiver']
    room = Chatroom.get_chatroom(sender_id, receiver_id)
    flask_socketio.join_room(room.name)


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

    # Add message to database
    message = Message(sender.id, data["message"], chatroom=room)
    database.session.add(message)
    room.messages.append(message)
    database.session.add(room)
    database.session.commit()


if __name__ == '__main__':
    socketio.run(app, debug=True)
    app.run()
