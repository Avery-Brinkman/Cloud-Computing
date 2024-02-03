from create_database import create_database
from database import getUserInfo
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session
import os
from backend import login, signup, userInfo, verifyUser

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
    return render_template("index.html", loggedIn=verifyUser())


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    # If we're already logged in, redirect
    if verifyUser():
        return redirect("/me")

    if request.method == "POST":
        if signup(
            request.form["user_name"], request.form["pswrd"], request.form["c_pswrd"]
        ):
            return redirect("signup/info")

    return render_template("signup.html")


@app.route("/signup/info", methods=["GET", "POST"])
def signup_info_page():
    # Check that user is logged in
    if verifyUser():
        if request.method == "POST":
            # Add the user info
            userInfo(
                request.form["firstName"],
                request.form["lastName"],
                request.form["email"],
            )
            # Show info
            return redirect("/me")

        # GET req for logged in user (to enter info)
        return render_template("info.html")

    return redirect("/signup")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        # Try to login
        if login(request.form["user_name"], request.form["pswrd"]):
            # Check if info needs to be added
            if getUserInfo(session["id"]) == None:
                return redirect("signup/info")

            # Otherwise show user info
            return redirect("me")

    return render_template("login.html")


@app.route("/me")
def me_page():
    # Check that user is logged in
    if verifyUser():
        # Get their info
        userInfo = getUserInfo(session["id"])

        # Check that we have info
        if userInfo != None:
            # Show page w user info
            return render_template(
                "me.html",
                userName=userInfo.user.userName,
                firstName=userInfo.firstName,
                lastName=userInfo.lastName,
                email=userInfo.email,
            )

    # Redirect to login if we failed at any step of the way
    return redirect("login")


if __name__ == "__main__":
    app.run()
