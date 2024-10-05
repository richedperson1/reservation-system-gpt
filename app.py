import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import time

# Database Connection
# @st.cache_resource
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ru15070610',
            database='railway_reservation_management',
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Fetch data from MySQL
@st.cache_data(ttl=600)
def fetch_data(query):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data
    return []

# Search functionality for stations and trains
def search_entity(entity, search_term):
    query = f"SELECT * FROM {entity} WHERE {entity}_name LIKE '%{search_term}%'"
    return fetch_data(query)

# Add new entity to the database
def add_entity(entity, columns, values):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = f"INSERT INTO {entity} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(values))})"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        st.success(f"New {entity[:-1]} added successfully!")

# Passenger Information Page
def passenger_info():
    st.subheader("Passenger Information")
    
    passengers = fetch_data("SELECT passenger_id, CONCAT(first_name, ' ', last_name) AS full_name FROM passengers")
    if passengers:
        selected_passenger_id = st.selectbox("Select Passenger", [f"{p[1]} (ID: {p[0]})" for p in passengers])
        if selected_passenger_id:
            passenger_id = int(selected_passenger_id.split("(ID:")[1].split(")")[0])
            passenger_data = fetch_data(f"SELECT * FROM passengers WHERE passenger_id = {passenger_id}")[0]
            with st.expander("Passenger Details"):
                st.markdown(f"""
                    - **Name**: {passenger_data[1]} {passenger_data[2]}
                    - **Gender**: {passenger_data[3]}
                    - **Age**: {passenger_data[4]}
                    - **Mobile**: {passenger_data[6]}
                    - **Aadhar No**: {passenger_data[5]}
                    - **Email**: {passenger_data[7]}
                """)
    else:
        st.warning("No passengers available.")

# Add new passenger
def add_passenger():
    st.subheader("Add New Passenger")
    with st.form("passenger_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=1, max_value=120)
        aadhar = st.text_input("Aadhar Number")
        mobile = st.text_input("Mobile Number")
        email = st.text_input("Email")
        
        if st.form_submit_button("Add Passenger"):
            add_entity(entity="passengers", columns=["first_name", "last_name", "gender", "age", "aadhar", "mobile", "email"], 
                       values=[first_name, last_name, gender, age, aadhar, mobile, email])

# Train Information Page
def train_info():
    st.subheader("Train Information")
    
    search_term = st.text_input("Search Train by Name")
    if search_term:
        trains = search_entity("train", search_term)
    else:
        trains = fetch_data("SELECT train_id, train_name FROM trains")

    if trains:
        selected_train_id = st.selectbox("Select Train", [f"{t[1]} (ID: {t[0]})" for t in trains])
        if selected_train_id:
            train_id = int(selected_train_id.split("(ID:")[1].split(")")[0])
            train_data = fetch_data(f"SELECT * FROM trains WHERE train_id = {train_id}")[0]
            with st.expander("Train Details"):
                st.markdown(f"""
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
    else:
        st.warning("No trains available.")

# Add new train
def add_train():
    st.subheader("Add New Train")
    with st.form("train_form"):
        train_name = st.text_input("Train Name")
        train_number = st.text_input("Train Number")
        train_type = st.text_input("Type (e.g. Express, Local)")
        start_station = st.text_input("Start Station")
        end_station = st.text_input("End Station")
        departure_time = st.time_input("Departure Time")
        arrival_time = st.time_input("Arrival Time")
        total_seats = st.number_input("Total Seats", min_value=1)
        available_seats = st.number_input("Available Seats", min_value=0)
        
        if st.form_submit_button("Add Train"):
            add_entity("trains", ["train_name", "train_number", "type", "start_station", "end_station", "departure_time", "arrival_time", "total_seats", "available_seats"],
                       [train_name, train_number, train_type, start_station, end_station, departure_time, arrival_time, total_seats, available_seats])

# Station Information Page
def station_info():
    st.subheader("Station Information")
    
    search_term = st.text_input("Search Station by Name")
    if search_term:
        stations = search_entity("station", search_term)
    else:
        stations = fetch_data("SELECT station_id, station_name FROM stations")

    if stations:
        selected_station_id = st.selectbox("Select Station", [f"{s[1]} (ID: {s[0]})" for s in stations])
        if selected_station_id:
            station_id = int(selected_station_id.split("(ID:")[1].split(")")[0])
            station_data = fetch_data(f"SELECT * FROM stations WHERE station_id = {station_id}")[0]
            with st.expander("Station Details"):
                st.markdown(f"""
                    - **Station Name**: {station_data[2]}
                    - **Station Code**: {station_data[1]}
                """)
    else:
        st.warning("No stations available.")

# Add new station
def add_station():
    st.subheader("Add New Station")
    with st.form("station_form"):
        station_name = st.text_input("Station Name")
        station_code = st.text_input("Station Code")
        
        if st.form_submit_button("Add Station"):
            add_entity("stations", ["station_name", "station_code"], [station_name, station_code])

# Book Reservation Page
def book_reservation():
    st.subheader("Book a Reservation")
    
    passengers = fetch_data("SELECT passenger_id, CONCAT(first_name, ' ', last_name) AS full_name FROM passengers")
    trains = fetch_data("SELECT train_id, train_name FROM trains")
    stations = fetch_data("SELECT station_id, station_name FROM stations")

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
                passenger_id = int(selected_passenger_id.split("(ID:")[1].split(")")[0])
                train_id = int(selected_train_id.split("(ID:")[1].split(")")[0])
                start_station_id = int(selected_start_station.split("(ID:")[1].split(")")[0])
                dest_station_id = int(selected_dest_station.split("(ID:")[1].split(")")[0])

                add_entity("reservations", ["passenger_id", "train_id", "train_start_station_id", "destination_station_id", "journey_date", "price"], 
                           [passenger_id, train_id, start_station_id, dest_station_id, journey_date, price])

                st.success("Reservation successfully booked!")
    else:
        st.warning("Unable to book reservation. Ensure passengers, trains, and stations are available.")

# Main Layout
st.title("🚆 Railway Reservation Management System")
st.sidebar.title("Navigation")

# Adding options for the user to choose the type of functionality they want
page = st.sidebar.radio(
    "Select a page",
    ["📋 Passenger Info", "📑 Train Info", "🏙️ Station Info", "🎟️ Book Reservation", "➕ Add Passenger", "➕ Add Train", "➕ Add Station"]
)

# Navigation based on the selected page
if page == "📋 Passenger Info":
    passenger_info()
elif page == "📑 Train Info":
    train_info()
elif page == "🏙️ Station Info":
    station_info()
elif page == "🎟️ Book Reservation":
    book_reservation()
elif page == "➕ Add Passenger":
    add_passenger()
elif page == "➕ Add Train":
    add_train()
elif page == "➕ Add Station":
    add_station()
