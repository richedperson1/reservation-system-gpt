
from db import mysql_connection

def view_reservations(st):
    st.header("View Reservations for a Train")

    connection = mysql_connection.get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM trains")
    trains = cursor.fetchall()
    train_options = {train['train_name']: train['train_id'] for train in trains}

    train = st.selectbox("Select Train", list(train_options.keys()))

    if st.button("View Reservations"):
        train_id = train_options[train]
        cursor.execute(
            "SELECT p.first_name, p.last_name, p.mobile_no, r.reservation_no, r.journey_date, c.class_name "
            "FROM reservations r "
            "JOIN passengers p ON r.passenger_id = p.passenger_id "
            "JOIN classes c ON r.class_id = c.class_id "
            "WHERE r.train_id = %s",
            (train_id,)
        )
        reservations = cursor.fetchall()
        
        if reservations:
            for res in reservations:
                st.write(f"Reservation No: {res['reservation_no']}, Passenger: {res['first_name']} {res['last_name']}, "
                         f"Mobile: {res['mobile_no']}, Class: {res['class_name']}, Journey Date: {res['journey_date']}")
        else:
            st.error("No reservations found for the selected train.")

    cursor.close()
