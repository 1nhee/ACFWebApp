import pymysql

class Database():
    def __init__(self):
        self.db = pymysql.connect(host='acfwebapp.mysql.database.azure.com',
                                  user='acfwebapp@acfwebapp',
                                  db='userdb', password='HelloAC4all!20Always1', charset='utf8')
        try:
            with db.cursor() as cursor:
                sql = """
                    CREATE TABLE test_table(
                           idx  INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                           name VARCHAR(256) NOT NULL,
                           nick VARCHAR(256) NOT NULL,
                    );
                """
                cursor.execute(sql)
                db.commit()
        finally:
            db.close()

