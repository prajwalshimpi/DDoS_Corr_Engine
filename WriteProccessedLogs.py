from MySQLConnection import *
class WriteProcessedLog:
    db = None
    cursor = None
    connection = None

    def __init__(self):
        self.db = MySQLConnection()
        self.cursor = self.db.getCursor()
        self.connection = self.db.getConnection()

    def writeLogs(self,ip, port, loc_country, zip, protocol, ts, times, is_attack):
        q = "insert into processed_data(ip,port,loc_country,zip,protocol,ts,times,is_attack)VALUES('{}',{},'{}','{}','{}','{}',{},{})".format(ip, port, loc_country, zip, protocol, ts, times, is_attack)
        self.insertSQL(q)

    def insertSQL(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            print("Oops! Somthing happend while updating to database...\n"+sys.exc_traceback()[0])
            self.connection.rollback()

    def __del__(self):
        del self.db