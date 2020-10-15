from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from DatabaseUtil import DatabaseUtil
import json
import os

app = Flask(__name__, static_url_path='')
# Handling Cross Origin Resource Sharing
CORS(app)


# API to list all items
@app.route('/list', methods=['GET'])
def list_items():
    try:
        results = []
        # Create response JSON for each item present
        for row in DatabaseUtil().list_all_items():
            data = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": float(row[3])
            }
            results.append(data)
        return json.dumps(results)
    except Exception as e:
        resp = jsonify({'message': str(e)})
        resp.status_code = 400
        return resp


# API to create new item
@app.route('/item', methods=['POST'])
def add_item():
    try:
        # Getting all multipart form data
        json_data = {'name': request.form['name'], 'description': request.form['description'],
                     'price': request.form['price']}
        file = request.files['imgFile']

        # Calling database function to make a new entry in database
        res = DatabaseUtil().insert_item_row(json_data['name'], json_data['description'], json_data['price'])
        if res:
            data = {
                "id": res[0][0]
            }
            # Saving the Image file to img directory
            file.save('img/' + str(res[0][0]) + '.jpg')
            return json.dumps(data)
        else:
            # Handling error in case database write failed with exception
            resp = jsonify({'message': 'Database Error'})
            resp.status_code = 500
            return resp
    except Exception as e:
        resp = jsonify({'message': str(e)})
        resp.status_code = 400
        return resp


# API to get item detail using item id
@app.route('/item/<item_id>', methods=['GET'])
def get_item(item_id):
    try:
        # Calling database function to get item detail using item id
        res = DatabaseUtil().get_item_detail(item_id)
        if res:
            # Creating response JSON
            data = {
                "name": res[0][1],
                "description": res[0][2],
                "price": float(res[0][3])
            }
            return json.dumps(data)
        else:
            # Handling the case when no data is found in database for provided item id
            resp = jsonify({'message': 'No data with associated id'})
            resp.status_code = 404
            return resp
    except Exception as e:
        resp = jsonify({'message': str(e)})
        resp.status_code = 400
        return resp


# API to delete item with item id
@app.route('/item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        # Calling database function to delete item with item id
        DatabaseUtil().delete_item(item_id)
        data = {
            "message": "success"
        }
        file_path = 'img/' + str(item_id) + '.jpg'
        # Remove image from img directory associated with item id
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("The file does not exist")
        return json.dumps(data)
    except Exception as e:
        resp = jsonify({'message': str(e)})
        resp.status_code = 400
        return resp


# API to send image file from img directory
@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('img', path)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
