from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/flask_items"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ItemsModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Item {self.name}>"

@app.route('/items', methods=['GET'])
def get_items():
   
    items = ItemsModel.query.all()
    results = [
        {
            "name": item.name
        } for item in items]

    return {"items": results}