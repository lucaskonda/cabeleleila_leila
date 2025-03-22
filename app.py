from flask import Flask
from database import db
from routes import app_routes  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agendamentos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave-secreta'

db.init_app(app)

app.register_blueprint(app_routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

