from flask import Blueprint, jsonify, request, redirect
from lhbs.models import LHBS
from lhbs import db
from datetime import date, timedelta

api = Blueprint('api', __name__)

all_lecture_halls = {1: "Lecture Hall 1", 2: "Lecture Hall 2", 3: "Lecture Hall 3", 4: "Lecture Hall 4",
                     5: "Lecture Hall 5", 6: "Lecture Hall 6", 7: "Lecture Hall 7", 8: "Lecture Hall 8",
                     9: "Lecture Hall 9", 10: "Lecture Hall 10", 11: "Lecture Hall 11", 12: "Lecture Hall 12",
                     13: "Lecture Hall 13", 14: "Lecture Hall 14", 15: "Lecture Hall 15", 16: "Lecture Hall 16"}

all_time_slots = {1: "8:00 am - 9:00 am", 2: "9:00 am - 10:00 am", 3: "10:00 am - 11:00 am", 4: "11:00 am - 12:00 pm",
                  5: "12:00 pm - 1:00 pm", 6: "1:00 pm - 2:00 pm", 7: "2:00 pm - 3:00 pm", 8: "3:00 pm - 4:00 pm",
                  9: "4:00 pm - 5:00 pm", 10: "5:00 pm - 6:00 pm", 11: "6:00 pm - 7:00 pm", 12: "7:00 pm - 8:00 pm"}


@api.route("/dates")
def show_dates_api():
    start_date = date.today()
    all_dates = []
    for i in range(1, 31):
        next_date = str(start_date + timedelta(days=i))
        all_dates.append(next_date)
    
    dates = []
    for check_date in all_dates:
        check_date_data = LHBS.query.filter_by(booked_date=check_date).count()
        if check_date_data == len(all_lecture_halls) * len(all_time_slots):
            is_available = False
        else:
            is_available = True
        dates.append([check_date, is_available])
    dates_api_data = {"dates": dates}
    return jsonify(dates_api_data)


@api.route("/dates/<string:specific_date>")
def show_lecture_halls_api(specific_date):
    lecture_halls = []
    for lecture_hall_key, lecture_hall_value in all_lecture_halls.items():
        lecture_hall_data = LHBS.query.filter_by(booked_date=specific_date,
                                                 booked_lecture_hall=lecture_hall_key).count()
        if lecture_hall_data == len(all_time_slots):
            is_available = False
        else:
            is_available = True
        lecture_halls.append([lecture_hall_key, lecture_hall_value, is_available])
    lecture_halls_api_data = {"lecture_halls": lecture_halls}
    return jsonify(lecture_halls_api_data)


@api.route("/dates/<string:specific_date>/<int:lecture_hall>")
def show_time_slot_api(specific_date, lecture_hall):
    time_slots = []
    for time_slot_key, time_slot_value in all_time_slots.items():
        time_slot_data = LHBS.query.filter_by(booked_date=specific_date, booked_lecture_hall=lecture_hall,
                                              booked_time_slot=time_slot_key).count()
        if time_slot_data:
            is_available = False
        else:
            is_available = True
        time_slots.append([time_slot_key, time_slot_value, is_available])
    time_slot_api_data = {"time_slots": time_slots}
    return jsonify(time_slot_api_data)


@api.route("/book-slot", methods=["GET", "POST"])
def book_time_slot_api():
    booked_date = request.form.get("booked-date")
    booked_lecture_hall = request.form.get("booked-lecture-hall")
    booked_time_slot = request.form.get("booked-time-slot")
    check_data = LHBS.query.filter_by(booked_date=booked_date,
                                      booked_lecture_hall=booked_lecture_hall,
                                      booked_time_slot=booked_time_slot).count()
    if check_data:
        return redirect("/")
    add_data_row = LHBS(booked_date=booked_date, booked_lecture_hall=booked_lecture_hall,
                        booked_time_slot=booked_time_slot)
    db.session.add(add_data_row)
    db.session.commit()
    return redirect('/')
