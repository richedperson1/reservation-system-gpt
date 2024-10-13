
import mysql.connector


class mysql_connection:
    # _INSTANCE = None
    @classmethod
    def get_connection(cls):
        _INSTANCE = mysql.connector.connect(host="localhost",user="root",password="ru15070610",database="railway_reservation_management_price")
        
        return _INSTANCE
    

def fetch_all_operation(query,value):
    
    connection = mysql_connection.get_connection()
    
    if connection:
        
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(query,value)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

def fetch_one_operation(query,value):
    
    connection = mysql_connection.get_connection()
    
    if connection:
        
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(query,value)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

def query_fetch_one_operation(query):
    
    connection = mysql_connection.get_connection()
    
    if connection:
        
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

def query_fetch_all_operation(query):
    
    connection = mysql_connection.get_connection()
    
    if connection:
        
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

def commit_operation(query,value):
    
    connection = mysql_connection.get_connection()
    
    if connection:
        
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(query,value)
        connection.commit()
        cursor.close()
        connection.close()
        return "Done"   

def commit_cursor_operation(query,value):
    
    connection = mysql_connection.get_connection()
    
    if connection:
        
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(query,value)
        connection.commit()
        # cursor.close()
        # connection.close()
        return cursor ,connection
 
    
