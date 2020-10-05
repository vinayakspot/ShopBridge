import requests

item_url = "http://localhost/shopbridge-backend/item"
item_list_url = "http://localhost/shopbridge-backend/list"

# Hardcode these values
POST_DATA = {
    'name': 'Some Name',
    'description': 'Some description',
    'price': '400'
}
files = [
    ('imgFile', open('/path/to/any/image.jpg','rb'))
]
GET_RESPONSE = {
    'name': 'Some Name',
    'description': 'Some description',
    'price': 400.0
}
DELETE_RESPONSE = {
    "message": "success"
}


class TestService:
    item_id = None

    def test_create(self):
        headers= {}
        response = requests.request("POST", item_url, headers=headers, data = POST_DATA, files = files)
        assert response.status_code == 200
        assert "id" in response.json()
        TestService.item_id = response.json()["id"]

    def test_get(self):
        response = requests.get(item_url + '/' + str(TestService.item_id))
        assert response.status_code == 200
        assert response.json() == GET_RESPONSE

    def test_list(self):
        response = requests.get(item_list_url, params={"id": TestService.item_id})
        print(response.json())
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_delete(self):
        response = requests.delete(item_url + '/' + str(TestService.item_id))
        print(response.json())
        assert response.status_code == 200
        assert response.json() == DELETE_RESPONSE
