import streamlit as st
import pyodbc

# Function to connect to SQL Server and execute query
def connect_and_query(server, database, user_id, password, query):
    connection = None  # Initialize connection to None
    cursor = None  # Initialize cursor to None
    try:
        # Establish connection to the database with a timeout
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={user_id};'
            f'PWD={password};'
            'Connection Timeout=30;'  # Corrected timeout syntax
        )
        st.success("Connected to SQL Server successfully!")

        # Create a cursor object to execute the query
        cursor = connection.cursor()

        # Execute user-entered query
        cursor.execute(query)

        # Commit if it's an INSERT, UPDATE, or DELETE query
        if query.strip().lower().startswith(('insert', 'update', 'delete')):
            connection.commit()
            st.success("Query executed successfully!")

        # Fetch and display results for SELECT queries
        elif query.strip().lower().startswith('select'):
            rows = cursor.fetchall()
            if rows:
                st.write("### Query Results:")
                for row in rows:
                    st.write(row)
            else:
                st.warning("No results found.")

    except pyodbc.Error as e:
        st.error(f"Error connecting to SQL Server: {e}")

    finally:
        # Safely close the cursor and connection if they were created
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        st.info("Connection closed.")

# Streamlit UI
st.title("SQL Server Query Interface")

# Input fields for connection details
server = st.text_input("Server")
database = st.text_input("Database")
user_id = st.text_input("User ID")
password = st.text_input("Password", type="password")

# Text area for SQL query input
query = st.text_area("Enter SQL Query")

# Button to execute the query
if st.button("Execute Query"):
    if server and database and user_id and password and query:
        connect_and_query(server, database, user_id, password, query)
    else:
        st.error("Please fill all the fields.")
