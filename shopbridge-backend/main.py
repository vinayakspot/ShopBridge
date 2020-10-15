from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from DatabaseUtil import DatabaseUtil
import json
import os

app = Flask(__name__, static_url_path='')
CORS(app)


@app.route('/list', methods=['GET'])
def list_items():
    try:
        results = []
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


@app.route('/item', methods=['POST'])
def add_item():
    try:
        json_data = {'name': request.form['name'], 'description': request.form['description'],
                     'price': request.form['price']}
        file = request.files['imgFile']

        res = DatabaseUtil().insert_item_row(json_data['name'], json_data['description'], json_data['price'])
        if res:
            data = {
                "id": res[0][0]
            }
            file.save('img/' + str(res[0][0]) + '.jpg')
            return json.dumps(data)
        else:
            resp = jsonify({'message': 'Database Error'})
            resp.status_code = 500
            return resp
    except Exception as e:
        resp = jsonify({'message': str(e)})
        resp.status_code = 400
        return resp


@app.route('/item/<item_id>', methods=['GET'])
def get_item(item_id):
    try:
        print("json_data", item_id)
        res = DatabaseUtil().get_item_detail(item_id)
        if res:
            data = {
                "name": res[0][1],
                "description": res[0][2],
                "price": float(res[0][3])
            }
            return json.dumps(data)
        else:
            resp = jsonify({'message': 'No data with associated id'})
            resp.status_code = 404
            return resp
    except Exception as e:
        resp = jsonify({'message': str(e)})
        resp.status_code = 400
        return resp


@app.route('/item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        if item_id:
            DatabaseUtil().delete_item(item_id)
            data = {
                "message": "success"
            }
            file_path = 'img/'+str(item_id) + '.jpg'
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                print("The file does not exist")
            return json.dumps(data)
        else:
            resp = jsonify({'message': 'Database Error'})
            resp.status_code = 500
            return resp
    except Exception as e:
        resp = jsonify({'message': str(e)})
        resp.status_code = 400
        return resp


@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('img', path)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')
