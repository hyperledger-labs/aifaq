import streamlit as st
from menu import menu_with_redirect
from database import create_connection

def get_all_users(conn):
    """Retrieve all users from database"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()
    except Exception as e:
        st.error(f"Error fetching users: {str(e)}")
        return []

def update_user_type(conn, email, new_type):
    """Update user type in database"""
    try:
        cur = conn.cursor()
        cur.execute("UPDATE users SET type = ? WHERE email = ?", (new_type, email))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error updating user type: {str(e)}")
        return False

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.user_type not in ["admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown("# User Management")

# Connect to database
conn = create_connection()
if conn is None:
    st.error("Could not connect to database")
    st.stop()

# Get all users
users = get_all_users(conn)

# Display users in a table with type selection
st.write("### User List")

# Create columns for the table header
cols = st.columns([3, 2, 2, 2])
cols[0].write("**Email**")
cols[1].write("**Username**")
cols[2].write("**Current Type**")
cols[3].write("**New Type**")

# Available user types
user_types = ["guest", "user", "admin"]

# Display each user with their current type and a dropdown to change it
for user in users:
    user_id, username, email, current_type, _, _ = user
    
    cols = st.columns([3, 2, 2, 2])
    cols[0].write(email)
    cols[1].write(username)
    cols[2].write(current_type)
    
    # Create a unique key for each dropdown
    key = f"type_{user_id}"
    new_type = cols[3].selectbox(
        "Select Type",
        options=user_types,
        index=user_types.index(current_type) if current_type in user_types else 0,
        key=key,
        label_visibility="collapsed"
    )
    
    # Update button
    if new_type != current_type:
        if cols[3].button("Save", key=f"save_{user_id}"):
            if update_user_type(conn, email, new_type):
                st.success(f"Updated {username}'s type to {new_type}")
                st.rerun()