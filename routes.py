from flask import Blueprint, render_template, jsonify, request
from flask_restful import Api, Resource
from restpluggable import BookAPI, BookItem, BookList
from models import Books, db

root_bp = Blueprint('root', __name__)


@root_bp.route('/')
def index():
    return render_template('index.html')

#
# @root.route('/books/', methods=['GET'])
# def allbooks():
#     res = Books.query.all()
#     lb = []
#     for i in res:
#         s = i.serialize()
#         lb.append(s)
#     return jsonify({"books": lb})
#
#
# @root.route('/books/<id>', methods=['GET'])
# def getbook(id):
#     res = Books.query.filter_by(book_id=id).first()
#     book = res.serialize()
#     return jsonify({"book": book})
#
#
# @root.route('/books', methods=['POST'])
# def addbook():
#     book = Books(request.json['book_id'], request.json['title'], request.json['author'], request.json['price'])
#     db.session.add(book)
#     db.session.commit()
#     return allbooks()
#
#
# @root.route('/books/<id>', methods=['PUT'])
# def updatebook(id):
#     id = request.json['book_id']
#     price = request.json['price']
#     res = Books.query.filter_by(book_id=id).first()
#     res.price = price
#     db.session.commit()
#     book = res.serialize()
#     return jsonify({"book": book})
#
#
# @root.route('/books/<id>', methods=['DELETE'])
# def deletebook(id):
#     res = Books.query.filter_by(book_id=id).first()
#     db.session.delete(res)
#     db.session.commit()
#     return allbooks()


book_view = BookAPI.as_view('book_api')
root_bp.add_url_rule('/books/', defaults={'id': None}, view_func=book_view, methods=['GET', ])
root_bp.add_url_rule('/books/', view_func=book_view, methods=['POST', ])
root_bp.add_url_rule('/books/<id>', view_func=book_view, methods=['GET', 'PUT', 'DELETE'])

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
api.add_resource(BookList, '/books/')
api.add_resource(BookItem, '/books/<id>')
