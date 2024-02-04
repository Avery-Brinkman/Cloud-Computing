import bcrypt
from database import createUser, getUser, getUserFromLogin, storeFile
from flask import session
import jwt
import os
from User import User
from UserFile import UserFile
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"txt", "png", "jpg", "jpeg", "gif"}


# Checks matching password
def checkPassword(plaintext: str, hashed: str) -> bool:
    return bcrypt.checkpw(bytes(plaintext, "utf-8"), bytes(hashed, "utf-8"))


# Checks session info to verify user. Removes info if invalid
def verifyUser() -> User | None:
    # Check for session values
    if ("id" in session) and ("jwt" in session):
        # Get user object by id
        user = getUser(session["id"])

        # Check that we got a user
        if user != None:
            # Get jwt
            try:
                payload = jwt.decode(
                    session["jwt"], os.getenv("SECRET_KEY"), algorithms=["HS256"]
                )
            except jwt.exceptions.InvalidTokenError:
                removeFromSession()
                return None

            # Check that payload has required values
            if ("id" in payload) and ("userName" in payload):
                # Check that values match the database
                if (payload["id"] == user.id) and (
                    payload["userName"] == user.userName
                ):
                    return user

    removeFromSession()
    return None


# Adds User info to session
def addToSession(user: User):
    session["id"] = user.id
    payload = {"id": user.id, "userName": user.userName}
    session["jwt"] = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")


# Removes session values
def removeFromSession():
    session.pop("id", None)
    session.pop("jwt", None)


# Checks user credentials and returns user (or none on invalid creds)
def login(userName: str, password: str) -> User | None:
    # Get user info
    user = getUserFromLogin(userName)

    # Check that we got a user with valid password
    if (user != None) and checkPassword(password, user.password):
        # Log user in if successful
        addToSession(user)
        return user

    return None


# Creates new user, and returns created user
def signup(userName: str, password: str, confirmPassword: str) -> User | None:
    if password != confirmPassword:
        return None

    # Hash password
    passHash = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())
    # Create user and add to database
    user = createUser(userName, passHash.decode("utf-8"))

    # Log user in if successful
    if user != None:
        addToSession(user)

    return user


# Get file contents as string (or None on error)
def readFile(fileName: str) -> str | None:
    try:
        file = open(fileName, "r")
        contents = file.read()
        file.close()
    except:
        contents = None

    return contents


def allowedFile(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def uploadFile(user: User, reqFile: FileStorage, saveLocation: str) -> UserFile | None:
    if reqFile.filename == None:
        return None
    secureFileName = secure_filename(reqFile.filename)

    file = storeFile(user, secureFileName)
    if file == None:
        return None

    reqFile.save(os.path.join(saveLocation, file.localName))
    return file
