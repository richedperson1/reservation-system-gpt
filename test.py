from db import mysql_connection


cursor = mysql_connection.get_connection()

connection = mysql_connection.get_connection()
cursor = connection.cursor(dictionary=True)

cursor.execute(
    "SELECT DISTINCT class_name,class_id FROM classes",)
reservations = cursor.fetchall()

print(reservations)