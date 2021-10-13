from lhbs import create_app, db
from lhbs.config import Config
from lhbs.models import Test #particular table

app = create_app()

with app.app_context():
    engine = create_engine('sqlite:///lhbs.db')
    meta.bind = engine
    Test.__table__.create(engine) #particular table

