from flask import render_template, Blueprint
from flask_login import current_user, login_required
from lhbs import db
from lhbs.models import Booking
import datetime



view = Blueprint('view', __name__)


@view.route("/")
def home_page():
    return render_template('index.html')


@login_required
@view.route("/user-booking")
def user_booking():
    current_date_time = datetime.datetime.now()
    all_bookings = Booking.query.filter(Booking.user_id == current_user.id).all()
    past_bookings = []
    future_bookings = []
    for booking in all_bookings:
        booking_date = booking.date
        booking_end_time = booking.end_time
        booking_date_time = datetime.datetime.combine(booking_date, booking_end_time)
        if booking_date_time > current_date_time:
            future_bookings.append(booking)
        else:
            past_bookings.append(booking)
    return render_template('user_booking.html', past_bookings=past_bookings, future_bookings=future_bookings)