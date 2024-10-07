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
    
    
    
def manage_fares1(st):
    st.header("Manage Fares for Trains")

    connection = mysql_connection.get_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch Trains and Classes
    cursor.execute("SELECT * FROM trains")
    trains = cursor.fetchall()
    train_options = {train['train_name']: train['train_id'] for train in trains}

    cursor.execute("SELECT * FROM classes")
    classes = cursor.fetchall()
    class_options = {cls['class_name']: cls['class_id'] for cls in classes}

    # Admin selects Train and Class
    train = st.selectbox("Select Train", list(train_options.keys()))
    ticket_class = st.selectbox("Select Class", list(class_options.keys()))

    # Fetch Current Fares
    train_id = train_options[train]
    class_id = class_options[ticket_class]
    
    cursor.execute(
        "SELECT fare_id, price FROM fares "
        "WHERE train_id = %s AND class_id = %s",
        (train_id, class_id)
    )
    fare_record = cursor.fetchone()
    print("fare_record =====> ",fare_record)
    if fare_record:
        # Modify Existing Fare
        st.subheader("Modify Existing Fare")
        fare_id = fare_record['fare_id']
        current_price = fare_record['price']
        new_price = st.number_input("New Price", value=float(current_price))
        
        if st.button("Update Fare"):
            cursor.execute(
                "UPDATE fares SET price = %s WHERE fare_id = %s",
                (new_price, fare_id)
            )
            connection.commit()
            st.success("Fare updated successfully.")
    else:
        # Add New Fare
        st.subheader("Add New Fare")
        price = st.number_input("Price", )

        if st.button("Add Fare"):
            cursor.execute(
                "INSERT INTO fares (train_id, class_id, price, start_station_id, end_station_id) "
                "VALUES (%s, %s, %s, NULL, NULL)",
                (train_id, class_id, price)
            )
            connection.commit()
            st.success("New fare added successfully.")

    cursor.close()





# ... (Your connection setup, import statements, etc.)

def manage_fares(st):
    try:
        connection = mysql_connection.get_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch Trains and Classes (Crucially, fetch all results!)
        cursor.execute("SELECT * FROM trains")
        trains = cursor.fetchall()
        train_options = {train['train_name']: train['train_id'] for train in trains}

        cursor.execute("SELECT * FROM classes")
        classes = cursor.fetchall()
        class_options = {cls['class_name']: cls['class_id'] for cls in classes}

        # ... (Rest of your code)  
        train = st.selectbox("Select Train", list(train_options.keys()))
        ticket_class = st.selectbox("Select Class", list(class_options.keys()))

        # Fetch Current Fares
        train_id = train_options[train]
        class_id = class_options[ticket_class]

        # Fetch Current Fares (Crucially, fetch all results!)
        cursor.execute(
            "SELECT fare_id, price FROM fares "
            "WHERE train_id = %s AND class_id = %s",
            (train_id, class_id)
        )
        fare_record = cursor.fetchone()  # Fetch result immediately
        
        # ... (Rest of your code)

        # ... (Your if/else block for adding or modifying fares)

        connection.commit() # commit only when necessary
        cursor.close()  # Close the cursor!
        # connection.close() # Close the connection!
    # except mysql.connector.Error as err:
        # Handle any database errors
        # print(f"Error: {err}")
        # Display an error message to the user
        # st.error("An error occurred while processing your request.")

    except Exception as e:
        # Handle other potential exceptions
        print(f"An unexpected error occurred: {e}")
        st.error("An unexpected error occurred.")