import streamlit as st
import os


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
            deleted = []
            for path in ["data/reviews.csv", "data/analyzed_reviews.csv"]:
                if os.path.exists(path):
                    os.remove(path)
                    deleted.append(path)
            if deleted:
                st.success(f" Deleted: {', '.join(deleted)}")
            else:
                st.info(" No data files found to delete.")
