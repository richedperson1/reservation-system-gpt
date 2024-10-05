from mysql.connector.abstracts import MySQLCursorAbstract
import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import time

# Initialize the MySQL connection with connection pooling
# @st.cache_resource
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ru15070610',
            database='railway_reservation_management',
            # pool_size=5  # Connection pool for scalability
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Fetch stations for dropdown
@st.cache_data(ttl=600)
def fetch_stations():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT station_id, station_name FROM stations")
        stations = cursor.fetchall()
        conn.close()
        return stations
    return []

# Fetch trains for dropdown
@st.cache_data(ttl=600)
def fetch_trains():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT train_id, train_name FROM trains")
        trains = cursor.fetchall()
        conn.close()
        return trains
    return []

# Fetch passengers for dropdown
@st.cache_data(ttl=600)
def fetch_passengers():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT passenger_id, CONCAT(first_name, ' ', last_name) AS full_name FROM passengers")
        passengers = cursor.fetchall()
        conn.close()
        return passengers
    return []

# Streamlit UI Layout
st.title("🚆 Railway Reservation Management System")

st.sidebar.title(body="Navigation")
page = st.sidebar.radio(label="Select a page", options=["📋 Passenger Info", "📑 Train Info", "🏙️ Station Info", "🎟️ Book Reservation"])

# Passenger Info Page
if page == "📋 Passenger Info":
    st.subheader("Passenger Information")
    
    passengers = fetch_passengers()
    selected_passenger_id = None
    if passengers:
        selected_passenger_id = st.selectbox("Select Passenger", [f"{p[1]} (ID: {p[0]})" for p in passengers])
    else:
        st.warning("No passengers available.")

    if selected_passenger_id:
        passenger_id = int(selected_passenger_id.split("(ID:")[1].split(")")[0])
        conn = create_connection()
        if conn:
            cursor: MySQLCursorAbstract  = conn.cursor()
            cursor.execute(f"SELECT * FROM passengers WHERE passenger_id = {passenger_id}")
            passenger_data = cursor.fetchone()
            print(passenger_data)
            # passenger_data = (1, 'Rutvik', '', 'Male', 1, '', '58978945634', '', datetime.datetime(2024, 10, 5, 16, 27, 55))
            if passenger_data:
                st.markdown(f"""
        **Passenger Details:**
        - **Name**: {passenger_data[1]} {passenger_data[2]}
        - **Gender**: {passenger_data[3]}
        - **Age**: {passenger_data[4]}
        - **Mobile**: {passenger_data[6]}
        - **Aadhar No**: {passenger_data[5]}
        - **Email**: {passenger_data[7]}
                """)
            conn.close()

# Train Info Page
if page == "📑 Train Info":
    st.subheader("Train Information")
    
    trains = fetch_trains()

    if trains:
        selected_train_id = st.selectbox("Select Train", [f"{t[1]} (ID: {t[0]})" for t in trains])
    else:
        st.warning("No trains available.")

    if selected_train_id:
        train_id = int(selected_train_id.split("(ID:")[1].split(")")[0])
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM trains WHERE train_id = {train_id}")
            train_data = cursor.fetchone()
            print(train_data)
            # (1, '12707', 'Hamsafar express', 'Superfast', 'Ranipat', 'Pune', datetime.timedelta(seconds=59340), datetime.timedelta(seconds=59340), 256, 1, datetime.datetime(2024, 10, 5, 16, 30, 37))
            if train_data:
                st.markdown(f"""
                **Train Details:**
                - **Train Name**: {train_data[2]}
                - **Train Number**: {train_data[1]}
                - **Type**: {train_data[3]}
                - **Start Station**: {train_data[4]}
                - **End Station**: {train_data[5]}
                - **Departure Time**: {train_data[6]}
                - **Arrival Time**: {train_data[7]}
                - **Total Seats**: {train_data[8]}
                - **Available Seats**: {train_data[9]}
                """)
            conn.close()

# Station Info Page
if page == "🏙️ Station Info":
    st.subheader("Station Information")

    stations = fetch_stations()

    if stations:
        selected_station_id = st.selectbox("Select Station", [f"{s[1]} (ID: {s[0]})" for s in stations])
    else:
        st.warning("No stations available.")

    if selected_station_id:
        station_id = int(selected_station_id.split("(ID:")[1].split(")")[0])
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM stations WHERE station_id = {station_id}")
            station_data = cursor.fetchone()
            print(station_data)
            # station_data = (1, '420', 'nashik', datetime.datetime(2024, 10, 5, 16, 29, 28))
            if station_data:
                st.markdown(f"""
        **Station Details:**
        - **Station Name**: {station_data[2]}
        - **Station Code**: {station_data[1]}
                """)
            conn.close()

# Book Reservation Page
if page == "🎟️ Book Reservation":
    st.subheader("Book a Reservation")

    passengers = fetch_passengers()
    trains = fetch_trains()
    stations = fetch_stations()

    if passengers and trains and stations:
        selected_passenger_id = st.selectbox("Select Passenger", [f"{p[1]} (ID: {p[0]})" for p in passengers])
        selected_train_id = st.selectbox("Select Train", [f"{t[1]} (ID: {t[0]})" for t in trains])
        selected_start_station = st.selectbox("Select Start Station", [f"{s[1]} (ID: {s[0]})" for s in stations])
        selected_dest_station = st.selectbox("Select Destination Station", [f"{s[1]} (ID: {s[0]})" for s in stations])
        journey_date = st.date_input("Journey Date", datetime.today())
        price = st.number_input("Price", min_value=0.0)

        if st.button("Book Reservation"):
            with st.spinner("Booking your reservation..."):
                time.sleep(1)  # Simulate processing time
                conn = create_connection()
                if conn:
                    cursor = conn.cursor()
                    passenger_id = int(selected_passenger_id.split("(ID:")[1].split(")")[0])
                    train_id = int(selected_train_id.split("(ID:")[1].split(")")[0])
                    start_station_id = int(selected_start_station.split("(ID:")[1].split(")")[0])
                    dest_station_id = int(selected_dest_station.split("(ID:")[1].split(")")[0])

                    cursor.execute("""
                        INSERT INTO reservations (passenger_id, train_id, train_start_station_id, destination_station_id, journey_date, price)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (passenger_id, train_id, start_station_id, dest_station_id, journey_date, price))
                    conn.commit()
                    conn.close()

                    st.success("Reservation successfully booked!")
    else:
        st.warning("Unable to book reservation. Please ensure passengers, trains, and stations are available.")
