from flask import render_template, Blueprint

view = Blueprint('view', __name__)


@view.route("/")
def home_page():
    return render_template('index.html')