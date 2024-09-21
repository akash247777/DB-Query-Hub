import streamlit as st
import pyodbc
import pandas as pd

# Constants for database, user ID, and password
DATABASE = "person"
USER_ID = "sa"
PASSWORD = "Apollo@123"

# Function to connect to SQL Server and execute query
def connect_and_query(server, query):
    try:
        # Establish connection to the database
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={DATABASE};'
            f'UID={USER_ID};'
            f'PWD={PASSWORD};'
        )
        st.success(f"Connected to SQL Server on {server} successfully!")

        cursor = connection.cursor()

        # Execute user-entered query
        cursor.execute(query)

        # Fetch and return results for SELECT queries
        if query.lower().startswith('select'):
            rows = cursor.fetchall()
            return rows

    except pyodbc.Error as e:
        st.error(f"Error connecting to SQL Server on {server}: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        st.info(f"Connection to {server} closed.")

# Streamlit UI
st.title("SQL Server Query Interface")

# File upload for servers
uploaded_file = st.file_uploader("Upload Excel file with server names", type=['xlsx'])

if uploaded_file:
    # Read the uploaded Excel file
    try:
        df = pd.read_excel(uploaded_file)

        # Check if 'Server' column exists in the uploaded file
        if 'Server' in df.columns:
            st.write("### Server List:")
            st.write(df)

            # Text area for SQL query
            query = st.text_area("Enter SQL Query")

            # Execute button for querying all servers
            if st.button("Execute Query on All Servers"):
                if query:
                    # Iterate over each server in the DataFrame and execute the query
                    for server in df['Server']:
                        st.write(f"### Results from server: {server}")
                        result = connect_and_query(server, query)

                        if result:
                            for row in result:
                                st.write(row)
                        else:
                            st.write("No results or error in the query.")
                else:
                    st.error("Please enter a query.")
        else:
            st.error("The uploaded file does not contain a 'Server' column. Please check the file.")
            st.write("Available columns:", df.columns)

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
else:
    st.info("Please upload an Excel file containing server names.")
