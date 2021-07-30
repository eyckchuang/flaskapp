import sqlite3

from flask import Flask, render_template, request, make_response, g
from flask_bootstrap import Bootstrap


from flask_sqlalchemy import SQLAlchemy

from restpluggable import BookAPI
from models import Students, Books, User
from __init__ import create_app, db
from myform import AdmissionForm, LoginForm

from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_uploads import UploadSet, configure_uploads, DATA, IMAGES

# app = Flask(__name__)

app = create_app()
app.static_folder = 'static'
app.config['UPLOAD_FOLDER'] = 'upload'
login_manager = LoginManager(app)
bs = Bootstrap(app)


@app.before_first_request
def first_request():
    print("This function is run before first request")


@app.before_request
def each_request():
    g.user = 'guest'
    print("This is run before {} visits '{}'".format(g.user, request.path))


@app.after_request
def after_request(response):
    print("This executes after exiting '{}'".format(request.path))
    return response


@app.route('/myip')
def myip():
    return "<h2>Your IP address is {}: {}</h2>".format(request.remote_addr, g.user)


@app.route('/createtable')
def createtable():
    con = sqlite3.connect("mydata.db")
    cur = con.cursor()
    createqry = '''
    create table if not exists Students (
    Name string (20) not null,
    Course string (20) ,
    Gender string (20),
    Mobile integer (10),
    Username string (6) primary key not null,
    Password text (8) not null
    );
    '''
    cur.execute(createqry)
    return 'ok'


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/books')
def booklist():
    q = db.session.query(Books, Students)
    rows = q.filter(Books.borrower == Students.username).all()
    return render_template('showbooks.html', rows=rows)


@app.route('/admission', methods=['GET', 'POST'])
def admission():
    form = AdmissionForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('admission.html', form=form)
        else:
            return '''
            <h1>Form successfully submitted</h1>
            <h2>Form Data Received</h2>
            <b>Name :{}<br>
            DOB : {} <br>
            Branch : {}</b>
            '''.format(form.student.data, form.dob.data, form.branch.data)
    elif request.method == 'GET':
        return render_template('admission.html', form=form)


# @app.route('/')
# def index():
#     list=[5,8,4,6,7]
#     string='Hello'
#     return render_template('hh.html',list=list,string=string)

# def result():
#     students = [('Anil',55),('Rajeev',40),('Leela',60),('Zuber',75),('John',30)]
#     return render_template("langs.html",students=students)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nm = request.form.get('name')
        # nm = request.args.get('name')
        # nm = request.args.get('name')
        # nm = request.args.get('name')
        return """<b>Name:</b>{}<br>""".format(nm)

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['uid']
        pwd = request.form['pswd']
        user = User.query.filter_by(id=id).first()
        if user is not None and user.pwd == pwd:
            login_user(user)
            return "<h2>you are logged in.</h2><a href='/logout'>logout</a>"
        else:
            return "<h2>Try again.</h2><a href='/'>click to go back</a>"
    else:
        form = LoginForm()
        return render_template("loginform.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/profile')
@login_required
def myprofile():
    user = current_user
    return render_template('myprofile.html', user=user)


# img = UploadSet("image", IMAGES)
# configure_uploads(app, img)
# app.config['UPLOADED_DEF_DEST'] = r'D:\proPycharm\flask_test\static\image_fold'
# app.config['UPLOADED_DEF_URL'] = '\\static\\upload\\'
#
#
# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST' and 'img' in request.files:
#         filename = img.save(request.files['img'])
#         return "file saved."


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "<h2>you are logged out.</h2><a href='/'>click to go back</a>"


@app.route('/hello/<name>/<int:age>')
def hello(name, age):
    return render_template('hello.html', name=name, age=age)


@app.template_filter("isodd")
def isodd(x):
    if x % 2 == 1:
        result = True
    else:
        result = False
    return result


@app.route('/adds')
def adds():
    s1 = Students("Amanpreet", "C/C++", "Male", "9741236457", "aman", "aman123")
    db.session.add(s1)
    db.session.commit()
    return "done"


@app.route('/dels')
def dels():
    s1 = Students.query.filter_by(username='aman').first()
    db.session.delete(s1)
    db.session.commit()
    return "done"


# @app.route('/<name>')
# def index(name):
#     return render_template('btn.html', name=name)


@app.route('/page')
def page():
    name = request.args.get('name')
    age = request.args.get('age')
    return render_template('page.html', name=name, age=age)


@app.route('/form')
def form():
    return render_template('register.html')


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['name']
        resp = make_response(render_template('setcookie.html'))
        resp.set_cookie('userID', user)
        return resp


@app.route('/readcookie')
def readcookie():
    name = request.cookies.get('userID')
    return render_template('readcookie.html', name=name)


@app.route('/addrectomongo', methods=['POST', 'GET'])
def addrectomongo():
    if request.method == 'POST':
        student = Students(name=request.form['name'])
        student.course = request.form['course']
        student.gender = request.form['gender']
        student.mobile = request.form['mobile']
        student.username = request.form['user']
        student.password = request.form['pwd']
        student.save()
        return 'success'
    # if request.method == 'POST':
    #     print(request.form.to_dict())
    #     students_collection = mongo.db.students
    #     students_collection.insert(request.form.to_dict())
    #     return 'added successfully'


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        con = sqlite3.connect("mydata.db")
        cur = con.cursor()
        msg = ''
        try:
            nm = request.form['name']
            gndr = request.form['gender']
            course = request.form['course']
            mob = request.form['mobile']
            usr = request.form['user']
            pw = request.form['pwd']
            ins = "insert into Students values(?,?,?,?,?,?)"
            cur.execute(ins, (nm, gndr, course, mob, usr, encpwd(pw)))
            con.commit()
            msg = "record successfully added"
        except Exception as e:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template('result.html', msg=msg)


@app.route('/list')
def list():
    return render_template("studentlist.html", students=Students.objects)


if __name__ == '__main__':
    app.run()
