from db import mysql_connection
def view_available_tickets(st):
    st.header("View Available Tickets")

    connection = mysql_connection.get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM trains")
    trains = cursor.fetchall()
    train_options = {train['train_name']: train['train_id'] for train in trains}

    train = st.selectbox("Select Train", list(train_options.keys()))

    if st.button("View Availability"):
        train_id = train_options[train]
        cursor.execute(
            "SELECT c.class_name, COUNT(s.seat_id) AS available_seats "
            "FROM seats s "
            "JOIN classes c ON s.class_id = c.class_id "
            "WHERE s.train_id = %s AND s.availability_status = 'Available' "
            "GROUP BY c.class_name",
            (train_id,)
        )
        available_seats = cursor.fetchall()
        
        if available_seats:
            for seat in available_seats:
                st.success(f"{seat['class_name']} Class - Available Seats: {seat['available_seats']}")
        else:
            st.error("No available seats found for the selected train.")

    cursor.close()
    