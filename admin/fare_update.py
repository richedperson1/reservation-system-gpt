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
    result = cursor.fetchall()
    cursor.close()
    return result

# Fetch class names from the classes table
def fetch_classes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT class_id, class_name FROM classes")
    result = cursor.fetchall()
    cursor.close()
    return result

# Fetch station names from the stations table
def fetch_stations(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT station_id, station_name FROM stations")
    result = cursor.fetchall()
    cursor.close()
    return result

# Fetch existing fares
def fetch_fares(conn):
    cursor = conn.cursor()
    query = """
    SELECT fares.fare_id, trains.train_name, classes.class_name, s1.station_name AS start_station, s2.station_name AS end_station, fares.price
    FROM fares
    JOIN trains ON fares.train_id = trains.train_id
    JOIN classes ON fares.class_id = classes.class_id
    JOIN stations s1 ON fares.start_station_id = s1.station_id
    JOIN stations s2 ON fares.end_station_id = s2.station_id
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Create a new fare in the database
def create_fare(conn, train_id, class_id, start_station_id, end_station_id, price):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fares (train_id, class_id, start_station_id, end_station_id, price)
        VALUES (%s, %s, %s, %s, %s)
    """, (train_id, class_id, start_station_id, end_station_id, price))
    conn.commit()

# Update an existing fare in the database
def update_fare(conn, fare_id, price):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE fares SET price = %s WHERE fare_id = %s
    """, (price, fare_id))
    conn.commit()

# Main Streamlit app
def fare_app(st):
    conn = create_connection()

    st.title("Add/Modify Fares for Trains")

    # Fetching dropdown data
    trains = fetch_trains(conn)
    classes = fetch_classes(conn)
    stations = fetch_stations(conn)
    fares = fetch_fares(conn)
    # admin_choice = st.selectbox('Admin Options', admin_menu)
    # Option to select operation
    operation = st.selectbox("Select Operation", ("Add New Fare", "Update Existing Fare"))

    if operation == "Add New Fare":
        st.header("Add New Fare")

        # Dropdowns for train, class, stations
        train_name = st.selectbox("Select Train", [train[1] for train in trains])
        class_name = st.selectbox("Select Class", [cls[1] for cls in classes])
        start_station_name = st.selectbox("Select Start Station", [station[1] for station in stations])
        end_station_name = st.selectbox("Select End Station", [station[1] for station in stations])

        # Price input
        price = st.number_input("Enter Fare Price", min_value=0.0, format="%.2f")

        # Finding corresponding IDs
        train_id = next(train[0] for train in trains if train[1] == train_name)
        class_id = next(cls[0] for cls in classes if cls[1] == class_name)
        start_station_id = next(station[0] for station in stations if station[1] == start_station_name)
        end_station_id = next(station[0] for station in stations if station[1] == end_station_name)

        # Button to submit
        if st.button("Add Fare"):
            create_fare(conn, train_id, class_id, start_station_id, end_station_id, price)
            st.success("Fare added successfully!")

    else:
        st.header("Update Existing Fare")

        # Create a list of fares with readable labels
        try:
            fare_options = [
                f"ID {fare[0]} : {fare[1]} - {fare[2]} Class from {fare[3]} to {fare[4]} (Price: {fare[5]})"
                for fare in fares
            ]
            selected_fare = st.selectbox("Select Fare to Update", fare_options)
            

            fare_id = int(selected_fare.split()[1])

            # Fetch the current price
            current_price = next(fare[5] for fare in fares if fare[0] == fare_id)

            # Price input
            new_price = st.number_input("Enter New Fare Price", min_value=0.0, value=float(current_price), format="%.2f")

            # Button to submit
            if st.button("Update Fare"):
                update_fare(conn, fare_id, new_price)
                st.success("Fare updated successfully!")
        except Exception as err:
            st.error(f"Error occured due to : {err}",icon="🚨")
    conn.close()


