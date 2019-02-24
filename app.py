from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for



app = Flask(__name__)
DB_URL = 'postgres://vnlkwtanyvyszi:430036ca9cf52e2a079bf370fedcf62c5564f1d55540e3f79b9f10e66323f1df@ec2-54-227-246-152.compute-1.amazonaws.com:5432/dspj71ln4p30f'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.debug = True
db = SQLAlchemy(app)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    NIM = db.Column(db.String(10), unique=True)
    absence_count = db.Column(db.Integer, nullable=True)

    def __init__(self, name, NIM):
        self.name = name
        self.NIM = NIM

    def __repr__(self):
        return '<Students %r>' % self.name


@app.route('/')
def index():
    myStudent = Students.query.all()
    oneItem = Students.query.filter_by(name="test").first()
    return render_template('add_student.html', myStudent=myStudent, oneItem=oneItem)


@app.route('/add_student', methods=['POST'])
def add_student():
    student = Students(request.form['name'], request.form['NIM'])
    student.absence_count = 0
    db.session.add(student)  # add to db
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/get_student/<NIM>')
def get_student(NIM):
    student = Students.query.filter_by(NIM=NIM).first()
    return render_template('profile.html', student=student)


@app.route('/get_absence/<NIM>')
def get_absence(NIM):
    student = Students.query.filter_by(NIM=NIM).first()
    return render_template('profile.html', absence_count=student.absence_count)


@app.route('/update_absence', methods=['POST'])
def update_absence():
    student_updated = Students.query.filter_by(NIM=request.form['NIM']).first()
    student_updated.absence_count = student_updated.absence_count + 1
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
