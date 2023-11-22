from flask import Flask,jsonify,render_template_string,request,Response,render_template
from flask import render_template, redirect, url_for
from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename
import subprocess
from project import app
import sqlite3
import os.path
import os

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

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

@app.route("/createFile")
def create_file_page():
    return render_template('createFile.html')

@app.route("/upload")
def upload_page():
    return render_template('upload.html')


@app.route("/readFile")
def readFile():
    return render_template('readFile.html')


@app.route("/get_admin_mail/admin")
def get_admin_mail_page():
    return render_template('admin.html')

#--------------------------------

@app.route("/user/<string:name>")
def search_user(name):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    cur.execute("select * from test where username = '%s'" % name)
    data = str(cur.fetchall())
    con.close()
    import logging
    logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)
    return jsonify(data=data),200

@app.route("/welcome/<string:name>")
def welcome(name):
    data="Welcome "+name
    return jsonify(data=data),200

@app.route("/welcome2/<string:name>")
def welcome2(name):
    data="Welcome "+name
    return data

@app.route("/hello")
def hello_ssti():
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
        hostname = request.args.get('hostname')
        command = "dig " + hostname
        data = subprocess.check_output(command, shell=True)
        
        return jsonify(result=data)
    except:
        data = str(hostname) + " hostname not found"
        return jsonify(result=data)

@app.route("/get_log/")
def get_log():
    try:
        command="cat restapi.log"
        data=subprocess.check_output(command,shell=True)
        return data
    except:
        return jsonify(data="Command didn't run"), 200


@app.route('/login', methods=["POST"])
def login():
    username=request.args.get("username")
    password=request.args.get("password")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "./../models/test.db")
    print(os.getcwd())

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Consulta o banco de dados para encontrar um usuário correspondente
    cursor.execute('SELECT * FROM test WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()

    connection.close()

    if user:
        return jsonify(result="Login Succeeded")
    else:
        return jsonify(result="Login Unsuccedeed")


@app.route('/upload', methods=['GET', 'POST'])
def uploadfile():

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "./upload")
    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(result="File uploaded successfully")
    else:
        return render_template('upload.html')
    
from flask import request, jsonify

@app.route("/createFile", methods=['POST'])
def create_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = request.form.get("filename")
        text = request.form.get("text")
        
        # Abre o arquivo para escrita e salva o texto
        with open(filename, "w") as file:
            file.write(text)

        # Salva o arquivo enviado pelo formulário
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return jsonify(data="File created"), 200
    else:
        return jsonify(data="File didn't create"), 200

@app.route('/logs')
def ImproperOutputNeutralizationforLogs():
    data = request.args.get('data')
    import logging
    logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)
    return jsonify(data="Logging ok"), 200

