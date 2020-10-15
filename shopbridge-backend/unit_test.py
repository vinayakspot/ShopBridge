import requests

item_url = "http://localhost/shopbridge-backend/item"
item_list_url = "http://localhost/shopbridge-backend/list"
image_url = "http://localhost/shopbridge-backend/img"

POST_DATA = {
    'name': 'Some Name',
    'description': 'Some description',
    'price': '400'
}
files = [
    ('imgFile', open('img/125.jpg', 'rb'))
]
# files = [
#     ('imgFile', open('/path/to/any/image.jpg','rb'))
# ]
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

    # Create a new item and get its id
    def test_create(self):
        headers = {}
        response = requests.request("POST", item_url, headers=headers, data=POST_DATA, files=files)
        assert response.status_code == 200
        assert "id" in response.json()
        TestService.item_id = response.json()["id"]

    # Test the new created item by its id
    def test_get(self):
        response = requests.get(item_url + '/' + str(TestService.item_id))
        assert response.status_code == 200
        assert response.json() == GET_RESPONSE

    # Fetch Image of new created item
    def test_image_fetch(self):
        response = requests.get(image_url + '/' + str(TestService.item_id) + '.jpg')
        assert response.status_code == 200

    # Get list of items and check list has at least 1 row
    def test_list(self):
        response = requests.get(item_list_url, params={"id": TestService.item_id})
        print(response.json())
        assert response.status_code == 200
        assert len(response.json()) > 0

    # Delete the created item by its id
    def test_delete(self):
        response = requests.delete(item_url + '/' + str(TestService.item_id))
        assert response.status_code == 200
        assert response.json() == DELETE_RESPONSE

    # Test to fetch item data when no item id exists in database
    def test_get_invalid_id(self):
        response = requests.get(item_url + '/' + str(TestService.item_id))
        assert response.status_code == 404
        assert response.json() == {'message': 'No data with associated id'}

    # Try to Delete the item by its invalid id
    def test_delete_invalid_id(self):
        response = requests.delete(item_url + '/' + str(TestService.item_id))
        assert response.status_code == 200
        assert response.json() == {'message': 'success'}

    # Try to Delete with no item id provided
    def test_invalid_api_request(self):
        response = requests.delete(item_url)
        assert response.status_code == 405

    # Create a new item with invalid parameters
    def test_create_invalid_params(self):
        INVALID_POST_DATA = {
            'invalid_name_key': 'Some Name',
            'invalid_description_key': 'Some description',
            'invalid_price_key': '400'
        }
        headers = {}
        response = requests.request("POST", item_url, headers=headers, data=INVALID_POST_DATA, files=files)
        assert response.status_code == 400

    # Fetch Image with invalid item id
    def test_image_fetch_invalid_id(self):
        response = requests.get(image_url + '/' + str(TestService.item_id) + '.jpg')
        assert response.status_code == 404
