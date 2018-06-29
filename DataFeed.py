# import the MySQLdb and sys modules
import MySQLdb
import sys

# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
connection = MySQLdb.connect(host="localhost", port=3308, user="root", passwd="admin", db="core_engine")

# prepare a cursor object using cursor() method
cursor = connection.cursor()

# execute the SQL query using execute() method.
cursor.execute("select DISTINCT ts from corr where pk>16")

# fetch all of the rows from the query
data = cursor.fetchall()

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
            dict = {str(le): {'IP': str(row[1]), 'P': 'HTTP', 'T': 1, 'LOC': str(row[2])}}
            le += 1
            continue
        else:
            for n in range(0, (len(dict))):
                if dict[str(n)]['IP'] == str(row[1]):
                    if dict[str(n)]['P'] == 'HTTP':
                        dict[str(n)]['T'] += 1
                        continue
                temp = {'IP': str(row[1]), 'P': 'HTTP', 'T': 1, 'LOC': str(row[2])}
                dict.setdefault(str(le), temp)
                le += 1
    for n in range(0, le):
        if dict[str(n)]['T'] > 15 :
            print(" \t " + str(dict[str(n)]))
        else:
            print(" \t No Sign of Attack")
    dict = {}
# close the cursor object
cursor.close()

# close the connection
connection.close()

# exit the program
sys.exit()
