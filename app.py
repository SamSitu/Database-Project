from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import studentform, updateform, deleteform, queryform, departmentform, courseform, enrollform
       
app = Flask(__name__)
app.config['SECRET_KEY'] = 'databases'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

StudentCourses = db.Table('StudentCourses', 
                        db.Column('Studentid', db.Integer, db.ForeignKey('student.id')),
                        db.Column('coursename', db.String, db.ForeignKey('course.name'))
                        )

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    ssn = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(50))
    birthdate = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String)
    gpa = db.Column(db.Float)
    courses = db.relationship('Course', secondary=StudentCourses, backref = 'students')
    departmentname = db.Column(db.String, db.ForeignKey('department.name'))    

    def __repr__(self):
        return f"Student('{self.firstname}', '{self.lastname}')"
    
class Course(db.Model):
    name = db.Column(db.String, primary_key=True)
    departmentname = db.Column(db.String, db.ForeignKey('department.name'))
    enrolled = db.relationship('Student', secondary=StudentCourses, backref='course')
    
class Department(db.Model):
    name = db.Column(db.String, primary_key=True)
    student_id = db.relationship('Student', backref='department')
    course = db.relationship('Course', backref='department')
    
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/input", methods=['GET', 'POST'])
def input():
    form = studentform()
    if form.validate_on_submit():
        flash('Data Inputted!', 'success')
        department = Department.query.filter_by(name=form.department.data)
        student = Student(id=form.id.data, firstname=form.firstname.data, lastname=form.lastname.data, 
                          ssn=form.ssn.data, major=form.major.data, birthdate=form.birthdate.data,
                          address=form.address.data, gpa=form.gpa.data, departmentname=department)
        db.session.add(student)
        db.session.commit()
    return render_template('input.html', form=form)

@app.route("/update", methods=['GET','POST'])
def update():
    form = updateform()
    if form.validate_on_submit():
        department = Department.query.filter_by(name=form.department.data)
        student=Student.query.get_or_404(form.id.data)
        student.firstname= form.firstname.data
        student.lastname=form.lastname.data
        student.ssn=form.ssn.data
        student.major=form.major.data
        student.birthdate=form.birthdate.data
        student.address=form.address.data
        student.gpa=form.gpa.data
        student.department=department
        db.session.commit()
        flash('Data Updated!', 'success')
    return render_template('update.html', form=form)

@app.route("/delete", methods=['GET','POST'])
def delete():
    form = deleteform()
    if form.validate_on_submit():
        student = Student.query.get_or_404(form.id.data)
        db.session.delete(student)
        db.session.commit()
        flash('Data Deleted!', 'success')
    return render_template('delete.html', form=form)

@app.route("/querystudents", methods=['Get','POST'])
def querystudents():
    student=Student.query.all()
    return render_template('querystudents.html', student=student)

@app.route("/query", methods=['GET', 'POST'])
def query():
    form = queryform()
    if form.validate_on_submit():
        if form.id.data!="":
            student=Student.query.get_or_404(form.id.data)
            return render_template('queryresults.html', student=student)
        elif form.firstname.data!="":
            student=Student.query.filter_by(firstname=form.firstname.data)
            return render_template('queryresults.html', student=student)
        elif form.lastname.data!="":
            student=Student.query.filter_by(lastname=form.lastname.data)
            return render_template('queryresults.html', student=student)
        else:
            student=Student.query.filter_by(major=form.major.data)
            return render_template('queryresults.html', student=student)
    return render_template('query.html', form=form)        

@app.route("/department", methods=['Get','POST'])
def department():
    form = departmentform()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        flash('Department Added', 'success')
    return render_template('department.html', form=form)

@app.route("/course", methods=['Get','POST'])
def course():
    form = courseform()
    if form.validate_on_submit():
        department = Department.query.filter_by(name=form.department.data)
        course = Course(name=form.name.data, departmentname=department)
        db.session.add(course)
        db.session.commit()
        flash('Course Added', 'success')
    return render_template('course.html', form=form)

@app.route("/querydepartments", methods=['Get','POST'])
def querydepartments():
    department=Department.query.all()
    return render_template('querydepartments.html', department=department)

@app.route("/querycourse", methods=['Get','POST'])
def querycourses():
    course=Course.query.all()
    return render_template('querycourse.html', department=course)

@app.route("/enroll", methods=['Get','POST'])
def enroll():
    form=enrollform()
    if form.validate_on_submit():
        course=Course.query.get_or_404(form.name.data)
        student=Student.query.get_or_404(form.id.data)
        student.courses.append(course)
        db.session.commit()
    return render_template('enroll.html', form=form)

#with app.app_context():
#    db.drop_all()
#    db.create_all()
#    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
