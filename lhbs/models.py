from lhbs import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    booking = db.relationship('Booking', backref='customer', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    lecture_hall = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    purpose = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Booking('{self.lecture_hall}', '{self.date}')"
    

# class Test(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     hall = db.Column(db.Integer)
#
#     def __repr__(self):
#         return f"Test('{self.hall}')"
