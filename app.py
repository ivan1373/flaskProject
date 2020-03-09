from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/flask_items"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
            "id": item.id,
            "name": item.name
        } for item in items]

    return {"items": results, "message": "Item je uspješno dohvaćen"}


@app.route('/items', methods=['POST'])
def add_item():
    req_data = request.get_json()
    item = req_data['name']
    new_item = ItemsModel(name=item)
    db.session.add(new_item)
    db.session.commit()
    return {"message": f"item {new_item.name} je uspješno stvoren"}


@app.route('/items/<id>', methods=['PUT'])
def edit_item(id):
    req_data = request.get_json()
    item_new = req_data['newname']
    item = ItemsModel.query.get(id)
    item.name = item_new
    db.session.commit()
    return {"message": "Item je uspješno izmijenjen"}


@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    item = ItemsModel.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return {"message": "Item je uspješno izbrisan"}
