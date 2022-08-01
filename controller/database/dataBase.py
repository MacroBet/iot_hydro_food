import pymysql.cursors


class Database:
    connection = None

    def __init__(self):
       return
    def connect_db(self):
        if self.connection is not None:
            return self.connection
        else:
            self.connection = pymysql.connect(host="localhost",
                                              user='root',
                                              password="mypass123",
                                              database="iot",
                                              cursorclass=pymysql.cursors.DictCursor)
            return self.connection