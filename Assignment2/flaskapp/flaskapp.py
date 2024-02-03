import bcrypt
from create_database import create_database
from database import createUser, addUserInfo, getUser, getUserInfo, getUserFromLogin
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session
import os
from UserInfo import UserInfo

# Constants
ROOT = "/var/www/html/flaskapp"
DATABASE_NAME = ROOT + "/database.db"


# Create app
app = Flask(__name__)

create_database()
# .env Values
load_dotenv(ROOT + "/.env")
# Set secret
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        if signup(
            request.form["user_name"], request.form["pswrd"], request.form["c_pswrd"]
        ):
            return redirect("signup/info")

    return render_template("signup.html")


@app.route("/signup/info", methods=["GET", "POST"])
def signup_info_page():
    if "id" in session:
        if request.method == "POST":
            userInfo(
                request.form["firstName"],
                request.form["lastName"],
                request.form["email"],
            )
            return redirect("/me")
        return render_template("info.html")

    return redirect("/signup")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        if login(request.form["user_name"], request.form["pswrd"]):
            return redirect("me")

    return render_template("login.html")


@app.route("/me")
def me_page():
    if "id" in session:
        userInfo = getUserInfo(session["id"])
        return render_template(
            "me.html",
            userName=userInfo.user.userName,
            firstName=userInfo.firstName,
            lastName=userInfo.lastName,
            email=userInfo.email,
        )
    else:
        return redirect("login")


def login(userName: str, password: str):
    user = getUserFromLogin(userName)

    if bcrypt.checkpw(bytes(password, "utf-8"), bytes(user.password, "utf-8")):
        session["id"] = user.id
        return True

    return False


def signup(userName: str, password: str, confirmPassword: str):
    if password != confirmPassword:
        return False

    passHash = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())
    user = createUser(userName, passHash.decode("utf-8"))
    session["id"] = user.id
    return True


def userInfo(firstName: str, lastName: str, email: str):
    user = getUser(session["id"])
    addUserInfo(user, firstName, lastName, email)


if __name__ == "__main__":
    app.run()
