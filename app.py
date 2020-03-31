import string
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from marshmallow import validate, Schema, fields, ValidationError
from werkzeug.exceptions import abort


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/flask_items"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


class ItemsModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Item %r>' % (self.name)


class CreateItemInputSchema(Schema):
    ALLOWED = string.ascii_letters + 'ćžšđč'
    name = fields.Str(required=True, validate=[validate.Length(min=3, max=50), validate.ContainsOnly(ALLOWED)])


@app.route('/items', methods=['GET'])
def get_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    items = ItemsModel.query.order_by(ItemsModel.id).paginate(page, per_page).items
    results = [
        {
            "id": item.id,
            "name": item.name
        } for item in items]
    return {"items": results, "message": "Items fetched successfully!"}


create_item_input_schema = CreateItemInputSchema()


@app.route('/items', methods=['POST'])
def add_item():
    req_data = request.get_json()
    item = req_data['name']
    errors = create_item_input_schema.validate(req_data)
    if errors:
        return {"message": "Missing or sending incorrect data to create an item!"}, 400
    else:
        new_item = ItemsModel(name=item)
        db.session.add(new_item)
        db.session.commit()
        return {"message": f"Item {new_item.name} created successfully!"}


@app.route('/items/<id>', methods=['PUT'])
def edit_item(id):
    req_data = request.get_json()
    item_new = req_data['name']
    errors = create_item_input_schema.validate(req_data)
    if errors:
        return {"message": "Missing or sending incorrect data to edit an item!"}, 400
    else:
        item = ItemsModel.query.get(id)
        if item is None:
            abort(404)
        item.name = item_new
        db.session.commit()
        return {"message": "Item updated successfully!"}


@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    item = ItemsModel.query.get(id)
    if item is None:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    return {"message": "Item removed successfully!"}


#app.run(host='0.0.0.0', port='5010', debug=True)
cors = CORS(app)
