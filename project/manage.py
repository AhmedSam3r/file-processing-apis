from project.settings import APP_SETTINGS
from flask_migrate import Migrate
from project import app, db

app.config.from_object(APP_SETTINGS)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
