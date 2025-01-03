import streamlit as st
import mysql.connector

# Connect to the database
def connect_to_database():
    try:
        return mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12755525",
            password="HwqRcpIgdx",
            database="sql12755525"
        )
    except mysql.connector.Error as err:
        st.error(f"Error connecting to the database: {err}")
        return None

# Function to execute a query
def execute_query(query, params=None):
    connection = connect_to_database()
    if connection is None:
        return None
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()  # Fetch all rows for SELECT queries
        connection.commit()  # Commit changes for INSERT/UPDATE/DELETE queries
        return None
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Function to display users
def display_users():
    try:
        users = execute_query("SELECT user_id, name, email, role FROM Users")
        st.write("### Users")
        if users and len(users) > 0:
            st.table(users)
        else:
            st.info("No users found.")
    except Exception as e:
        st.error(f"An error occurred while retrieving users: {e}")

# Function to display customers
def display_customers():
    try:
        customers = execute_query("SELECT customer_id, name, contact_info, industry FROM Customers")
        st.write("### Customers")
        if customers and len(customers) > 0:
            st.table(customers)
        else:
            st.info("No customers found.")
    except Exception as e:
        st.error(f"An error occurred while retrieving customers: {e}")

# Function to display leads
def display_leads():
    try:
        leads = execute_query("""
            SELECT 
                Leads.lead_id, 
                Customers.name AS customer_name, 
                Users.name AS assigned_to, 
                Leads.status, 
                Leads.created_at
            FROM Leads
            LEFT JOIN Customers ON Leads.customer_id = Customers.customer_id
            LEFT JOIN Users ON Leads.assigned_to = Users.user_id
        """)
        st.write("### Leads")
        if leads and len(leads) > 0:
            st.table(leads)
        else:
            st.info("No leads found.")
    except Exception as e:
        st.error(f"An error occurred while retrieving leads: {e}")

# Function to add a new user
def add_user():
    with st.form("Add User"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        role = st.selectbox("Role", ['Sales Representative', 'Sales Manager', 'Account Manager', 'Marketing Team', 'Product Manager', 'Executive'])
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Add User")
        if submitted:
            try:
                if not name or not email or not password:
                    st.error("All fields are required.")
                    return
                execute_query(
                    "INSERT INTO Users (name, email, role, password_hash) VALUES (%s, %s, %s, %s)",
                    (name, email, role, password)
                )
                st.success("User added successfully!")
            except Exception as e:
                st.error(f"An error occurred while adding a user: {e}")

# Main application
def main():
    st.title("Sales Management System")

    # Navigation menu
    menu = ["Users", "Customers", "Leads", "Add User"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Users":
        display_users()
    elif choice == "Customers":
        display_customers()
    elif choice == "Leads":
        display_leads()
    elif choice == "Add User":
        add_user()

if __name__ == "__main__":
    main()
