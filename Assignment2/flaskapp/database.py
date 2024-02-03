import sqlite3
from typing import Any, Callable

from User import User
from UserFile import UserFile
from UserInfo import UserInfo

DATABASE_NAME = "/var/www/html/flaskapp/database.db"


def _runFunction(function: Callable, params: dict):
    con = sqlite3.connect(f"file:{DATABASE_NAME}?mode=rw", uri=True)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = 1")

    results = None
    try:
        results = function(cur, params)
    finally:
        con.commit()
        con.close()

    return results


def _convertToUser(data: tuple[int, str, str]) -> User:
    return User(data[0], data[1], data[2])


def _convertToUserInfo(user: User, data: tuple[Any, str, str, str]) -> UserInfo:
    return UserInfo(user, data[1], data[2], data[3])


def _convertToUserInfo_fullData(data: tuple[int, str, str, str, str, str]) -> UserInfo:
    return UserInfo(User(data[0], data[1], data[2]), data[3], data[4], data[5])


def _convertToUserFile(data: tuple[int, str, int]) -> UserFile:
    return UserFile(data[0], data[1], data[2])


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


def _getUser(cur: sqlite3.Cursor, params: dict) -> User | None:
    result = cur.execute("SELECT * FROM users WHERE id=:id", params).fetchone()
    if result == None:
        return None
    return _convertToUser(result)


def _getUserInfo(cur: sqlite3.Cursor, params: dict) -> UserInfo | None:
    result = cur.execute(
        """SELECT users.id, users.userName, users.password, userInfo.firstname, userInfo.lastName, userInfo.email 
                                FROM userInfo 
                                INNER JOIN users ON users.id=userInfo.id WHERE userInfo.id=:id""",
        params,
    ).fetchone()

    if result == None:
        return None
    return _convertToUserInfo_fullData(result)


def _getUserFromLogin(cur: sqlite3.Cursor, params: dict) -> User | None:
    result = cur.execute(
        "SELECT * FROM users WHERE userName=:userName", params
    ).fetchone()

    if result == None:
        return None
    return _convertToUser(result)


def _getUserFiles(cur: sqlite3.Cursor, params: dict) -> list[UserFile]:
    # Get users files
    result = cur.execute(
        "SELECT * FROM files WHERE uploaderId=:uploaderId", params
    ).fetchall()

    fileList: list[UserFile] = []
    for file in result:
        fileList.append(_convertToUserFile(file))

    return fileList


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


def getUser(id: int) -> User | None:
    params = {"id": id}
    return _runFunction(_getUser, params)


def getUserInfo(id: int) -> UserInfo | None:
    params = {"id": id}
    return _runFunction(_getUserInfo, params)


def getUserFromLogin(userName: str) -> User | None:
    params = {"userName": userName}
    return _runFunction(_getUserFromLogin, params)


def getUserFiles(userId: int) -> list[UserFile]:
    params = {"uploaderId": userId}
    return _runFunction(_getUserFiles, params)
