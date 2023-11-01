from flask import Flask
import config
from exts import db
from models import Stockdata
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():  # put application's code here
    stockdata = Stockdata(id=666666, stockname='大自在', markettag='hu', datajson={'key': 'value'})
    db.session.add(stockdata)
    db.session.commit()
    return 'Hello Wo'


@app.route('/refresh/')
def refresh():
    return 'refresh finished!'


if __name__ == '__main__':
    app.run()
