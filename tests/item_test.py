import unittest
import requests
import json
import sys
sys.path.append('../')
from app import app, db, ItemsModel


class TestItems(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/test_items'
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass


    def test_get_items(self):
        response = requests.get("http://localhost:5000/items")
        assert response.status_code == 200

    def test_add_item(self):
        response = requests.post("http://localhost:5000/items", json={'name': 'test'})
        assert response.status_code == 200

    def test_add_item_wrong(self):
        response = requests.post("http://localhost:5000/items", json={'name': '/'})
        assert response.status_code != 200

    def test_delete_item(self):
        response = requests.delete('http://localhost:5000/items/11')
        assert response.status_code == 200
    
    def test_delete_item_missing(self):
        response = requests.delete('http://localhost:5000/items/1')
        assert response.status_code != 200

    def test_update_item(self):
        response = requests.put("http://localhost:5000/items/1", json={'name': '123'})
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
