from database.sql import *
from database.model import *

class SQL:

    @staticmethod
    def save_coin(table_name, price, current_time):

        db = DBAccess.get_db_instance()

        result = db.session.execute("INSERT INTO " + table_name + "(price, time) VALUES('" + str(price) + "', '" + str(current_time) + "')")

        return 1

    @staticmethod
    def get_coin_price(table_name, select_time):

        from sqlalchemy import text
        db = DBAccess.get_db_instance()
        sql = text('select price from ' + table_name + ' where time >= "' + str(select_time) + '" order by id limit 1')
        result = db.session.execute(sql)
        names = []
        for row in result:
            names.append(row[0])

        return names[0]


