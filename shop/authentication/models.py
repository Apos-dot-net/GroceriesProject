from datetime import datetime

from flask_login import user_logged_in, user_logged_out
from sqlalchemy.dialects.mysql import INTEGER

from shop import db, app
from shop.admin import User


# Define the LoginTracker model
class LoginTracker(db.Model):
    __tablename__ = 'login_tracker'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    user_id = db.Column(INTEGER(unsigned=True), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Add any other fields you want to track, such as IP address, user agent, etc.

    def __init__(self, user_id, user_type):
        self.user_id = user_id
        self.user_type = user_type

    def __repr__(self):
        return '<LoginTracker %r>' % self.id


# Define the LogoutTracker model
class LogoutTracker(db.Model):
    __tablename__ = 'logout_tracker'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    user_id = db.Column(INTEGER(unsigned=True), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    logout_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    # Add any other fields you want to track, such as IP address, user agent, etc.

    def __init__(self, user_id, user_type):
        self.user_id = user_id
        self.user_type = user_type

    def __repr__(self):
        return '<LogoutTracker %r>' % self.id


# Function to track user logins
def track_login(sender, user, **extra):
    # Check if the user is from the User model or RegisterModel
    user_type = 'admin' if isinstance(user, User) else 'user'

    # Create a new LoginTracker entry
    login_tracker = LoginTracker(user_id=user.id, user_type=user_type)
    db.session.add(login_tracker)
    db.session.commit()


# Function to track user logouts
def track_logout(sender, user, **extra):
    # Check if the user is from the User model or RegisterModel
    user_type = 'admin' if isinstance(user, User) else 'user'

    # Create a new LogoutTracker entry
    logout_tracker = LogoutTracker(user_id=user.id, user_type=user_type)
    db.session.add(logout_tracker)
    db.session.commit()


# Connect the track_login function to the user_logged_in signal
user_logged_in.connect(track_login)

# Connect the track_logout function to the user_logged_out signal
user_logged_out.connect(track_logout)

with app.app_context():
    db.create_all()
