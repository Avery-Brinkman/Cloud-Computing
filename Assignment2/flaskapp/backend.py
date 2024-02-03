import os
import bcrypt
from database import createUser, addUserInfo, getUser, getUserFromLogin
from flask import session
import jwt
from User import User


# Checks matching password
def checkPassword(plaintext: str, hashed: str) -> bool:
    return bcrypt.checkpw(bytes(plaintext, "utf-8"), bytes(hashed, "utf-8"))


# Checks session info to verify user
def verifyUser() -> bool:
    # Check for session values
    if "id" in session and "jwt" in session:
        # Get user object by id
        user = getUser(session["id"])

        # Check that we got a user
        if user == None:
            return False

        # Get jwt
        try:
            payload = jwt.decode(session["jwt"], os.getenv("SECRET_KEY"))
        except jwt.exceptions.InvalidTokenError:
            return False

        # Check that payload has required values
        if "id" in payload and "userName" in payload:
            # Check that values match the database
            return payload["id"] == user.id and payload["userName"] == user.userName

    return False


# Adds User info to session
def addToSession(user: User):
    session["id"] = user.id
    payload = {"id": user.id, "userName": user.userName}
    session["jwt"] = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")


# Checks user credentials, and adds info to session if valid
def login(userName: str, password: str) -> bool:
    # Get user info
    user = getUserFromLogin(userName)

    # Check that we got a user
    if user == None:
        return False

    # Check password
    if checkPassword(password, user.password):
        # Set session data
        addToSession(user)

        return True

    return False


def signup(userName: str, password: str, confirmPassword: str):
    if password != confirmPassword:
        return False

    # Hash password
    passHash = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())
    # Create user and add to database
    user = createUser(userName, passHash.decode("utf-8"))

    if user == None:
        return False

    # Add session info
    addToSession(user)

    return True


def userInfo(firstName: str, lastName: str, email: str):
    user = getUser(session["id"])
    if user == None:
        return
    addUserInfo(user, firstName, lastName, email)
