from db import mysql_connection
from db import fetch_all_operation,query_fetch_all_operation,commit_operation

def add_route(st):
    st.header("Assign Train to Route")
    
    connection = mysql_connection.get_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch Trains and Stations
    query = "SELECT * FROM trains"
    # cursor.execute(query)
    # trains = cursor.fetchall()
    
    trains = query_fetch_all_operation(query=query)
    
    train_options = {train['train_name']: train['train_id'] for train in trains}

    query = "SELECT * FROM stations"
    # cursor.execute(query)
    # stations = cursor.fetchall()
    
    stations = query_fetch_all_operation(query)
    station_options = {station['station_name']: station['station_id'] for station in stations}

    # Select Train and Define Route
    train = st.selectbox("Select Train", list(train_options.keys()))
    station_sequence = []

    st.subheader("Add Stations to the Route")
    num_stations = st.number_input("Number of Stations in the Route", min_value=2, max_value=len(station_options))

    for i in range(int(num_stations)):
        station = st.selectbox(f"Select Station {i+1}", list(station_options.keys()), key=f"station_{i}")
        arrival_time = st.time_input(f"Arrival Time at {station}", key=f"arrival_{i}")
        departure_time = st.time_input(f"Departure Time at {station}", key=f"departure_{i}")
        station_sequence.append({
            'station_id': station_options[station],
            'arrival_time': arrival_time,
            'departure_time': departure_time,
            'sequence': i + 1
        })

    if st.button("Assign Route to Train"):
        train_id = train_options[train]
        for station in station_sequence:
            query = "INSERT INTO routes (train_id, station_id, arrival_time, departure_time, sequence) VALUES (%s, %s, %s, %s, %s)"
            values = (train_id, station['station_id'], station['arrival_time'], station['departure_time'], station['sequence'])
            
            commit_operation(query=query,value=values)
            # cursor.execute(
            #     "INSERT INTO routes (train_id, station_id, arrival_time, departure_time, sequence) "
            #     "VALUES (%s, %s, %s, %s, %s)",
            #     (train_id, station['station_id'], station['arrival_time'], station['departure_time'], station['sequence'])
            # )
        # connection.commit()
        st.success("Route assigned to train successfully.")

    cursor.close()

