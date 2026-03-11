import streamlit as st
import re
from utils.report_generator import generate_report
from utils.email_sender import send_email


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

        with st.spinner("Generating PDF report..."):
            report_path = generate_report()

        if report_path is None:
            st.error(" No analysis data found. Please run analysis first.")
            return

        with st.spinner("Sending email..."):
            success, message = send_email(email.strip(), report_path)

        if success:
            st.success(f"✅ {message}")
        else:
            st.error(f"❌ {message}")