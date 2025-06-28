from flask import Blueprint, render_template, request, redirect, url_for, session, render_template_string, flash, send_from_directory, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from ..db import db 
from ..db.models import User

web = Blueprint("web",__name__)
UPLOAD_FOLDER = Path(os.getcwd() + '/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



class AppProduct:
    def __init__(self,id,image_url,name, description, cart_id, product_id, quantity, price):
        self.id = id
        self.image_url = image_url
        self.name = name
        self.description = description
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

  

products_list = [
    AppProduct(1,"https://images.pexels.com/photos/905847/pexels-photo-905847.jpeg","pizza","Qui adipisicing exercitation magna aliquip labore aute velit et. Esse tempor excepteur elit laborum deserunt exercitation ex reprehenderit est ad sit eiusmod. Eu tempor anim esse adipisicing aute aliqua laboris sit fugiat. Qui Lorem Lorem ea quis do incididunt adipisicing. Aliqua culpa duis excepteur eu sint laborum quis labore aliquip sint. Ex consectetur officia sint fugiat tempor consequat duis proident minim do magna ad",1, 1, 100, 15),
    AppProduct(2,"https://images.pexels.com/photos/1132558/pexels-photo-1132558.jpeg","strawberries","Ea enim anim cillum quis laboris ullamco esse. Sunt ut fugiat nulla duis non veniam quis labore ut velit nulla aliqua. Irure cillum reprehenderit anim incididunt cupidatat elit. Laboris non ut pariatur elit culpa occaecat fugiat magna duis labore laborum",1, 2, 50, 13),
    AppProduct(3,"https://images.pexels.com/photos/2912108/pexels-photo-2912108.jpeg","wine","Proident ullamco Lorem sunt et ea id ex nisi. Amet nisi cillum cupidatat nisi cupidatat qui irure elit ipsum commodo eu. Anim veniam enim minim pariatur. Anim do eu aliquip elit. Aute ad ea excepteur nisi et magna est consequat", 1, 3, 10, 20),
    AppProduct(4, "https://images.pexels.com/photos/376464/pexels-photo-376464.jpeg", "pancakes", "Pariatur ut cupidatat proident voluptate est ea. Elit sint dolor adipisicing dolore ad. Occaecat ea duis cupidatat culpa velit Lorem duis elit do sunt enim sit. Nulla enim laboris aute cupidatat quis aliquip. Aliqua mollit aute exercitation occaecat tempor sit officia commodo veniam incididunt laboris. Esse fugiat quis sit nulla anim ex pariatur veniam quis ullamco cillum elit. Dolor culpa ipsum magna elit aliquip tempor Lorem laborum.", 1, 3, 10, 10),
    AppProduct(5, "https://images.pexels.com/photos/291528/pexels-photo-291528.jpeg", "chocolate cake", "Tempor id adipisicing voluptate adipisicing elit consequat aliquip dolor pariatur nulla incididunt. Est sit ullamco tempor incididunt cillum. Minim ex ullamco laborum veniam fugiat qui magna adipisicing aliquip id ipsum cillum pariatur do. Cupidatat ea fugiat amet qui minim qui occaecat in proident Lorem esse mollit. Proident esse dolore incididunt deserunt non consectetur anim laborum ad amet duis. Incididunt fugiat excepteur do id sunt incididunt sunt voluptate aliqua.", 1, 3, 10, 13),
    AppProduct(6, "https://images.pexels.com/photos/808941/pexels-photo-808941.jpeg", "Macarons", "Labore proident et deserunt minim pariatur. Eu eu cillum fugiat ut quis ullamco sunt enim proident adipisicing culpa non duis Lorem. Excepteur laboris Lorem velit mollit officia nisi non reprehenderit mollit commodo ex. Esse irure sit dolore mollit ea cillum commodo nulla incididunt veniam. Ullamco enim cillum dolor enim officia consectetur do non ad officia amet incididunt cillum. Duis dolor elit excepteur magna cillum reprehenderit et non culpa dolor. Quis fugiat non ex Lorem amet.", 1, 3, 10, 20)
]




def allowed_file(filename):
    """ Allow files """
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

## ===========================
## GET

@web.route("/", methods=["GET"])
def index():
    """ Render the landing page"""
    return render_template("index.html")


@web.route("/home", methods=["GET"])
def home():
    return render_template("fragments/home.html")


@web.route("/login", methods=["GET"])
def login():
    if session and "username" in session:
        return redirect(url_for("web.dashboard"))
    return render_template("fragments/login.html")


@web.route("/signup", methods=["GET"])
def signup():
    if session and "username" in session:
        return redirect(url_for("web.dashboard"))
    return render_template("fragments/signup.html")


@web.route("/dashboard", methods=["GET"])
def dashboard():
    if session and "username" in session:
        email = session["username"]
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar()
        if user:
            return render_template('fragments/dashboard.html', user=user)
    session["error"] = {'message': 'You are not logged in'}    
    return redirect(url_for('web.error'))

@web.route('/error', methods=["GET"])
def error():
    error = session.pop('error', None)
    return render_template('fragments/error.html', message=error["message"])


@web.route('/static/<name>')
def display_file_content(name):
    return send_from_directory(UPLOAD_FOLDER, name)


@web.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('web.login'))
     

@web.route('/offers', methods=["GET"])
def menu():
    offers = products_list
    return render_template('fragments/offers.html', offers=offers)



@web.route("/cart/add/<int:id>", methods=["GET"])
def card_add(id):
    return
       



## ===========================
## POST







@web.route("/auth/login", methods=["POST"])
def auth_login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = db.session.execute(db.select(User).filter_by(email=email)).scalar()
    if not user:
        session["error"]= { 'message': 'Invalid Data'}
        return redirect(url_for('web.error'))  
    if not user.check_password(password):
        session["error"]= { 'message': 'Invalid Data'}
        return redirect(url_for('web.error')) 
    session["username"] = user.email 
    return redirect(url_for('web.dashboard'))
    

    
@web.route("/user/create", methods=["POST"])
def user_create():
    if 'photo' not in request.files:
            flash('No photo part')
            return redirect(request.url)
    photo = request.files['photo']
    if photo.filename == '':
            flash('No selected photo')
            return redirect(request.url)
    if photo and allowed_file(photo.filename):
        photo_name = secure_filename(photo.filename)
        photo.save(os.path.join(UPLOAD_FOLDER, photo_name))
        email = request.form.get('email')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')

        user = User(
            email=email,
            firstname = firstname,
            lastname = lastname,
            photo_url = photo_name
        )

        user.password = password
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('web.login'))
    session["error"] = { 'message' : 'Fail to sign up'}
    return redirect(url_for('web.error'))

