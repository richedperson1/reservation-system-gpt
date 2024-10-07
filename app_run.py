import streamlit as st
import mysql.connector
# from mysql.connector import errorcode
import pandas as pd
import hashlib
from datetime import datetime

# The code you provided is a Python code snippet with a comment `# from admin import`. However, the
# import statement is incomplete, as it does not specify what is being imported from the `admin`
# module. To complete the import statement, you need to specify the module or object that you want to
# import from the `admin` module. For example, if you want to import a specific function named
# `my_function` from the `admin` module, the import statement should look like this:
from admin import  add_route,view_available_tickets,view_reservations,increase_seats_in_train


# from authenticate import Authenticate  # Replace this with the actual location of Authenticate

# --- Database Connection ---
# @st.experimental_singleton
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
        user="root",
        password="ru15070610",
        database="railway_reservation_management_price"
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        st.stop()


# --- Main Application ---

def main():
    st.set_page_config(page_title="Railway Reservation System", layout="wide")
    st.title("Railway Reservation Management System")

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Page Navigation
    menu = ['Admin Panel','Home', 'Reserve Ticket']
    choice = st.sidebar.selectbox('Navigation', menu)

    if choice == 'Home':
        # st.image('railway_banner.jpg', use_column_width=True)
        st.markdown("""
        Welcome to the Railway Reservation System. Navigate through the sidebar to reserve tickets or access the admin panel.
        """)

    elif choice == 'Reserve Ticket':
        st.header("Reserve Ticket")

        # --- User Input for Reservation ---
        with st.form("reservation_form"):
            st.subheader("Passenger Information")
            first_name = st.text_input("First Name", max_chars=100)
            last_name = st.text_input("Last Name", max_chars=100)
            gender = st.selectbox("Gender", options=['Male', 'Female', 'Other'])
            age = st.number_input("Age", min_value=0, max_value=120, value=25)
            mobile_no = st.text_input("Mobile No", max_chars=15)
            aadhar_no = st.text_input("Aadhar No", max_chars=12)
            email = st.text_input("Email")

            st.subheader("Journey Details")
            # Fetch Stations
            cursor.execute("SELECT station_id, station_name FROM stations")
            stations = cursor.fetchall()
            station_options = {station['station_name']: station['station_id'] for station in stations}
            start_station_name = st.selectbox("Starting Station", options=station_options.keys())
            destination_station_name = st.selectbox("Destination Station", options=station_options.keys())

            journey_date = st.date_input("Journey Date", min_value=datetime.today())

            # Fetch Classes
            cursor.execute("SELECT class_id, class_name FROM classes")
            classes = cursor.fetchall()
            class_options = {cls['class_name']: cls['class_id'] for cls in classes}
            selected_class_name = st.selectbox("Class", options=class_options.keys())

            submitted = st.form_submit_button("Check Availability")

        if submitted:
            # --- Processing Reservation ---
            passenger_data = {
                'first_name': first_name.strip(),
                'last_name': last_name.strip(),
                'gender': gender,
                'age': age,
                'mobile_no': mobile_no.strip(),
                'aadhar_no': aadhar_no.strip(),
                'email': email.strip()
            }

            # Input validation can be added here (omitted for brevity)

            start_station_id = station_options[start_station_name]
            destination_station_id = station_options[destination_station_name]
            class_id = class_options[selected_class_name]

            # Fetch Trains available between stations
            cursor.execute("""
                SELECT DISTINCT t.train_id, t.train_name
                FROM trains t
                JOIN routes r1 ON t.train_id = r1.train_id
                JOIN routes r2 ON t.train_id = r2.train_id
                WHERE r1.station_id = %s AND r2.station_id = %s AND r1.sequence < r2.sequence
            """, (start_station_id, destination_station_id))
            trains = cursor.fetchall()

            if trains:
                train_options = {train['train_name']: train['train_id'] for train in trains}
                selected_train_name = st.selectbox("Available Trains", options=train_options.keys())
                selected_train_id = train_options[selected_train_name]

                # Check Seat Availability
                cursor.execute("""
                    SELECT COUNT(*) AS available_seats
                    FROM seats
                    WHERE train_id = %s AND class_id = %s AND availability_status = 'Available'
                """, (selected_train_id, class_id))
                seat_availability = cursor.fetchone()['available_seats']

                if seat_availability > 0:
                    st.success(f"Seats Available: {seat_availability}")

                    # Fetch Fare
                    cursor.execute("""
                        SELECT price
                        FROM fares
                        WHERE train_id = %s AND class_id = %s AND start_station_id = %s AND end_station_id = %s
                    """, (selected_train_id, class_id, start_station_id, destination_station_id))
                    fare = cursor.fetchone()

                    if fare:
                        ticket_price = fare['price']
                        st.info(f"Ticket Price: ₹{ticket_price}")

                        if st.button("Confirm Reservation"):
                            # Insert Passenger
                            cursor.execute("""
                                INSERT INTO passengers (first_name, last_name, gender, age, mobile_no, aadhar_no, email)
                                VALUES (%(first_name)s, %(last_name)s, %(gender)s, %(age)s, %(mobile_no)s, %(aadhar_no)s, %(email)s)
                            """, passenger_data)
                            conn.commit()
                            passenger_id = cursor.lastrowid

                            # Book Seat
                            cursor.execute("""
                                SELECT seat_id
                                FROM seats
                                WHERE train_id = %s AND class_id = %s AND availability_status = 'Available'
                                LIMIT 1
                            """, (selected_train_id, class_id))
                            seat = cursor.fetchone()
                            seat_id = seat['seat_id']

                            cursor.execute("""
                                UPDATE seats
                                SET availability_status = 'Booked', reservation_id = NULL  -- Will be updated after reservation
                                WHERE seat_id = %s
                            """, (seat_id,))
                            conn.commit()

                            # Create Reservation
                            reservation_no = f"RES{hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:10]}"
                            cursor.execute("""
                                INSERT INTO reservations
                                (passenger_id, train_id, class_id, reservation_no, train_start_station_id, destination_station_id, reservation_date, journey_date, fare_id)
                                VALUES (%s, %s, %s, %s, %s, %s, CURDATE(), %s, (SELECT fare_id FROM fares WHERE train_id = %s AND class_id = %s AND start_station_id = %s AND end_station_id = %s))
                            """, (passenger_id, selected_train_id, class_id, reservation_no, start_station_id, destination_station_id, journey_date, selected_train_id, class_id, start_station_id, destination_station_id))
                            conn.commit()
                            reservation_id = cursor.lastrowid

                            # Update seat with reservation_id
                            cursor.execute("""
                                UPDATE seats
                                SET reservation_id = %s
                                WHERE seat_id = %s
                            """, (reservation_id, seat_id))
                            conn.commit()

                            st.success(f"Reservation Successful! Your Reservation Number is {reservation_no}")

                            # Optionally, display or email ticket details.

                    else:
                        st.error("Ticket fare information is not available for the selected route.")
                else:
                    st.error("No seats available in the selected class.")
            else:
                st.error("No trains available between the selected stations.")

    elif choice == 'Admin Panel':
        st.header("Admin Panel")

        # --- Admin Authentication ---
        authentication_status = True
        if authentication_status:
            st.success("Admin authenticated successfully.")

            admin_menu: list[str] = ["Add Train", "Add Station", "Add Ticket Class", "Add Train Route", "View Available Tickets", "View Reservations", "Increase Seats in Train"]
            admin_choice = st.selectbox('Admin Options', admin_menu)

            if admin_choice == 'Add Train':
                st.subheader("Add New Train")
                with st.form("add_train_form"):
                    train_no = st.text_input("Train Number", max_chars=10)
                    train_name = st.text_input("Train Name", max_chars=255)
                    train_type = st.selectbox("Train Type", options=['Passenger', 'Express', 'Superfast'])
                    total_seats = st.number_input("Total Seats", min_value=1, value=100)
                    submitted = st.form_submit_button("Add Train")
                if submitted:
                    cursor.execute("""
                        INSERT INTO trains (train_no, train_name, train_type, total_seats)
                        VALUES (%s, %s, %s, %s)
                    """, (train_no, train_name, train_type, total_seats))
                    conn.commit()
                    st.success(f"Train {train_name} added successfully.")
            elif admin_choice == "View Available Tickets":
                view_available_tickets(st)
            elif admin_choice == "View Reservations":
                view_reservations(st=st)
            elif admin_choice == "Increase Seats in Train":
                increase_seats_in_train(st)
            elif admin_choice== "Add Train Route":
                add_route(st=st)
            elif admin_choice == 'Add Station':
                st.subheader("Add New Station")
                with st.form("add_station_form"):
                    station_code = st.text_input("Station Code", max_chars=10)
                    station_name = st.text_input("Station Name", max_chars=255)
                    city = st.text_input("City", max_chars=100)
                    state = st.text_input("State", max_chars=100)
                    submitted = st.form_submit_button("Add Station")
                if submitted:
                    cursor.execute("""
                        INSERT INTO stations (station_code, station_name, city, state)
                        VALUES (%s, %s, %s, %s)
                    """, (station_code, station_name, city, state))
                    conn.commit()
                    st.success(f"Station {station_name} added successfully.")

            # elif admin_choice == 'Set Ticket Prices':
            #     set_ticket_price(st=st)
            # Logout button
            if st.button("Logout"):
                # authenticator.logout('Logout', 'sidebar')
                st.session_state.clear()
                st.experimental_rerun()

        elif authentication_status == False:
            st.error("Username/password is incorrect")
        elif authentication_status == None:
            st.warning("Please enter your username and password")

    # --- Close Database Connection ---
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()