from lhbs import create_app, db
from lhbs.models import Test #particular table

app = create_app()

with app.app_context():
    Test.drop()  # particular table
