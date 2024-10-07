import streamlit as st
import mysql.connector
from datetime import date
from mysql.connector import Error

# Database connection setup
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ru15070610",
        database="railway_reservation_management_price"
    )

# Helper function to check admin
def is_admin(user_role):
    return user_role == 'admin'

# Home Page (Public)
def home_page():
    st.title("Railway Reservation System")
    st.subheader("Book Your Tickets")
    st.text("Select your train, starting station, and destination to reserve your ticket.")

    # Fetch available trains, stations, and classes
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM stations")
    stations = cursor.fetchall()
    station_options = {station['station_name']: station['station_id'] for station in stations}

    cursor.execute("SELECT * FROM trains")
    trains = cursor.fetchall()
    train_options = {train['train_name']: train['train_id'] for train in trains}

    cursor.execute("SELECT * FROM classes")
    classes = cursor.fetchall()
    class_options = {cls['class_name']: cls['class_id'] for cls in classes}

    # Form to select options for booking
    train = st.selectbox("Select Train", list(train_options.keys()))
    start_station = st.selectbox("Select Start Station", list(station_options.keys()))
    destination_station = st.selectbox("Select Destination Station", list(station_options.keys()))
    ticket_class = st.selectbox("Select Class", list(class_options.keys()))
    journey_date = st.date_input("Journey Date", min_value=date.today())

    if st.button("Check Availability & Price"):
        # Fetch price and availability
        train_id = train_options[train]
        class_id = class_options[ticket_class]
        start_station_id = station_options[start_station]
        end_station_id = station_options[destination_station]

        cursor.execute(
            "SELECT price FROM fares WHERE train_id=%s AND class_id=%s AND start_station_id=%s AND end_station_id=%s",
            (train_id, class_id, start_station_id, end_station_id)
        )
        fare = cursor.fetchone()
        
        if fare:
            st.success(f"Ticket Price: ₹{fare['price']}")
            # Check seat availability
            cursor.execute(
                "SELECT COUNT(*) AS available_seats FROM seats WHERE train_id=%s AND class_id=%s AND availability_status='Available'",
                (train_id, class_id)
            )
            seats = cursor.fetchone()
            if seats['available_seats'] > 0:
                st.success(f"Seats Available: {seats['available_seats']}")
                if st.button("Reserve Ticket"):
                    st.write("Ticket reservation process will go here.")
            else:
                st.error("No seats available.")
        else:
            st.error("Price not found for the selected route.")

    cursor.close()
    

# Admin Panel (Admin only)
def admin_panel():
    st.title("Admin Panel")
    st.subheader("Manage Trains, Stations, and Ticket Classes")
    
    admin_task = st.selectbox("Select Task", ["Add Train", "Add Station", "Add Ticket Class"])
    
    if admin_task == "Add Train":
        add_train()
    elif admin_task == "Add Station":
        add_station()
    elif admin_task == "Add Ticket Class":
        add_ticket_class()

def add_train():
    st.header("Add New Train")
    train_no = st.text_input("Train Number")
    train_name = st.text_input("Train Name")
    train_type = st.selectbox("Train Type", ["Passenger", "Express", "Superfast"])
    total_seats = st.number_input("Total Seats", min_value=1)

    if st.button("Add Train"):
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO trains (train_no, train_name, train_type, total_seats) VALUES (%s, %s, %s, %s)",
            (train_no, train_name, train_type, total_seats)
        )
        connection.commit()
        st.success("Train added successfully.")
        cursor.close()
        

def add_station():
    st.header("Add New Station")
    station_code = st.text_input("Station Code")
    station_name = st.text_input("Station Name")
    city = st.text_input("City")
    state = st.text_input("State")

    if st.button("Add Station"):
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO stations (station_code, station_name, city, state) VALUES (%s, %s, %s, %s)",
            (station_code, station_name, city, state)
        )
        connection.commit()
        st.success("Station added successfully.")
        cursor.close()
        

def add_ticket_class():
    st.header("Add New Ticket Class")
    class_name = st.selectbox("Class Name", ["Sleeper", "AC", "General"])

    if st.button("Add Ticket Class"):
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO classes (class_name) VALUES (%s)", (class_name,)
        )
        connection.commit()
        st.success("Ticket class added successfully.")
        cursor.close()
        

# Main Streamlit Application Flow
def main():
    st.sidebar.title("Railway Reservation System")
    user_role = st.sidebar.selectbox("Login As", ["User", "Admin"])

    if user_role == "Admin":
        st.sidebar.write("Logged in as Admin")
        admin_panel()
    else:
        home_page()

if __name__ == "__main__":
    main()
