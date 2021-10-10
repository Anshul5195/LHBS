from flask import Blueprint, jsonify, request, redirect
from lhbs.models import LHBS
from lhbs import db
import datetime

api = Blueprint('api', __name__)

all_lecture_halls = {1: "Lecture Hall 1", 2: "Lecture Hall 2", 3: "Lecture Hall 3", 4: "Lecture Hall 4",
                     5: "Lecture Hall 5", 6: "Lecture Hall 6", 7: "Lecture Hall 7", 8: "Lecture Hall 8",
                     9: "Lecture Hall 9", 10: "Lecture Hall 10", 11: "Lecture Hall 11", 12: "Lecture Hall 12",
                     13: "Lecture Hall 13", 14: "Lecture Hall 14", 15: "Lecture Hall 15", 16: "Lecture Hall 16"}

# slot for 12 hours hence 12*60*60 seconds
total_time = 43200


@api.route("/dates")
def show_dates_api():
    start_date = datetime.datetime.now().date()
    all_dates = []
    for i in range(1, 31):
        next_date = start_date + datetime.timedelta(days=i)
        all_dates.append(next_date)
    
    dates = []
    for check_date in all_dates:
        check_date_data = LHBS.query.filter_by(date=check_date).all()
        check_date_total_time = 0
        for check_date_time_data in check_date_data:
            check_date_start_time = check_date_time_data.start_time
            check_date_end_time = check_date_time_data.end_time
            check_date_interval_time = int((datetime.datetime.combine(datetime.date.today(), check_date_end_time)
                                            - datetime.datetime.combine(datetime.date.today(), check_date_start_time)).
                                           total_seconds())
            check_date_total_time += check_date_interval_time
        if check_date_total_time == len(all_lecture_halls) * total_time:
            is_available = False
        else:
            is_available = True
        dates.append([str(check_date), check_date.strftime("%A"), is_available])
    dates_api_data = {"dates": dates}
    return jsonify(dates_api_data)


@api.route("/dates/<string:specific_date>")
def show_lecture_halls_api(specific_date):
    specific_date_date_obj = datetime.datetime.strptime(specific_date, "%Y-%m-%d").date()
    lecture_halls = []
    for lecture_hall_key, lecture_hall_value in all_lecture_halls.items():
        lecture_hall_data = LHBS.query.filter_by(date=specific_date_date_obj,
                                                 lecture_hall=lecture_hall_key).all()
        lecture_hall_total_time = 0
        for lecture_hall_time_data in lecture_hall_data:
            lecture_hall_start_time = lecture_hall_time_data.start_time
            lecture_hall_end_time = lecture_hall_time_data.end_time
            lecture_hall_interval_time = int((datetime.datetime.combine(datetime.date.today(), lecture_hall_end_time)
                                              - datetime.datetime.combine(datetime.date.today(),
                                                                          lecture_hall_start_time)).total_seconds())
            lecture_hall_total_time += lecture_hall_interval_time
        if lecture_hall_total_time == total_time:
            is_available = False
        else:
            is_available = True
        lecture_halls.append([lecture_hall_key, lecture_hall_value, is_available])
    lecture_halls_api_data = {"lecture_halls": lecture_halls}
    return jsonify(lecture_halls_api_data)


