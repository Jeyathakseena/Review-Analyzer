import streamlit as st
import pandas as pd
from utils.file_loader import load_file
from database.db_manager import save_raw_reviews

def show():
    st.markdown("""
    <div class="page-header">
        <h2> Upload Review Files</h2>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Drag & drop files here — CSV, XLSX, TXT, or DOCX",
        accept_multiple_files=True,
        type=["csv", "xlsx", "txt", "docx"],
    )

    if uploaded_files:
        all_reviews = []
        errors = []

        for file in uploaded_files:
            df, err = load_file(file)
            if df is not None:
                all_reviews.append(df)
                st.success(f" **{file.name}** — {len(df)} reviews loaded")
            else:
                errors.append(file.name)
                st.warning(f" **{file.name}** — {err}")

        if all_reviews:
            combined = pd.concat(all_reviews, ignore_index=True)
            
            # --- NEW DATABASE LOGIC ---
            try:
                save_raw_reviews(combined)
                st.divider()
                st.metric("Total Reviews Uploaded", len(combined))
                st.info(" Files saved to database. Head to **Run Analysis** to process them.")
            except Exception as e:
                st.error(f" Database Error: {e}")
        else:
            st.error(" No valid review data could be extracted from the uploaded files.")