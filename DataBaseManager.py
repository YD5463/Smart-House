import sqlite3
import bcrypt
import random
import string
import unicodedata


class DataBaseManager:
    def create_tables(self):
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS Users(username TEXT,password TEXT,email TEXT PRIMARY KEY);")
        self.__conn.commit()
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS Devices(username TEXT REFERENCES Users(email),device_name TEXT,type TEXT,status TEXT);")
        self.__conn.commit()
    def __init__(self):
        self.__conn = sqlite3.connect('MyDB.db',check_same_thread=False)
        self.__cursor = self.__conn.cursor()
        self.create_tables()

    def __del__(self):
        self.__conn.close()

    def add_device(self,email,device_name,type):
        self.__cursor.execute("INSERT INTO Devices(username,device_name,type,status) VALUES(?,?,?,?);", (email,device_name,type,"off"))
        self.__conn.commit()

    def remove_device(self,email,device_name):
        self.__cursor.execute("DELETE FROM Devices WHERE username=(?) AND device_name=(?);",(email,device_name))
        self.__conn.commit()

    def change_status(self,status,email,device_name):
        self.__cursor.execute("UPDATE Devices SET status=(?) WHERE username=(?) AND device_name=(?)",(status,email,device_name))
        self.__conn.commit()

    def get_devices_by_type(self,email,type):
        self.__cursor.execute("SELECT * FROM Devices WHERE username=(?) and type=(?)",(email,type))
        self.__conn.commit()
        results = self.__cursor.fetchall()
        dict_res = {}
        for res in results:
            try:
                dict_res.update({unicodedata.normalize('NFKD', res[1]).encode('ascii','ignore'):unicodedata.normalize('NFKD', res[3]).encode('ascii','ignore')})
            except:
                dict_res.update({})
        return dict_res

    def add_user(self,username,password,email):
        if(self.is_user_exist(email)==0):
            password = bcrypt.hashpw(password, bcrypt.gensalt())
            self.__cursor.execute("INSERT INTO Users(username,password,email) VALUES (?,?,?);", (username,password,email))
            self.__conn.commit()
            return True
        return False

    def is_user_exist(self,email):
        print(email)	
        self.__cursor.execute("SELECT * FROM Users WHERE email=(?);", (email,))
        row = self.__cursor.fetchone()
        return row!=None

    def user_is_registered(self,email,password):
        if(self.is_user_exist(email)):
            print("user is exist!")
            self.__cursor.execute("SELECT password FROM Users WHERE email=(?);", (email,))
            hashed_password = (self.__cursor.fetchone()[0])

            return (bcrypt.checkpw(password, hashed_password))

        return False

    def get_user_password(self,email):
        new_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        hashed_new_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
        self.change_password(hashed_new_password,email)
        return new_password

    def change_password(self,new_password,email):
        self.__cursor.execute("UPDATE Users SET password=(?) WHERE email=(?);", (new_password,email,))
        self.__conn.commit()

    def get_username_by_email(self,email):
        print(email)
        self.__cursor.execute("SELECT username FROM Users WHERE email=(?);",(email,))
        username = self.__cursor.fetchone()[0]
        return username

