from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import DevApplication
from db import db
from resources.routes import routes

app = Flask(__name__)  # инициализираме фласк апликацията
app.config.from_object(DevApplication)  # конфигурираме фласк апликацията
db.init_app(
    app
)  # инициализираме database обекта с апликацията която вече е конфигурирана


migrate = Migrate(app, db)
api = Api(app)

[api.add_resource(*r) for r in routes]  # *r = (Register, "/register") и тн.

if __name__ == "__main__":
    app.run()
