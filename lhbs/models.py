from lhbs import db


class LHBS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    lecture_hall = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    def __repr__(self):
        return f"({self.id}, '{self.date}', {self.lecture_hall}, '{self.start_time}', '{self.end_time}')"