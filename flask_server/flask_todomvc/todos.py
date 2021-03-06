from .extensions import db
from .models import Todo
from flask import Blueprint, jsonify, request

import json

bp = Blueprint('todos', __name__, url_prefix='/todos')

@bp.route('/', methods=['POST'])
def create():
  todo = Todo()
  todo.from_json(request.get_json())
  db.session.add(todo)
  db.session.commit()
  return _todo_response(todo)

@bp.route('/all', methods=['GET'])
def read_all():
  todos = Todo.query.all()
  todo_list = list(map(Todo.to_json, todos))
  return json.dumps(todo_list)

@bp.route('/<int:id>')
def read(id):
  todo = Todo.query.get_or_404(id)
  return _todo_response(todo)

@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
  todo = Todo.query.get_or_404(id)
  todo.from_json(request.get_json())
  db.session.commit()
  return _todo_response(todo)

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
  Todo.query.filter_by(id=id).delete()
  db.session.commit()
  return jsonify()

def _todo_response(todo):
  return jsonify(**todo.to_json())
