import flask
import flask_login
import hashlib
from functools import wraps
from flask import request, Response, render_template
from flask.ext.login import login_required
from pymongo import MongoClient
from bson.objectid import ObjectId

app = flask.Flask(__name__)
app.secret_key = '5441c5151ad92c83b722181b'

client = MongoClient('localhost', 27017)
db = client.test

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return db.users.find_one({'_id': ObjectId(userid)})

@app.route('/')
def home():
    cs = db.users.find({'username': {'$ne': 'pstandt'}})
    return render_template('candc.html', lawyers=cs)

@app.route('/files')
@login_required
def files():
    cs = db.cases.find()
    return render_template('files.html', cases=cs)

@app.route('/cases')
@login_required
def cases():
    cs = db.cases.find()
    return render_template('cases.html', cases=cs)

@app.route('/red')
def red():
    return 'x' * 10000 * 10000

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        pword = request.form['pword']
        user = db.users.find_one({'username': uname, 'password': hashlib.md5(pword).hexdigest()})
        if user:
            login_user(user)
            return user
        else:
            return "Error"

    return render_template('login.html', cases=[])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