@api.route("/dates/<string:specific_date>/<int:lecture_hall>")
def show_time_slot_api(specific_date, lecture_hall):
    booked_time_slots = []
    specific_date_date_obj = datetime.datetime.strptime(specific_date, "%Y-%m-%d").date()
    time_slot_data = LHBS.query.filter_by(date=specific_date_date_obj, lecture_hall=lecture_hall).all()
    for check_time_slot_data in time_slot_data:
        time_slot_start_time = check_time_slot_data.start_time
        time_slot_end_time = check_time_slot_data.end_time
        booked_time_slots.append([str(time_slot_start_time), str(time_slot_end_time),
                                 time_slot_start_time.strftime("%I:%M %p"),
                                  time_slot_end_time.strftime("%I:%M %p"), False])
    booked_time_slots.sort(key=lambda x: int(x[0].split(":")[0])*60 + int(x[0].split(":")[1]))
    time_slots = []
    if booked_time_slots:
        first = ["08:00:00", booked_time_slots[0][0], "08:00 AM", booked_time_slots[0][2], True]
        if first[0] == first[1]:
            pass
        else:
            time_slots.append(first)
        for i in range(len(booked_time_slots) - 1):
            time_slots.append(booked_time_slots[i])
            available_slot = [booked_time_slots[i][1], booked_time_slots[i + 1][0], booked_time_slots[i][3],
                              booked_time_slots[i + 1][2], True]
            time_slots.append(available_slot)
        time_slots.append(booked_time_slots[-1])
        last = [booked_time_slots[-1][1], "20:00:00", booked_time_slots[-1][3], "08:00 PM", True]
        if last[0] == last[1]:
            pass
        else:
            time_slots.append(last)
    else:
        time_slots.append(["08:00:00", "20:00:00", "08:00 AM", "08:00 PM", True])
    time_slots.sort(key=lambda x: x[4], reverse=True)
    time_slot_api_data = {"time_slots": time_slots}
    return jsonify(time_slot_api_data)


@api.route("/book-slot", methods=["GET", "POST"])
def book_time_slot_api():
    booked_date = request.form.get("date")
    booked_date_date_obj = datetime.datetime.strptime(booked_date, "%Y-%m-%d").date()
    booked_lecture_hall = request.form.get("lectureHall")
    booked_lecture_hall_int_obj = int(booked_lecture_hall)
    booked_start_time = request.form.get("startTimeValue")
    booked_start_time_time_obj = datetime.datetime.strptime(booked_start_time, "%H:%M:%S").time()
    booked_end_time = request.form.get("endTimeValue")
    booked_end_time_time_obj = datetime.datetime.strptime(booked_end_time, "%H:%M:%S").time()
    if booked_end_time_time_obj > booked_start_time_time_obj:
        check_data = LHBS.query.filter(LHBS.date == booked_date_date_obj,
                                       LHBS.lecture_hall == booked_lecture_hall_int_obj,
                                       LHBS.start_time <= booked_start_time_time_obj,
                                       LHBS.end_time >= booked_end_time_time_obj).count()
        if check_data:
            return redirect("/")
        add_data_row = LHBS(date=booked_date_date_obj,
                            lecture_hall=booked_lecture_hall_int_obj,
                            start_time=booked_start_time_time_obj, end_time=booked_end_time_time_obj)
        db.session.add(add_data_row)
        db.session.commit()
        return redirect('/')
    else:
        return redirect("/")


# @api.route("/justToCheck")
# def just_to_check_api():
#     booked_date = "2021-10-11"
#     booked_date_date_obj = datetime.datetime.strptime(booked_date, "%Y-%m-%d").date()
#     booked_lecture_hall_int_obj = 1
#     booked_start_time = "16:00:00.000000"
#     booked_start_time_time_obj = datetime.datetime.strptime(booked_start_time, "%H:%M:%S.%f").time()
#     print(booked_start_time_time_obj)
#     booked_end_time = "18:00:00.000000"
#     booked_end_time_time_obj = datetime.datetime.strptime(booked_end_time, "%H:%M:%S.%f").time()
#     print(booked_end_time_time_obj)
#     check_data = LHBS.query.filter(LHBS.date == booked_date_date_obj,
#                                    LHBS.lecture_hall == booked_lecture_hall_int_obj,
#                                    LHBS.start_time <= booked_start_time_time_obj,
#                                    LHBS.end_time >= booked_end_time_time_obj).count()
#     check_data_date = check_data.date
#     return jsonify(check_data_date)
