import os
os.environ['DATABASE_URL'] = "postgresql:///cupcakes_test"

from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

with app.app_context():
    db.drop_all()
    db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""
        with app.app_context():
            db.drop_all()
            db.create_all()

            cupcake = Cupcake(**CUPCAKE_DATA)
            db.session.add(cupcake)
            db.session.commit()

            self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()
            db.drop_all()

    def test_list_cupcakes(self):
        """Test listing all cupcakes"""
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(len(data["cupcakes"]), 1)

            cupcake = data["cupcakes"][0]
            self.assertEqual(cupcake["id"], self.cupcake_id)

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })
    def test_get_cupcake_not_found(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes/9999")
            self.assertEqual(resp.status_code, 404)


    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        with app.test_client() as client:
            data = {
                "flavor": "UpdatedFlavor",
                "size": "UpdatedSize",
                "rating": 9,
                "image": "http://test.com/updated.jpg"
            }

            resp = client.patch(f"/api/cupcakes/{self.cupcake_id}", json=data)
            self.assertEqual(resp.status_code, 200)

            json = resp.get_json()
            self.assertEqual(json['cupcake']['flavor'], "UpdatedFlavor")
            self.assertEqual(json['cupcake']['size'], "UpdatedSize")
            self.assertEqual(json['cupcake']['rating'], 9)
            self.assertEqual(json['cupcake']['image'], "http://test.com/updated.jpg")

    def test_update_cupcake_not_found(self):
        with app.test_client() as client:
            resp = client.patch("/api/cupcakes/9999", json={
                "flavor": "Nothing",
                "size": "None",
                "rating": 0,
                "image": "http://test.com/nothing.jpg"
            })

            self.assertEqual(resp.status_code, 404)

    def test_delete_cupcake_not_found(self):
        with app.test_client() as client:
            resp = client.delete("/api/cupcakes/9999")
            self.assertEqual(resp.status_code, 404)

    def test_delete_cupcake(self):
        with app.test_client() as client:
            resp = client.delete(f"/api/cupcakes/{self.cupcake_id}")
            self.assertEqual(resp.status_code, 200)

            data = resp.get_json()
            self.assertEqual(data, {"message": "Deleted"})

            self.assertIsNone(Cupcake.query.get(self.cupcake_id))

    def test_search_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes?search=TestFlavor")
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertEqual(len(data["cupcakes"]), 1)
            self.assertEqual(data["cupcakes"][0]["flavor"], "TestFlavor")


