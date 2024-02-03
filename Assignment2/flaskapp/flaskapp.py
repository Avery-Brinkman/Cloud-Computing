from backend import login, readFile, removeFromSession, signup, verifyUser
from create_database import create_database
from database import addUserInfo, getFile, getUserFiles, getUserInfo
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request
import os

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
    return render_template("index.html", loggedIn=(verifyUser() != None))


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    # If we're already logged in, redirect
    if verifyUser() != None:
        return redirect("/me")

    if request.method == "POST":
        user = signup(
            request.form["user_name"],
            request.form["pswrd"],
            request.form["c_pswrd"],
        )
        # Succesfully created account
        if user != None:
            return redirect("/signup/info")

    return render_template("signup.html")


@app.route("/signup/info", methods=["GET", "POST"])
def signup_info_page():
    # Check that user is logged in
    user = verifyUser()
    if user == None:
        return redirect("/signup")

    if request.method == "POST":
        # Add the user info
        addUserInfo(
            user,
            request.form["firstName"],
            request.form["lastName"],
            request.form["email"],
        )
        # Show info
        return redirect("/me")

    # GET req for logged in user (to enter info)
    return render_template("info.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        # Try to login
        user = login(request.form["user_name"], request.form["pswrd"])
        if user != None:
            # Check if info needs to be added
            if getUserInfo(user.id) == None:
                return redirect("/signup/info")

            # Otherwise go to homepage
            return redirect("/")

    return render_template("login.html")


@app.route("/me")
def me_page():
    # Check that user is logged in
    user = verifyUser()
    if user == None:
        # Redirect to login
        return redirect("/login")

    # Get their info
    userInfo = getUserInfo(user.id)

    # Check that we have info
    if userInfo == None:
        # Redirect to enter info if missing
        return redirect("/signup/info")

    # Show page w user info
    return render_template(
        "me.html",
        userName=user.userName,
        firstName=userInfo.firstName,
        lastName=userInfo.lastName,
        email=userInfo.email,
    )


@app.route("/files")
def files_page():
    # Check that user is logged in
    user = verifyUser()
    if user == None:
        return redirect("/")

    # Get users files
    fileList = []
    for file in getUserFiles(user.id):
        fileList.append({"id": file.id, "name": file.fileName})

    return render_template("userFiles.html", userName=user.userName, fileList=fileList)


@app.route("/files/<int:fileId>")
def user_file_page(fileId: int):
    # Check that user is logged in
    user = verifyUser()
    if user == None:
        return redirect("/")

    # Get the file
    file = getFile(fileId)
    # Check that file exists and that user owns it
    if (file == None) or (user.id != file.uploader):
        # File doesn't exist (treat not owner as not existing)
        return render_template("file.html")

    # Try to read the contents
    contents = readFile(ROOT + "/userFiles/" + file.fileName)
    if contents == None:
        # Can't read file
        return render_template("file.html", fileName=file.fileName)

    # Everything worked
    wordCount = len(contents.split())
    return render_template(
        "file.html",
        fileContents=contents,
        fileName=file.fileName,
        wordCount=wordCount,
    )


@app.route("/signout")
def signout():
    removeFromSession()
    return redirect("/")


if __name__ == "__main__":
    app.run()
