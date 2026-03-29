import streamlit as st
from database.db_manager import clear_database

def show():
    st.markdown("""
    <div class="page-header">
        <h2> Clear Stored Data</h2>
    </div>
    """, unsafe_allow_html=True)

    st.warning(" This action is irreversible. All uploaded reviews and analysis results will be permanently deleted.")

    confirm = st.checkbox("I understand — delete all data")

    if confirm:
        if st.button(" Delete All Data", type="primary"):
            try:
                # --- NEW DATABASE LOGIC ---
                clear_database()
                st.success(" All database records have been successfully deleted.")
            except Exception as e:
                st.error(f" Failed to clear database: {e}")