from flask import Flask
from controllers import routes
from models.database import db
from models.favorite_champion import FavoriteChampion
import os

app = Flask(__name__, template_folder='views')

# Configuração do banco de dados SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa o banco de dados
db.init_app(app)

with app.app_context():
    db.create_all()

routes.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
