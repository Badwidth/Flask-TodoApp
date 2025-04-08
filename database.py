import sqlite3

con =  sqlite3.connect("tododb.db")
cursor = con.cursor()


cursor.execute('''CREATE TABLE users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT,
               password TEXT )''')

cursor.execute('''CREATE TABLE list (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               task TEXT,
               FOREIGN KEY (user_id) REFERENCES users(id)
               )''') 


class Db :
    
    @staticmethod
    def freshconnection():
        con =  sqlite3.connect("tododb.db")
        cur = con.cursor()
        return con, cur
    
    @staticmethod
    def getUserId(username) -> int:
        con =  sqlite3.connect("tododb.db")
        cursor = con.cursor()
        cursor.execute('''SELECT id FROM users WHERE username = :un''', {"un":username})
        uid = cursor.fetchone()[0]
        cursor.close()
        return uid
        

    @staticmethod
    def usernameDoesNotExistInDb(username) -> bool:
        con , cursor = Db.freshconnection()
        cursor.execute('''SELECT * FROM users WHERE username = :un''', {"un":username})
        huh = cursor.fetchone()
        con.close()
        return not huh


    @staticmethod
    def correctPassword(username, password) -> bool:
        con , cursor = Db.freshconnection()
        cursor.execute('''SELECT password FROM users WHERE username = :un ''', {"un":username})
        password_from_db = cursor.fetchone()[0]
        if password_from_db == password:
            con.close()
            return True
        con.close()
        return False
    
    @staticmethod
    def addUser(username, password) -> None:
        con, cursor = Db.freshconnection()
        cursor.execute('''INSERT INTO users (username, password) VALUES (:un, :pw)''', {"un": username, "pw": password})
        con.commit()
        con.close()

    @staticmethod
    def getToDoList(uid) -> list:
        con, cursor = Db.freshconnection()
        cursor.execute('''SELECT task, id FROM list WHERE user_id = :uid ''', {"uid": uid})
        result = cursor.fetchall()
        con.close()
        return result

    @staticmethod
    def addTask(task, uid) -> None:
        con, cursor = Db.freshconnection()
        cursor.execute('''INSERT INTO list (task, user_id) VALUES (:tk, :uid)''', {"tk":task, "uid":uid})
        con.commit()
        con.close

    @staticmethod
    def removeTask(task_id) -> None:
        con, cursor = Db.freshconnection()
        cursor.execute('''DELETE from list WHERE id = :tid''', {"tid":task_id})
        con.commit()
        con.close()