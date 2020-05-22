import sys
from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    # 0 for not 1 yes
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repe__(self):
        return '<Task %r>' % self.id
 
@app.route('/', methods=['POST', 'GET'])
def home():

    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue assing your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('home.html', tasks=tasks)
    

@app.route('/about')
def about():
    return 'About page'

@app.route('/tasks')
def tasks():
    return 'show all tasks'

@app.route('/tasks/new_task')
def newTasks():
    return 'input new task'

@app.route('/tasks/remove_task')
def removeTasks():
    return 'remove task'

@app.route('/tasks/modify_task')
def modifyTasks():
    return 'modify task'

if __name__ == '__main__':
    app.run(debug=True)