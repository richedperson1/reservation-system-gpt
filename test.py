from db import mysql_connection


cursor = mysql_connection.get_connection()

connection = mysql_connection.get_connection()
cursor = connection.cursor(dictionary=True)

cursor.execute(
    "SELECT p.first_name, p.last_name, p.mobile_no, r.reservation_no, r.journey_date, c.class_name "
    "FROM reservations r "
    "JOIN passengers p ON r.passenger_id = p.passenger_id "
    "JOIN classes c ON r.class_id = c.class_id "
    "WHERE r.train_id = %s",
    (1,)
)
reservations = cursor.fetchall()

print(reservations)