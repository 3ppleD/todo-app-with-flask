from flask import Blueprint,request,flash,redirect,url_for,render_template, session
from model.model import User
from app import db

user_bp = Blueprint("user_bp", __name__)

# @user_bp.route("/")
# def welcome():
#     return "Welcome to the Todo app"


@user_bp.route("/signup", methods = ['GET', 'POST'])
def signupUser():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmPass = request.form.get("confirmPass")

        if not name or not email or not password:
            flash("Error! All fileds are required.", 'error')

        elif password != confirmPass:
            flash("Password must be confirm password", 'warning')
        else:
            try:
                new_user = User(name=name,email=email,password=password)
                db.session.add(new_user)
                db.session.commit()
                flash("You have successfully registerd")
                return redirect(url_for("user_bp.signupUser"))
            except ValueError as e:
                flash(str(e),"error")
    return render_template("signup.html", redirect_url = url_for("user_bp.login"))   


@user_bp.route ("/",methods=["GET", "POST"])
def login():              
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            user = User.query.filter_by(email=email).first()

            if user and user.password == password:
                session["user_id"] = user.id
                session["name"] = user.name
                flash("Welcome back on board", "success")
                return redirect(url_for("todo_bp.homepage"))
            else:
                flash("Invalid email or password", "error")
                return render_template("login.html")
            
        return render_template("login.html")


