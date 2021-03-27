from flask_wtf import FlaskForm
from wtforms import FieldList, SelectField, StringField
from wtforms.validators import DataRequired

from jimmy import models


class PersonForm(FlaskForm):
    last_name = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    second_name = StringField('Отчество')
    degree = SelectField('Уч. степень', choices=models.Person.DEGREES)
    title = SelectField('Уч. звание', choices=models.Person.TITLES)
    emails = FieldList(StringField('Почта'))
