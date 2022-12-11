from flask import  Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) # создание объекта на основе класса Flask# __name - директива для запуска файла
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    pretext = db.Column(db.String(500), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Entries %r' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/entries')
def entries():
    entries = Entries.query.order_by(Entries.date.desc()).all()
    return render_template("entries.html", entries=entries)


@app.route('/entries/<int:id>')
def entries_more(id):
    entrie = Entries.query.get(id)
    return render_template("entries_more.html", entrie=entrie)

@app.route('/create-entries', methods=['POST', 'GET'])
def create_entries():
    if request.method == "POST":
        title = request.form['title']
        pretext = request.form['pretext']
        text = request.form['text']

        entries = Entries(title=title, pretext=pretext, text=text)

        try:
            db.session.add(entries)
            db.session.commit()
            return redirect('/entries')
        except:
            return "При создании треда произошла ошибка"
    else:
        return render_template("create-entries.html")


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: " + name + " - " + str(id)

if __name__ == "__main__":
    app.run(debug=True)