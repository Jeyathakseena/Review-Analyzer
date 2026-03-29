import streamlit as st
import re
import threading
from utils.report_generator import generate_report
from utils.email_sender import send_email

def background_send(email_address, report_path):
    """This function runs invisibly in the background."""
    send_email(email_address, report_path)

def show():
    st.markdown("""
    <div class="page-header">
        <h2> Email Analytics Report</h2>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input("Recipient Email Address", placeholder="example@gmail.com")

    if st.button(" Generate & Send Report"):
        if not email.strip():
            st.error(" Please enter an email address.")
            return

        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email.strip()):
            st.error(" Please enter a valid email address.")
            return

        # We still wait for the PDF to generate since it relies on the data
        with st.spinner("Generating PDF report..."):
            report_path = generate_report()

        if report_path is None:
            st.error(" No analysis data found. Please run analysis first.")
            return

        # --- THREADING MAGIC ---
        # Instead of waiting for SMTP, we launch it as a background process
        thread = threading.Thread(target=background_send, args=(email.strip(), report_path))
        thread.start()

        # Immediately unblock the UI!
        st.success("✅ Report generated! The email is currently sending in the background. You can continue using the app.")