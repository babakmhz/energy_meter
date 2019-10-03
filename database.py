import sqlite3

class db():
    connection = None
    def __init__(self):
        db_conn = sqlite3.connect('db/energymeter.sqlite')
        db_conn.execute("CREATE TABLE IF NOT EXISTS MainTable(id INTEGER PRIMARY KEY autoincrement, name TEXT,serial TEXT, UNIQUE(id,name));")
        db_conn.execute("CREATE TABLE IF NOT EXISTS Consumption(id INTEGER PRIMARY KEY AUTOINCREMENT,tag INTEGER ,date TEXT,total_time INTEGER default 0);")
        db_conn.execute("CREATE TABLE IF NOT EXISTS UpTime(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT,uptime TEXT,UNIQUE(id,date));")
        #db_conn.close()
        self.connection = db_conn
    def connect_to_db(self):
        return sqlite3.connect('db/energymeter.sqlite')

    def insertSensors(self,sensors):
        if self.connection is None:
            self.connection = self.connect_to_db()
        i = 1
        for sensor in sensors:
            self.connection.execute("insert or ignore into MainTable (id,serial,name) values(?,?,?);",(i,sensor,' vahed '+str(i),))
            self.connection.commit()
            i+=1


    def updateSensorDate(self,db_conn,sensor_id):
        pass

    def closedb(self):
        if self.connection is not None:
            self.connection.close()
            self.conection = None
    def updateUptime(self,offset,date):
        if self.connection is None:
            self.connection = self.connect_to_db()
        self.connection.execute("update UpTime set uptime = "+str(offset)+" where date like(?) ",(date,))
        self.connection.commit()
    def is_consumption_added(self,date,tag):
        if self.connection is None:
            self.connection = self.connect_to_db()
        cursor = self.connection.execute("select tag,date from Consumption where tag = ? and date = ?",(tag,date,))
        if len(cursor.fetchall())>0:
            return True
        return False
    def updateConsumeTime(self,date,total_time,tag):
        if self.connection is None:
            self.connection = self.connect_to_db()
        print('is consuption added ? : ',self.is_consumption_added(date,tag))
        if self.is_consumption_added(date,tag):
            self.connection.execute("update Consumption set total_time = total_time+"+str(total_time)+" where date = ? and tag = ?",(str(date,),str(tag),))
        else:
            self.connection.execute("insert into Consumption(date,total_time,tag) values(?,?,?)" ,(str(date),total_time,tag))
        self.connection.commit()
    def is_date_inserted(self,date):
        if self.connection is None:
            self.connection = self.connect_to_db()
        cursor = self.connection.execute("SELECT date FROM UpTime where date like (?)",(date,))
        if len(cursor.fetchall())>0:
            return True
        return False
    def insertNewUptimeDate(self,date):
        if self.connection is None:
            self.connection = self.connect_to_db()
            print('no connection!')
        if not self.is_date_inserted(date):
            cursor = self.connection.execute("insert or ignore into UpTime (date) values (?)",(date,))
            self.connection.commit()
            print('new day added, last row id is : ',cursor.lastrowid)
            return cursor.lastrowid
            #print('last inserted row id for date:',cursor.lastrowid)
            #self.connection.execute("insert or ignore into Cun")
        else:
            #return self.connection.execute("select last_insert_row_id()")
            cursor = self.connection.execute("select * from sqlite_sequence")
            index=0
            for row in cursor:
                if index==1:
                    print(row[1])
                    return row[1]
                print(row,row[1],type(row))
                index+=1
    def reportConsumption(self,date_from,date_to):
        if self.connection is None:
            self.connection = self.connect_to_db()
            print('no connection!')
        cursor = self.connection.execute("select tag,total_time from Consumption where date between '"+date_from+"'  and '"+date_to+"' ")
        rows = cursor.fetchall()
        d = dict()
        for x,y in rows:
            if x not in d:
                #print('key is not in dict adding...' , x)
                d[x] = y
            else:
                #print('key is in dict not adding...' , x)
                this_time = d[x]
                d[x] = (y)+int(this_time)
        return d
