import mysql.connector

# MySQL connection details
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # replace with your MySQL username
        password="ru15070610",  # replace with your MySQL password
        database="railway_reservation_management_price"
    )

# Fetch train names from the trains table
def fetch_trains(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT train_id, train_name FROM trains")
    return cursor.fetchall()

# Fetch class names from the classes table
def fetch_classes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT class_id, class_name FROM classes")
    return cursor.fetchall()

# Fetch station names from the stations table
def fetch_stations(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT station_id, station_name FROM stations")
    return cursor.fetchall()

# Fetch fare details
def fetch_fares(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT fare_id, train_name, class_name, start.station_name, end.station_name, price
        FROM fares
        JOIN trains ON fares.train_id = trains.train_id
        JOIN classes ON fares.class_id = classes.class_id
        JOIN stations start ON fares.start_station_id = start.station_id
        JOIN stations end ON fares.end_station_id = end.station_id
    """)
    return cursor.fetchall()

# Fetch reservation details
def fetch_reservations(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reservations.reservation_id, passengers.first_name, passengers.last_name, trains.train_name, reservations.reservation_no, reservations.journey_date
        FROM reservations
        JOIN passengers ON reservations.passenger_id = passengers.passenger_id
        JOIN trains ON reservations.train_id = trains.train_id
    """)
    return cursor.fetchall()

# Function to delete a reservation entry
def delete_reservation(conn, reservation_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservations WHERE reservation_id = %s", (reservation_id,))
    conn.commit()
    
# Function to delete a train entry
def delete_train(conn, train_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trains WHERE train_id = %s", (train_id,))
    conn.commit()

# Function to delete a station entry
def delete_station(conn, station_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stations WHERE station_id = %s", (station_id,))
    conn.commit()

# Function to delete a fare entry
def delete_fare(conn, fare_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fares WHERE fare_id = %s", (fare_id,))
    conn.commit()

# Main Streamlit app for deletion
def delete_op_app(st):
    conn = create_connection()

    st.title("Delete Railway Information")

    # Fetching available data
    trains = fetch_trains(conn)
    stations = fetch_stations(conn)
    fares = fetch_fares(conn)
    reservations = fetch_reservations(conn)
    # Choose the type of data to delete
    delete_type = st.radio("Select the type of information to delete:", ('Train', 'Station', 'Fare',"Reservation"))

    if delete_type == 'Train':
        # Dropdown to select train to delete
        train_name = st.selectbox("Select Train to Delete", [train[1] for train in trains])
        train_id = next(train[0] for train in trains if train[1] == train_name)
        
        if st.button("Delete Train"):
            delete_train(conn, train_id)
            st.success(f"Train '{train_name}' deleted successfully!")

    elif delete_type == 'Station':
        # Dropdown to select station to delete
        station_name = st.selectbox("Select Station to Delete", [station[1] for station in stations])
        station_id = next(station[0] for station in stations if station[1] == station_name)

        if st.button("Delete Station"):
            delete_station(conn, station_id)
            st.success(f"Station '{station_name}' deleted successfully!")

    elif delete_type == 'Fare':
        # Dropdown to select fare to delete based on train name, class name, and station names
        fare_details = st.selectbox(
            "Select Fare to Delete", 
            [f"{fare[1]} - {fare[2]} (From {fare[3]} to {fare[4]}, Price: {fare[5]})" for fare in fares]
        )
        fare_id = next(fare[0] for fare in fares if f"{fare[1]} - {fare[2]} (From {fare[3]} to {fare[4]}, Price: {fare[5]})" == fare_details)

        if st.button("Delete Fare"):
            delete_fare(conn, fare_id)
            st.success(f"Fare '{fare_details}' deleted successfully!")
    elif delete_type == 'Reservation':
        # Dropdown to select reservation to delete based on passenger name, train, and reservation no
        reservation_details = st.selectbox(
            "Select Reservation to Delete",
            [f"{reservation[1]} {reservation[2]} - {reservation[3]} (Reservation No: {reservation[4]}, Journey Date: {reservation[5]})"
             for reservation in reservations]
        )
        reservation_id = next(reservation[0] for reservation in reservations if
                              f"{reservation[1]} {reservation[2]} - {reservation[3]} (Reservation No: {reservation[4]}, Journey Date: {reservation[5]})" == reservation_details)

        if st.button("Delete Reservation"):
            delete_reservation(conn, reservation_id)
            st.success(f"Reservation '{reservation_details}' deleted successfully!")
    conn.close()

