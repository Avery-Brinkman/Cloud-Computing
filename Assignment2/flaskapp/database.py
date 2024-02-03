import sqlite3
from typing import Callable

from User import User
from UserInfo import UserInfo

DATABASE_NAME = "/var/www/html/flaskapp/database.db"


def _runFunction(function: Callable, params: dict):
    con = sqlite3.connect(f"file:{DATABASE_NAME}?mode=rw", uri=True)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = 1")

    results = function(cur, params)

    con.commit()
    con.close()

    return results


def _convertToUser(data: tuple) -> User:
    return User(data[0], data[1], data[2])


def _convertToUserInfo(user: User, data: tuple) -> UserInfo:
    return UserInfo(user, data[1], data[2], data[3])


def _convertToUserInfo_fullData(data: tuple) -> UserInfo:
    return UserInfo(User(data[0], data[1], data[2]), data[3], data[4], data[5])


def _createUser(cur: sqlite3.Cursor, params: dict) -> User:
    # Add row
    cur.execute(
        "INSERT INTO users (userName, password) VALUES (:userName, :password)",
        params,
    )
    # Get data
    result = cur.execute(
        "SELECT * FROM users WHERE rowid=?", (cur.lastrowid,)
    ).fetchone()
    # Return new User
    return _convertToUser(result)


def _addUserInfo(cur: sqlite3.Cursor, params: dict) -> UserInfo:
    # Add row
    cur.execute(
        "INSERT INTO userInfo (id, firstName, lastName, email) VALUES (:id, :firstName, :lastName, :email)",
        params,
    )
    # Get data
    result = cur.execute(
        "SELECT * FROM userInfo WHERE rowid=?", (cur.lastrowid,)
    ).fetchone()
    return _convertToUserInfo(params["user"], result)


def _getUser(cur: sqlite3.Cursor, params: dict) -> User:
    result = cur.execute("SELECT * FROM users WHERE id=:id", params).fetchone()
    return _convertToUser(result)


def _getUserInfo(cur: sqlite3.Cursor, params: dict) -> UserInfo:
    result = cur.execute(
        """SELECT users.id, users.userName, users.password, userInfo.firstname, userInfo.lastName, userInfo.email 
                                FROM userInfo 
                                INNER JOIN users ON users.id=userInfo.id WHERE userInfo.id=:id""",
        params,
    ).fetchone()
    return _convertToUserInfo_fullData(result)


def _getUserFromLogin(cur: sqlite3.Cursor, params: dict) -> User:
    result = cur.execute(
        "SELECT * FROM users WHERE userName=:userName", params
    ).fetchone()
    return _convertToUser(result)


def createUser(userName: str, passwordHash: str) -> User:
    params = {"userName": userName, "password": passwordHash}
    return _runFunction(_createUser, params)


def addUserInfo(user: User, firstName: str, lastName: str, email: str) -> UserInfo:
    params = {
        "id": user.id,
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "user": user,
    }
    return _runFunction(_addUserInfo, params)


def getUser(id: int) -> User:
    params = {"id": id}
    return _runFunction(_getUser, params)


def getUserInfo(id: int) -> UserInfo:
    params = {"id": id}
    return _runFunction(_getUserInfo, params)


def getUserFromLogin(userName: str) -> User:
    params = {"userName": userName}
    return _runFunction(_getUserFromLogin, params)
