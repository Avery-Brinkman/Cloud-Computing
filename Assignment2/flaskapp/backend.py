import bcrypt
from database import createUser, addUserInfo, getUser, getUserFromLogin
from flask import session
import jwt
import os
from User import User


# Checks matching password
def checkPassword(plaintext: str, hashed: str) -> bool:
    return bcrypt.checkpw(bytes(plaintext, "utf-8"), bytes(hashed, "utf-8"))


# Checks session info to verify user. Removes info if invalid
def verifyUser() -> bool:
    # Check for session values
    if ("id" in session) and ("jwt" in session):
        # Get user object by id
        user = getUser(session["id"])

        # Check that we got a user
        if user == None:
            removeFromSession()
            return False

        # Get jwt
        try:
            payload = jwt.decode(
                session["jwt"], os.getenv("SECRET_KEY"), algorithms=["HS256"]
            )
        except jwt.exceptions.InvalidTokenError:
            removeFromSession()
            return False

        # Check that payload has required values
        if ("id" in payload) and ("userName" in payload):
            # Check that values match the database
            valid = (payload["id"] == user.id) and (
                payload["userName"] == user.userName
            )
            if not valid:
                removeFromSession()
            return valid

    removeFromSession()
    return False


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


def userInfo(firstName: str, lastName: str, email: str):
    user = getUser(session["id"])
    if user == None:
        raise Exception(f'Could not find user {session["id"]} to add info to')
    addUserInfo(user, firstName, lastName, email)
