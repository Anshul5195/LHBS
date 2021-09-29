from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('home.html', title='Home')


@app.route("/lecture_hall/<int:number>")
def lecture_hall(number):
    return render_template('lecture_hall.html', title=f'Lecture Hall {number}', number=number)


if __name__ == '__main__':
    app.run(debug=True)