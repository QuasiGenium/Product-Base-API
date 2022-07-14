import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid
import flask
import datetime

try:
    name = open('name.txt', 'r').readline()
except FileNotFoundError:
    print('Файла "name.txt" нет в папке с программой')
    raise FileNotFoundError
cred = credentials.Certificate(name)  # FIREBASE
firebase_admin.initialize_app(cred)
db = firestore.client()

blueprint = flask.Blueprint('products_api', __name__, template_folder='templates')  # API
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'kkkk'


@blueprint.route('/products')  # ПРОДУКТЫ
def get_products():
    products = db.collection('products')
    list_of_products = [i.to_dict() for i in products.stream()]
    li = [{'id': i.get('id'), 'name': i.get('name'), 'img': i.get('imgs')[0]}
          for i in sorted(list_of_products, key=lambda x: x.get('createdAt'), reverse=True)]
    return flask.jsonify(li)


@blueprint.route('/products/details')
def get_products_with_details():
    products = db.collection('products')
    list_of_products = [i.to_dict() for i in products.stream()]
    return flask.jsonify(sorted(list_of_products, key=lambda x: x.get('createdAt'), reverse=True))


@blueprint.route('/products/<string:product_id>', methods=['GET'])
def get_one_product(product_id):
    products = db.collection('products')
    list_of_products = [i.to_dict() for i in products.stream()]
    item = list(filter(lambda x: x.get('id') == product_id, list_of_products))
    if not item:
        return flask.jsonify({'result': '404', 'text': 'Not found'})
    return flask.jsonify({'id': item[0].get('id'), 'name': item[0].get('name'), 'img': item[0].get('imgs')[0]})


@blueprint.route('/products/<string:product_id>/details', methods=['GET'])
def get_one_product_details(product_id):
    products = db.collection('products')
    list_of_products = [i.to_dict() for i in products.stream()]
    item = list(filter(lambda x: x.get('id') == product_id, list_of_products))
    if not item:
        return flask.jsonify({'result': '404', 'text': 'Not found'})
    return flask.jsonify(item[0])


@blueprint.route('/products', methods=['POST'])
def create_product():
    products = db.collection('products')
    if not flask.request.json:
        return flask.jsonify({'result': '400', 'text': 'Bad request'})
    elif not all(key in flask.request.json for key in
                 ['name', 'imgs', 'category', "price", "content", "productLink"]):
        return flask.jsonify({'result': '400', 'text': 'Bad request'})
    n = str(uuid.uuid4())
    categories = db.collection('categories')
    list_of_categories = [i.to_dict() for i in categories.stream()]
    if flask.request.json['category'] not in list_of_categories:
        if flask.request.json['category'].get('name') not in [i.to_dict().get('name') for i in categories.stream()]:
            h = str(uuid.uuid4())
            cat = {'id': h, 'name': flask.request.json['category'].get('name')}
            categories.document(h).set(cat)
        else:
            cat = [i for i in list_of_categories if i.get('name') == flask.request.json['category'].get('name')][0]
    else:
        cat = flask.request.json['category']
    products.document(n).set({
        'id': n,
        'name': flask.request.json['name'],
        'imgs': flask.request.json['imgs'],
        'category': cat,
        "price": flask.request.json['price'],
        "content": flask.request.json['content'],
        "productLink": flask.request.json['productLink'],
        "createdAt": str(datetime.datetime.now())
    })
    return flask.jsonify({'result': '200', 'text': 'OK'})


@blueprint.route('/products/<string:product_id>', methods=['PUT'])
def put_one_product(product_id):
    products = db.collection('products')
    list_of_products = [i.to_dict() for i in products.stream()]
    item = list(filter(lambda x: x.get('id') == product_id, list_of_products))
    if not item:
        return flask.jsonify({'result': '404', 'text': 'Not found'})
    elif not all(key in flask.request.json for key in
                 ['name', 'imgs', 'category', "price", "content", "productLink"]):
        return flask.jsonify({'result': '400', 'text': 'Bad request'})
    products.document(product_id).set({
        'id': item[0].get('id'),
        'name': flask.request.json['name'],
        'imgs': flask.request.json['imgs'],
        'category': flask.request.json['category'],
        "price": flask.request.json['price'],
        "content": flask.request.json['content'],
        "productLink": flask.request.json['productLink'],
        "createdAt": item[0].get('createdAt')
    })
    return flask.jsonify({'result': '200', 'text': 'OK'})


