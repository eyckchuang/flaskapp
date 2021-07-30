from flask.views import MethodView
from flask import Flask, request, jsonify
from flask_restful import Resource

from models import Books, db


class BookAPI(MethodView):

    def get(self, id):
        if id is None:
            res = Books.query.all()
            lb = []
            for i in res:
                s = i.serialize()
                lb.append(s)
            return jsonify({"books": lb})
        else:
            res = Books.query.filter_by(book_id=id).first()
            book = res.serialize()
            return jsonify({"book": book})

    def post(self):
        book = Books(request.json['book_id'], request.json['title'], request.json['author'], request.json['price'])
        db.session.add(book)
        db.session.commit()
        res = Books.query.all()
        lb = []
        for i in res:
            s = i.serialize()
            lb.append(s)
        return jsonify({"books": lb})

    def delete(self, id):
        res = Books.query.filter_by(book_id=id).first()
        db.session.delete(res)
        db.session.commit()
        res = Books.query.all()
        lb = []
        for i in res:
            s = i.serialize()
            lb.append(s)
        return jsonify({"books": lb})

    def put(self, id):
        id = request.json['book_id']
        price = request.json['price']
        res = Books.query.filter_by(book_id=id).first()
        res.price = price
        db.session.commit()
        book = res.serialize()
        return jsonify({'book': book})


class BookItem(Resource):
    def get(self, id):
        if id is None:
            res = Books.query.all()
            lb = []
            for i in res:
                s = i.serialize()
                lb.append(s)
            return jsonify({"books": lb})
        else:
            res = Books.query.filter_by(book_id=id).first()
            book = res.serialize()
            return jsonify({"book": book})

    def delete(self, id):
        res = Books.query.filter_by(book_id=id).first()
        db.session.delete(res)
        db.session.commit()
        res = Books.query.all()
        lb = []
        for i in res:
            s = i.serialize()
            lb.append(s)
        return jsonify({"books": lb})

    def put(self, id):
        id = request.json['book_id']
        price = request.json['price']
        res = Books.query.filter_by(book_id=id).first()
        res.price = price
        db.session.commit()
        book = res.serialize()
        return jsonify({'book': book})


class BookList(Resource):
    def get(self):
        res = Books.query.all()
        lb = []
        for i in res:
            s = i.serialize()
            lb.append(s)
        return jsonify({"books": lb})

    def post(self):
        book = Books(request.json['book_id'], request.json['title'], request.json['author'], request.json['price'])
        db.session.add(book)
        db.session.commit()
        res = Books.query.all()
        lb = []
        for i in res:
            s = i.serialize()
            lb.append(s)
        return jsonify({"books": lb})
