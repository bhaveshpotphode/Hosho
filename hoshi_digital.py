# -*- coding: utf-8 -*-
"""Hoshi digital.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1F7U65S9nNyuc-7cD58W8_AAa3h4jXpew
"""

import streamlit as st
import pymysql

# Database connection settings
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Bhavesh@90"
DB_NAME = "hosho_digital_project"

# Connect to the database
def connect_to_database():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to execute a query
def execute_query(query, params=None):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

# Function to display users
def display_users():
    users = execute_query("SELECT * FROM Users")
    st.write("### Users")
    st.table(users)

# Function to display customers
def display_customers():
    customers = execute_query("SELECT * FROM Customers")
    st.write("### Customers")
    st.table(customers)

# Function to display leads
def display_leads():
    leads = execute_query("""
        SELECT Leads.lead_id, Customers.name AS customer_name, Users.name AS assigned_to, Leads.status, Leads.created_at
        FROM Leads
        LEFT JOIN Customers ON Leads.customer_id = Customers.customer_id
        LEFT JOIN Users ON Leads.assigned_to = Users.user_id
    """)
    st.write("### Leads")
    st.table(leads)

# Function to add a new user
def add_user():
    with st.form("Add User"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        role = st.selectbox("Role", ['Sales Representative', 'Sales Manager', 'Account Manager', 'Marketing Team', 'Product Manager', 'Executive'])
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Add User")
        if submitted:
            password_hash = hash(password)  # Simple hash, replace with a secure hash in production
            execute_query(
                "INSERT INTO Users (name, email, role, password_hash) VALUES (%s, %s, %s, %s)",
                (name, email, role, password_hash)
            )
            st.success("User added successfully!")

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
