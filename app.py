from packages.models import *
from packages.backend import *

app = flask.Flask(__name__)
app.secret_key = "shlok"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
socketio = SocketIO(app)
database.init_app(app)

with app.app_context():
    database.create_all()
    pass


@app.route("/")
def main():
    # user = Users.query.all()[0]
    # user.chatrooms[0].messages = []
    # database.session.commit()
    email = flask.session.get("email")
    if email:
        # return website with user data
        user = Users.query.filter_by(email=email).first()
        return flask.render_template("dashboard.html", user=user)
    # else return launch page
    return flask.render_template("launch.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # if user makes new account
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        courses = flask.request.form.getlist("course")

        if len(password) < 8:  # checks if password is less than 8 characters
            return flask.render_template("signup.html",
                                         error="Please input a valid email and password with 8 characters of more.")
        elif len(courses) == 0:  # checks if user has not selected a course
            return flask.render_template("signup.html", error="Please choose a course")

        if Users.query.filter_by(email=email).first():  # if this email is already in use
            return flask.render_template("signup.html", error="Email in use!")
        else:
            # Creating new user
            user = Users(email, password, courses)
            database.session.add(user)
            database.session.commit()
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

        user = Users.query.filter_by(email=email).first()
        if not user:  # check if users exists
            return flask.render_template("login.html", error="invalid credentials")
        elif user.password != password:  # check if password is incorrect
            return flask.render_template("login.html", error="invalid credentials")
        else:
            # takes to main page
            flask.session["email"] = email
            flask.session.permanent = True
            return flask.redirect("/")
    # if user simply visits page
    return flask.render_template("login.html")


# CHAT ROUTES
@socketio.on('join')
def handle_join(data):
    sender = Users.query.filter_by(email=flask.session.get("email")).first()
    sender_id = sender.id
    receiver_id = data['receiver']
    room = Chatroom.get_name(sender_id, receiver_id)
    print(room)
    flask_socketio.join_room(room)


@socketio.on('send_message')
def handle_send_message(data):
    # Update screens
    sender_email = flask.session.get("email")
    sender = Users.query.filter_by(email=sender_email).first()
    sender_id = sender.id
    receiver_id = data["user_id"]

    room_name = Chatroom.get_name(sender_id, receiver_id)

    message_object = {"message": data["message"], "sender": sender.id}
    print(room_name)
    flask_socketio.send(message_object, room=room_name)

    # Add message to database

    chatroom = Chatroom.query.filter_by(name=Chatroom.get_name(1, 2)).first()
    message = Message(sender.id, data["message"], chatroom=chatroom)
    database.session.add(message)
    chatroom.messages.append(message)
    database.session.add(chatroom)
    database.session.commit()


if __name__ == '__main__':
    socketio.run(app, debug=True)
    app.run()
