import streamlit as st
import pyodbc

# Function to connect to SQL Server and execute query
def connect_and_query(server, database, user_id, password, query):
    connection = None
    cursor = None
    try:
        # Establish connection to the database
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={user_id};'
            f'PWD={password};'
        )
        st.success("Connected to SQL Server successfully!")

        cursor = connection.cursor()

        # Execute user-entered query
        cursor.execute(query)

        # Commit if it's an INSERT, UPDATE, or DELETE query
        if query.lower().startswith(('insert', 'update', 'delete')):
            connection.commit()
            st.success("Query executed successfully!")

        # Fetch and display results for SELECT queries
        elif query.lower().startswith('select'):
            rows = cursor.fetchall()
            st.write("### Query Results:")
            for row in rows:
                st.write(row)

    except pyodbc.Error as e:
        st.error(f"Error connecting to SQL Server: {e}")

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
        st.info("Connection closed.")

# Streamlit UI
st.title("SQL Server Query Interface")

# Input fields
server = st.text_input("Server", value="APL94855")  # Pre-fill the server name
database = st.text_input("Database")  # You'll need to enter the database manually
user_id = st.text_input("User ID", value="sa")  # Use 'sa' based on your image
password = st.text_input("Password", type="password")  # Enter the password

# Text area for SQL query
query = st.text_area("Enter SQL Query")

# Execute button
if st.button("Execute Query"):
    if server and database and user_id and password and query:
        connect_and_query(server, database, user_id, password, query)
    else:
        st.error("Please fill all the fields.")
