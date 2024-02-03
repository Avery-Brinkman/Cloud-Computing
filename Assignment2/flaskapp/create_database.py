import sqlite3


def cleanDB(cur):
    cur.execute("""DROP TABLE IF EXISTS files""")
    cur.execute("""DROP TABLE IF EXISTS userInfo""")
    cur.execute("""DROP TABLE IF EXISTS users""")


def createUsersTable(cur):
    cur.execute(
        """CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        userName VARCHAR UNIQUE,
        password VARCHAR
    )"""
    )


def createUserInfoTable(cur):
    cur.execute(
        """CREATE TABLE userInfo (
        id INTEGER UNIQUE,
        firstName VARCHAR,
        lastName VARCHAR,
        email VARCHAR,
        FOREIGN KEY(id) REFERENCES users(id)
    )"""
    )


def createFilesTable(cur):
    cur.execute(
        """CREATE TABLE files (
        id INTEGER PRIMARY KEY,
        fileName VARCHAR,
        uploaderId INTEGER,
        FOREIGN KEY(uploaderId) REFERENCES users(id)
    )"""
    )


def create_database():
    con = sqlite3.connect("file:/var/www/html/flaskapp/database.db?mode=rwc", uri=True)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = 1")

    cleanDB(cur)

    createUsersTable(cur)
    createUserInfoTable(cur)
    createFilesTable(cur)

    con.commit()
    con.close()
