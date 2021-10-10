$.get('/dates', function(data) {
    var options = '<option disabled selected>Dates</option>';
    for (var i in data["dates"]) {
        if (data["dates"][i][2]) {
            options += `<option value="${data["dates"][i][0]}">${data["dates"][i][1] + " " + data["dates"][i][0]}</option>`
        }
        else {
            options += `<option disabled>${data["dates"][i][1] + " " + data["dates"][i][0]}</option>`
        }
    }
    document.getElementById("bookedDate").innerHTML = options
});

function changeDateFunc() {
    document.getElementById("bookedTimeSlot").innerHTML = '<option disabled selected>Time Slots</option>';
    document.getElementById("startTime").setAttribute("disabled", true);
    document.getElementById("endTime").setAttribute("disabled", true);
    document.getElementById("bookSlot").setAttribute("disabled", true);
    var selectDateBox = document.getElementById("bookedDate");
    var selectedDate = selectDateBox.options[selectDateBox.selectedIndex].value;
    document.getElementById("bookedDate").setAttribute("value", selectedDate);
    $.get('/dates/' + selectedDate, function(data){
        var options = '<option disabled selected>Lecture Halls</option>';
        for (var i in data["lecture_halls"]) {
            if (data["lecture_halls"][i][2]) {
                options += `<option value="${data["lecture_halls"][i][0]}">${data["lecture_halls"][i][1]}</option>`
            }
            else {
                options += `<option disabled>${data["lecture_halls"][i][1]}</option>`

            }
        }
        document.getElementById("bookedLectureHall").innerHTML = options;
    });
};

function changeLectureHallFunc() {
    document.getElementById("startTime").setAttribute("disabled", true);
    document.getElementById("endTime").setAttribute("disabled", true);
    document.getElementById("bookSlot").setAttribute("disabled", true);
    var selectLectureHallBox = document.getElementById("bookedLectureHall");
    var selectedLectureHall = selectLectureHallBox.options[selectLectureHallBox.selectedIndex].value;
    var selectedDate = document.getElementById("bookedDate").value;
    document.getElementById("bookedLectureHall").setAttribute("value", selectedLectureHall);
    $.get('/dates/' + selectedDate + '/' + selectedLectureHall, function(data){
        var options = '<option disabled selected>Time Slots</option>';
        for (var i in data["time_slots"]) {
            if (data["time_slots"][i][4]) {
                options += `<option value="${data["time_slots"][i][0] + "-" +
                data["time_slots"][i][1]}">${data["time_slots"][i][2] + " - " + data["time_slots"][i][3]}</option>`
            }
            else {
                options += `<option disabled>${data["time_slots"][i][2] + " - " + data["time_slots"][i][3]}</option>`

            }
        }
        document.getElementById("bookedTimeSlot").innerHTML = options;
    });
};

function changeTimeSlotFunc() {
    var startTimeSpanElement = document.getElementById("startTimeValue");
    startTimeSpanElement.innerHTML = '';
    document.getElementById("endTime").setAttribute("disabled", true);
    document.getElementById("bookSlot").setAttribute("disabled", true);
    var selectTimeSlotBox = document.getElementById("bookedTimeSlot");
    var selectedTimeSlot = selectTimeSlotBox.options[selectTimeSlotBox.selectedIndex].value;
    document.getElementById("bookedTimeSlot").setAttribute("value", selectedTimeSlot);

    var selectedTimeSlotSplit = selectedTimeSlot.split("-");
    var startTimeSplit = selectedTimeSlotSplit[0].split(":");
    var endTimeSplit = selectedTimeSlotSplit[1].split(":");

    var minTime = (Number(startTimeSplit[0]) - 8)*60 + Number(startTimeSplit[1]);

    var timeSpan = (Number(endTimeSplit[0]) - Number(startTimeSplit[0]))*60 + (Number(endTimeSplit[1])
                                                                                   - Number(startTimeSplit[1]));
    var maxTime = minTime + timeSpan;
    document.getElementById("startTime").setAttribute("min", minTime);
    document.getElementById("startTime").setAttribute("max", maxTime);
    document.getElementById("startTime").setAttribute("value", minTime);
    document.getElementById("endTime").setAttribute("min", minTime);
    document.getElementById("endTime").setAttribute("max", maxTime);
    document.getElementById("endTime").setAttribute("value", maxTime);
    document.getElementById("startTime").removeAttribute("disabled");
};

