from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def time_ago(time):
    time = time + timedelta(hours=5, minutes=30)
    now = datetime.now()
    diff = now - time

    seconds = diff.total_seconds()

    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} min ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hr ago"
    elif seconds < 604800:
        days = int(seconds // 86400)
        return f"{days} day ago"
    else:
        return time.strftime("%d %b %Y")

app.jinja_env.filters['timeago'] = time_ago


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET','POST'])
def home_page():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')

        if title and desc:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()

    alltodo = Todo.query.all()
    return render_template("todo.html", alltodo=alltodo)


@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()

    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')

        if title and desc:
            todo.title = title
            todo.desc = desc
            db.session.commit()
            return redirect('/')

    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))