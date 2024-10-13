import mysql.connector
from mysql.connector import Error

# MySQL connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # replace with your MySQL username
        password="ru15070610",  # replace with your MySQL password
        database="railway_reservation_management_price"
    )

# Function to check if a class already exists in the database
def class_exists(conn, class_name):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM classes WHERE class_name = %s", (class_name,))
    result = cursor.fetchone()
    return result[0] > 0  # Returns True if class exists, False otherwise

# Function to insert a new class into the database
def insert_class(conn, class_name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO classes (class_name) VALUES (%s)", (class_name,))
    conn.commit()

# Main Streamlit app for adding train classes
def class_app(st):
    conn = create_connection()

    st.title("Add Train Class")

    # Input form for adding a new train class
    with st.form("add_class_form"):
        class_name = st.selectbox("Select Class Name", ['Sleeper', 'AC', 'General'])

        # Submit button for the form
        submit_button = st.form_submit_button("Add Class")

    if submit_button:
        # Check if the class already exists
        if class_exists(conn, class_name):
            st.warning(f"Class '{class_name}' already exists!")
        else:
            try:
                # Inserting the class if it's not already in the table
                insert_class(conn, class_name)
                st.success(f"Class '{class_name}' added successfully!")
            except Error as e:
                st.error(f"Error: {e}")

    conn.close()