function changeStartTimeInputFunc() {
    var endTimeSpanElement = document.getElementById("endTimeValue");
    endTimeSpanElement.innerHTML = '';
    document.getElementById("bookSlot").setAttribute("disabled", true);
    var hourMap = {8: "08", 9: "09", 10: "10", 11: "11", 12: "12", 13: "01", 14: "02", 15: "03", 16: "04",
                    17: "05", 18: "06", 19: "07", 20: "08"};
    var minuteMap = {0: "00", 1: "01", 2: "02", 3: "03", 4: "04", 5: "05", 6: "06", 7: "07", 8: "08", 9: "09"};
    var timeMap = {8: "08", 9: "09"};
    var startTimeElement = document.getElementById("startTime");
    var startTimeSpanElement = document.getElementById("startTimeValue");
    startTimeSpanElement.innerHTML = startTimeElement.value;
    startTimeElement.addEventListener('input', function () {
        var timeHour = Math.floor(startTimeElement.value/60) + 8;
        var timeMinute = startTimeElement.value % 60;
        if (timeMinute < 10) {
            timeMinute = minuteMap[timeMinute];
        }
        else {
            timeMinute = timeMinute.toString();
        }
        if (timeHour < 12) {
            addSpanElement = hourMap[timeHour] + ":" + timeMinute + " AM";
        }
        else {
            addSpanElement = hourMap[timeHour] + ":" + timeMinute + " PM";
        }
        if (timeHour < 10) {
            var databaseTimeHour = timeMap[timeHour];
        }
        else {
            var databaseTimeHour = timeHour.toString();
        }
        var databaseStartTime = databaseTimeHour + ":" + timeMinute + ":00"
        document.getElementById("startTimeOutputValue").setAttribute("value", databaseStartTime);
        var startTimeElementValue = document.getElementById("startTime").value;
        document.getElementById("startTime").setAttribute("value", startTimeElementValue);
        startTimeSpanElement.innerHTML = addSpanElement;
    }, false);

    document.getElementById("endTime").removeAttribute("disabled");
};

function changeEndTimeInputFunc() {
    var hourMap = {8: "08", 9: "09", 10: "10", 11: "11", 12: "12", 13: "01", 14: "02", 15: "03", 16: "04",
                    17: "05", 18: "06", 19: "07", 20: "08"};
    var minuteMap = {0: "00", 1: "01", 2: "02", 3: "03", 4: "04", 5: "05", 6: "06", 7: "07", 8: "08", 9: "09"}
    var timeMap = {8: "08", 9: "09"};
    var endTimeElement = document.getElementById("endTime");
    var endTimeSpanElement = document.getElementById("endTimeValue");
    endTimeSpanElement.innerHTML = endTimeElement.value;
    endTimeElement.addEventListener('input', function () {
        var timeHour = Math.floor(endTimeElement.value/60) + 8;
        var timeMinute = endTimeElement.value % 60;
        if (timeMinute < 10) {
            timeMinute = minuteMap[timeMinute]
        }
        else {
            timeMinute = timeMinute.toString()
        }

        if (timeHour < 12){
            addSpanElement = hourMap[timeHour] + ":" + timeMinute + " AM"
        }
        else {
            addSpanElement = hourMap[timeHour] + ":" + timeMinute + " PM"
        }
        if (timeHour < 10) {
            var databaseTimeHour = timeMap[timeHour];
        }
        else {
            var databaseTimeHour = timeHour.toString();
        }
        var databaseEndTime = databaseTimeHour + ":" + timeMinute + ":00"
        document.getElementById("endTimeOutputValue").setAttribute("value", databaseEndTime);
        var endTimeElementValue = document.getElementById("endTime").value;
        document.getElementById("endTime").setAttribute("value", endTimeElementValue);
        endTimeSpanElement.innerHTML = addSpanElement;
    }, false);
    if (Number(document.getElementById("endTime").value) > Number(document.getElementById("startTime").value)) {
        document.getElementById("bookSlot").removeAttribute("disabled");
    }
    else {
        document.getElementById("bookSlot").setAttribute("disabled", true);
    }
};