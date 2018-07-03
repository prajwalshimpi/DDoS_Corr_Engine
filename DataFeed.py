# import the MySQLdb and sys modules

import time
from MySQLConnection import *
from WriteProccessedLogs import *
# open a database connection
wpl = WriteProcessedLog()
db = MySQLConnection()

# prepare a cursor object using cursor() method
cursor = db.getCursor()

# execute query to get all the data from database
try:
    cursor.execute("select DISTINCT ts from corr")
except:
    print("Couldn't Connect to MySQLdb")
    time.sleep(5)
    raise

# fetch all of the rows from the query
data = cursor.fetchall()
#data = cursor.fetchmany(10)

# print the rows
if data == 0:
    exit()

for time in data:
    print("Time : " + str(time[0]))
    p = "select * from corr where ts=\'" + str(time[0]) + "\'"
    # cursor.execute("select * from corr where ts="+str(time[0]))
    cursor.execute(str(p))

    log = cursor.fetchall()
    le = 0
    cunt = 1
    for row in log:
        cunt+=1
        if le == 0:
            dict = {str(le): {'IP': str(row[1]), 'P': 'HTTP', 'T': 1, 'LOC': str(row[2]),'zip':str(row[3]),'port':80}}
            le += 1
            continue
        else:
            for n in range(0, (len(dict))):
                no = str(n)
                if dict[no]['IP'] == str(row[1]):
                    if dict[no]['P'] == 'HTTP':
                        dict[no]['T'] += 1
                        continue
                temp = {'IP': str(row[1]), 'P': 'HTTP', 'T': 1, 'LOC': str(row[2]),'zip':str(row[3]),'port':80}
                dict.setdefault(str(le), temp)
                le += 1
    for n in range(0, le):
        pos = str(n)
        if dict[str(n)]['T'] > 15 :
            wpl.writeLogs(dict[pos]['IP'],dict[pos]['port'],dict[pos]['LOC'],dict[pos]['zip'],dict[pos]['P'],str(time[0]),dict[pos]['T'],str(1))
            print(" \t " + str(dict[pos]))
        else:
            wpl.writeLogs(dict[pos]['IP'], dict[pos]['port'], dict[pos]['LOC'], dict[pos]['zip'],dict[pos]['P'], str(time[0]), dict[pos]['T'], str(0))
            print(" \t " + str(dict[pos]))
    dict = {}

# closing MySQLConnection obj cursor
del cursor
sys.exit()
