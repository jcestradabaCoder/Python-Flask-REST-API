from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

user = 'jcestradaba'
pwd = 'jceb94'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + user + ':' + pwd + '@localhost/db_tasks?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(70), unique = True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many = True)

@app.route('/', methods = ['GET'])
def index():
    return jsonify({'message': 'Welcome to task REST API'})


@app.route('/tasks', methods = ['POST'])
def create_task():
    # print(request.json)

    title = request.json['title']
    description = request.json['description']

    new_task = Task(title, description)
    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)


@app.route('/tasks', methods = ['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)

    return jsonify(result)


@app.route('/tasks/<id>', methods = ['GET'])
def get_task_by_id(id):
    task = Task.query.get(id)

    return task_schema.jsonify(task)


@app.route('/tasks/<id>', methods = ['PUT'])
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()

    return task_schema.jsonify(task)


@app.route('/tasks/<id>', methods = ['DELETE'])
def delete_task(id):
    task = Task.query.get(id)

    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

if __name__ == "__main__":
    app.run(debug = True)