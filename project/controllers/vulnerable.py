from flask import jsonify,render_template_string,request,render_template
from flask import render_template
from werkzeug.utils import secure_filename
import subprocess
from project import app
import sqlite3
import os.path
import os


@app.route("/home")
def main_page():
    return render_template('main.html')

@app.route('/login',methods=["GET"])
def login_page():
    return render_template('login.html')

@app.route("/hello")
def hello_page():
    return render_template('hello.html')

@app.route("/getUsers")
def get_users_page():
    return render_template('getUsers.html')

@app.route("/upload")
def upload_page():
    return render_template('upload.html')


@app.route("/admin")
def get_admin_mail_page():
    return render_template('admin.html')

#--------------------------------

@app.route("/hello")
def hello():
    if request.args.get('name'):
        name = request.args.get('name')
        template = f'''<div>
        <h1>Hello</h1>
        {name}
        </div>
        '''
        import logging
        logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
        logging.debug(str(template))
        return render_template_string(template)

@app.route("/get_users")
def get_users():
    try:
        hostname = request.args.get("hostname") 

        command = "dig " + hostname
        output = subprocess.check_output(command, shell=True)

        response_data = {
            "status": "success",
            "hostname": hostname,
            "result": output.decode("utf-8")
        }

        return jsonify(response_data)
    except Exception as e:
        response_data = {
            "status": "error",
            "message": f"Failed to look up hostname: {str(e)}",
            "hostname": hostname
        }

        return jsonify(response_data)

@app.route('/login', methods=["POST"])
def login():

    data = request.json 
    username = data.get("username")
    password = data.get("password")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "./../models/test.db")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM test WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone() 

    connection.close()

    if user:
        return jsonify(result="Login Succeeded")
    else:
        return jsonify(result="Login Unsucceeded")


@app.route('/upload', methods=['GET', 'POST'])
def uploadfile():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "./../upload")
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(result="File uploaded successfully")
    else:
        return render_template('upload.html')