@blueprint.route('/products/delete/<string:product_id>', methods=['DELETE'])
def delete_product(product_id):
    products = db.collection('products')
    list_of_products = [i.to_dict() for i in products.stream()]
    item = list(filter(lambda x: x.get('id') == product_id, list_of_products))
    if not item:
        return flask.jsonify({'result': '404', 'text': 'Not found'})
    products.document(item[0].get('id')).delete()
    return flask.jsonify({'result': '200', 'text': 'OK'})


@blueprint.route('/categories')  # КАТЕГОРИИ
def get_categories():
    categories = db.collection('categories')
    list_of_categories = [i.to_dict() for i in categories.stream()]
    return flask.jsonify(list_of_categories)


@blueprint.route('/categories/<string:category_id>', methods=['GET'])
def get_one_category(category_id):
    categories = db.collection('categories')
    list_of_categories = [i.to_dict() for i in categories.stream()]
    item = list(filter(lambda x: x.get('id') == category_id, list_of_categories))
    if not item:
        return flask.jsonify({'result': '404', 'text': 'Not found'})
    return flask.jsonify(item[0])


@blueprint.route('/categories', methods=['POST'])
def create_category():
    categories = db.collection('categories')
    if not flask.request.json:
        return flask.jsonify({'result': '400', 'text': 'Bad request'})
    elif not all(key in flask.request.json for key in ['name']):
        return flask.jsonify({'result': '400', 'text': 'Bad request'})
    n = str(uuid.uuid4())
    categories.document(n).set({'id': n, 'name': flask.request.json['name']})
    return flask.jsonify({'result': '200', 'text': 'OK'})


@blueprint.route('/categories/<string:category_id>', methods=['PUT'])
def put_one_category(category_id):
    categories = db.collection('categories')
    list_of_categories = [i.to_dict() for i in categories.stream()]
    item = list(filter(lambda x: x.get('id') == category_id, list_of_categories))
    if not item:
        return flask.jsonify({'result': '404', 'text': 'Not found'})
    elif not all(key in flask.request.json for key in ['name']):
        return flask.jsonify({'result': '400', 'text': 'Bad request'})
    categories.document(category_id).set({'id': item[0].get('id'), 'name': flask.request.json['name']})
    return flask.jsonify({'result': '200', 'text': 'OK'})


@blueprint.route('/categories/delete/<string:category_id>', methods=['DELETE'])
def delete_category(category_id):
    categories = db.collection('categories')
    list_of_categories = [i.to_dict() for i in categories.stream()]
    item = list(filter(lambda x: x.get('id') == category_id, list_of_categories))
    if not item:
        return flask.jsonify({'result': '404', 'text': 'Not found'})
    categories.document(item[0].get('id')).delete()
    return flask.jsonify({'result': '200', 'text': 'OK'})


@blueprint.route('/products/category/<string:category_id>', methods=['GET'])
def find_all_of_category(category_id):
    products = db.collection('products')
    list_of_products = [i.to_dict() for i in products.stream()]
    categories = db.collection('categories')
    list_of_categories = [i.to_dict() for i in categories.stream()]
    item = list(filter(lambda x: x.get('id') == category_id, list_of_categories))
    if not item:
        return flask.jsonify({'result': '404', 'text': 'Not found'})
    items = list(filter(lambda x: x.get('category').get('id') == category_id, list_of_products))
    return flask.jsonify(items)


def main():
    app.register_blueprint(blueprint)
    app.run()


if __name__ == '__main__':
    main()
