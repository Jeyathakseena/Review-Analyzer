import streamlit as st
import pandas as pd
import os
from utils.file_loader import load_file


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
            os.makedirs("data", exist_ok=True)
            combined.to_csv("data/reviews.csv", index=False)
            st.divider()
            st.metric("Total Reviews Uploaded", len(combined))
            st.info(" Files saved. Head to **Run Analysis** to process them.")
        else:
            st.error(" No valid review data could be extracted from the uploaded files.")
