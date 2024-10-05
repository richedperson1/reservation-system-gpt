import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Initialize the MySQL connection with pooling
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ru15070610',
            database='railway_reservation_management',
            pool_size=5  
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Streamlit sidebar for navigation
st.sidebar.title("Railway Reservation System")
page = st.sidebar.selectbox("Navigate", ["Passenger Management", "Reservation Management", "Train Management", "Station Management"])

# Passenger Management
if page == "Passenger Management":
    st.title("Passenger Management")
    
    def add_passenger():
        st.subheader("Add New Passenger")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=1, max_value=100)
        mobile_no = st.text_input("Mobile No")
        aadhar_no = st.text_input("Aadhar No")
        email = st.text_input("Email")

        if st.button("Add Passenger"):
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO passengers (first_name, last_name, gender, age, mobile_no, aadhar_no, email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (first_name, last_name, gender, age, mobile_no, aadhar_no, email))
                conn.commit()
                conn.close()
                st.success("Passenger added successfully!")

    def view_passengers():
        st.subheader("View Passengers")
        conn = create_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM passengers")
            data = cursor.fetchall()
            if data:
                st.table(data)
            else:
                st.warning("No passengers found.")
            conn.close()

    # UI Options
    action = st.radio("Action", ["Add Passenger", "View Passengers"])
    if action == "Add Passenger":
        add_passenger()
    elif action == "View Passengers":
        view_passengers()

# Reservation Management
if page == "Reservation Management":
    st.title("Reservation Management")

    def book_reservation():
        st.subheader("Book Reservation")
        passenger_id = st.text_input("Passenger ID")
        train_id = st.text_input("Train ID")
        start_station = st.text_input("Start Station")
        destination_station = st.text_input("Destination Station")
        journey_date = st.date_input("Journey Date")
        price = st.number_input("Price", min_value=0.0)

        if st.button("Book Reservation"):
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO reservations (passenger_id, train_id, train_start_station_id, destination_station_id, journey_date, price)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (passenger_id, train_id, start_station, destination_station, journey_date, price))
                conn.commit()
                conn.close()
                st.success("Reservation booked successfully!")

    def view_reservations():
        st.subheader("View Reservations")
        conn = create_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM reservations")
            data = cursor.fetchall()
            if data:
                st.table(data)
            else:
                st.warning("No reservations found.")
            conn.close()

    # UI Options
    action = st.radio("Action", ["Book Reservation", "View Reservations"])
    if action == "Book Reservation":
        book_reservation()
    elif action == "View Reservations":
        view_reservations()

# Train Management
if page == "Train Management":
    st.title("Train Management")

    def add_train():
        st.subheader("Add New Train")
        train_no = st.text_input("Train Number")
        train_name = st.text_input("Train Name")
        train_type = st.selectbox("Train Type", ["Passenger", "Express", "Superfast"])
        start_station = st.text_input("Start Station")
        end_station = st.text_input("End Station")
        departure_time = st.time_input("Departure Time")
        arrival_time = st.time_input("Arrival Time")
        total_seats = st.number_input("Total Seats", min_value=1)
        available_seats = st.number_input("Available Seats", min_value=1)

        if st.button("Add Train"):
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO trains (train_no, train_name, train_type, start_station, end_station, departure_time, arrival_time, total_seats, available_seats)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (train_no, train_name, train_type, start_station, end_station, departure_time, arrival_time, total_seats, available_seats))
                conn.commit()
                conn.close()
                st.success("Train added successfully!")

    # UI Options
    add_train()

# Station Management
if page == "Station Management":
    st.title("Station Management")
    
    def add_station():
        st.subheader("Add New Station")
        station_code = st.text_input("Station Code")
        station_name = st.text_input("Station Name")

        if st.button("Add Station"):
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO stations (station_code, station_name)
                    VALUES (%s, %s)
                """, (station_code, station_name))
                conn.commit()
                conn.close()
                st.success("Station added successfully!")

    add_station()
