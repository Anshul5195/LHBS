from lhbs import db


class LHBS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booked_date = db.Column(db.String(32))
    booked_lecture_hall = db.Column(db.Integer)
    booked_time_slot = db.Column(db.Integer)

    def __repr__(self):
        return f"({self.id}, '{self.booked_date}', {self.booked_lecture_hall}, {self.booked_time_slot})"