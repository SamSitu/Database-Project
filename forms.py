from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length 

class studentform(FlaskForm):
    id = StringField('StudentID', validators=[DataRequired(), Length(min=5, max=20)])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators = [DataRequired()])
    ssn = StringField('SSN', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    birthdate = StringField('Birthdate', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    gpa = FloatField('GPA', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('submit')
    
class updateform(FlaskForm):
    id = StringField('StudentID', validators=[DataRequired(), Length(min=5, max=20)])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators = [DataRequired()])
    ssn = StringField('SSN', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    birthdate = StringField('Birthdate', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    gpa = FloatField('GPA', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Update')
    
class deleteform(FlaskForm):
    id = StringField('StudentID', validators=[DataRequired(), Length(min=5, max=20)])
    submit = SubmitField('Delete')
    
class queryform(FlaskForm):
    id = StringField('StudentID')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    major = StringField('Major')
    submit = SubmitField('Query')
    
class departmentform(FlaskForm):
    name = StringField('Department Name', validators = [DataRequired()])
    submit = SubmitField('submit')

class courseform(FlaskForm):
    name = StringField('Course Name', validators = [DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('submit')

class enrollform(FlaskForm):
    name = StringField('Course Name', validators = [DataRequired()])
    id = StringField('Student ID', validators=[DataRequired()])
    submit = SubmitField('submit')
    