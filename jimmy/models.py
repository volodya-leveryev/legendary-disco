from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'{self.username}'


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    second_name = db.Column(db.String(25))
    degree = db.Column(db.String(12), nullable=False)
    title = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        result = f'{self.last_name} {self.first_name:.1}.'
        if self.second_name:
            result += f'{self.second_name:.1}.'
        return result


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    teacher = db.relationship('Teacher')
    position = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    wage_rate = db.Column(db.Numeric(precision=2), nullable=False)
