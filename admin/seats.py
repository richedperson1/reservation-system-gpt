from db import mysql_connection
def increase_seats_in_train(st):
    st.header("Increase Seats in Train")

    connection = mysql_connection.get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM trains")
    trains = cursor.fetchall()
    train_options = {train['train_name']: train['train_id'] for train in trains}

    cursor.execute("SELECT * FROM classes")
    classes = cursor.fetchall()
    class_options = {cls['class_name']: cls['class_id'] for cls in classes}

    train = st.selectbox("Select Train", list(train_options.keys()))
    ticket_class = st.selectbox("Select Class", list(class_options.keys()))
    num_new_seats = st.number_input("Number of Additional Seats", min_value=1)

    if st.button("Add Seats"):
        train_id = train_options[train]
        class_id = class_options[ticket_class]

        # Add new seats to the selected class
        for i in range(num_new_seats):
            seat_no = f"{ticket_class[:3].upper()}-{i+1}"  # Example: AC-1, SL-1
            cursor.execute(
                "INSERT INTO seats (train_id, seat_no, class_id, availability_status) "
                "VALUES (%s, %s, %s, 'Available')",
                (train_id, seat_no, class_id)
            )

        connection.commit()
        st.success(f"Added {num_new_seats} new seats to {ticket_class} class in {train}.")

    cursor.close()
    
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


