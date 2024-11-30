from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TopSecretAPIKey'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo-list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), unique=True, nullable=False)
    value = db.Column(db.String(10), nullable=False)

    def to_dictionary(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

#
# with app.app_context():
#     db.create_all()

now = datetime.now()
date_today = now.strftime('%m/%d/%Y')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/todo', methods=["GET", "POST"])
def to_do_list():
    todo_list = Task.query.all()

    if request.method == 'POST':
        task = request.form.get('input1')
        new_task = Task(
            task=task,
            value='ongoing',
        )
        with app.app_context():
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('to_do_list'))

    return render_template('todo.html', date=date_today, list=todo_list)


@app.route('/delete/<int:task_id>', methods=["DELETE", "GET"])
def delete_task(task_id):
    task_to_be_deleted = Task.query.filter_by(id=task_id).first()
    print(task_to_be_deleted.task)

    db.session.delete(task_to_be_deleted)
    db.session.commit()

    return redirect(url_for('to_do_list'))


if __name__ == '__main__':
    app.run(debug=True)