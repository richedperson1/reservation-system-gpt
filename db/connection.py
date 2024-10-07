
import mysql.connector


class mysql_connection:
    _INSTANCE = None
    @classmethod
    def get_connection(cls):
        if cls._INSTANCE:
            return cls._INSTANCE
        
        cls._INSTANCE = mysql.connector.connect(host="localhost",user="root",password="ru15070610",database="railway_reservation_management_price")
        
        return cls._INSTANCE