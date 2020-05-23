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
        u_tasks = Todo.query.filter_by(completed=0).all()
        c_tasks = Todo.query.filter_by(completed=1).all()
        return render_template('home.html', u_tasks=u_tasks, c_tasks=c_tasks)
    

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem deleting that task"
    else:
        return render_template('update.html', task=task_to_update)

@app.route('/complete/<int:id>')
def complete(id):
    task_to_complete = Todo.query.get_or_404(id)
    task_to_complete.completed = 1
    try:
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem completing that task"


@app.route('/uncomplete/<int:id>')
def uncomplete(id):
    task_to_complete = Todo.query.get_or_404(id)
    task_to_complete.completed = 0
    try:
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem completing that task"




@app.route('/about')
def about():
    return render_template('about.html')




if __name__ == '__main__':
    app.run(debug=True)