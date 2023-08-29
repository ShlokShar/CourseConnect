from packages.imports import *


# redirects user to launch page if they aren't logged in
def logged_in(f):
    @wraps(f)
    def validator(*args, **kwargs):
        if flask.session.get("email"):
            return f(*args, **kwargs)
        else:
            return flask.redirect("/")

    return validator
