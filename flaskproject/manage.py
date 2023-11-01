from flask_script import Manager
from flask_script import Command
from app import app
from exts import db
from flask_migrate import Migrate

manager = Manager(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    manager.run()
