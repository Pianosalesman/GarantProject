import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

ITEMS = []


def remove_item(item_id):
    for item in ITEMS:
        if item['id'] == item_id:
            ITEMS.remove(item)
            return True
        return False


@app.route('/items', methods=['GET', 'POST'])
def all_items():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        ITEMS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'body': post_data.get('body'),
            'period': post_data.get('period'),
            'start': post_data.get('start'),
            'end': post_data.get('end')
        })
        response_object['message'] = 'Гарантия добавлена!'
    else:
        response_object['items'] = ITEMS
    return jsonify(response_object)


@app.route('/items/<item_id>', methods=['PUT', 'DELETE'])
def single_items(item_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_item(item_id)
        ITEMS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'body': post_data.get('body'),
            'period': post_data.get('period'),
            'start': post_data.get('start'),
            'end': post_data.get('end')
        })
        response_object['message'] = 'Гарантия обновлена!'

    if request.method == 'DELETE':
        remove_item(item_id)
        response_object['message'] = 'Гарантия удалена!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(debug=True)
