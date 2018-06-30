import MySQLdb
import sys

class MySQLConnection:

    connection = None
    cursor = None
    def __init__(self):
        try:
            self.connection = self.initConnection()
            self.cursor = self.initCursor()
        except:
            print("Unexpected error While Initializing Database Connection:", sys.exc_info())

    def initConnection(self):
        con = MySQLdb.connect(host="localhost", port=3308, user="root", passwd="admin", db="core_engine")
        return con
    def initCursor(self):
        cur = self.connection.cursor()
        return cur

    def getConnection(self):
        return self.connection
    def getCursor(self):
        return self.cursor

    def __del__(self):
        self.cursor.close()
        self.connection.close()




