from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return "<Task %r>" % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST" and request.form['content'] !="":
        task_content = request.form["content"]
        new_todo = Todo()
        new_todo.content = task_content
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your task!!!"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", task=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Delete operation was unsucessfull!!"


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        to_update.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Update operation was unsucessfull!!"
    else:
        return render_template("update.html",task=to_update)

if __name__ == "__main__":
    app.run(debug=True)
