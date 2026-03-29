import streamlit as st
import pandas as pd
from utils.sentiment_engine import analyze_dataframe
from database.db_manager import load_raw_reviews, save_analyzed_reviews

def show():
    st.markdown("""
    <div class="page-header">
        <h2> Run Review Analysis</h2>
    </div>
    """, unsafe_allow_html=True)

    # --- NEW DATABASE LOGIC ---
    df = load_raw_reviews()

    if df.empty:
        st.warning(" No data found in the database. Please upload review files first.")
        return

    st.info(f" **{len(df)} reviews** loaded and ready to analyze.")

    if st.button("▶  Start Analysis"):
        if "Review" not in df.columns:
            possible = ["review", "reviews", "text", "comment", "feedback"]
            matched = next((c for c in df.columns if c.lower() in possible), None)
            if matched is None:
                st.error(" No review column found. Columns available: " + str(df.columns.tolist()))
                return
            df.rename(columns={matched: "Review"}, inplace=True)

        with st.spinner("Analyzing reviews — please wait..."):
            result_df = analyze_dataframe(df)

        # --- NEW DATABASE LOGIC ---
        try:
            save_analyzed_reviews(result_df)
            st.success(" Analysis complete and saved to database!")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total",    len(result_df))
            col2.metric("Positive", (result_df["Sentiment"] == "Positive").sum())
            col3.metric("Negative", (result_df["Sentiment"] == "Negative").sum())
            col4.metric("Neutral",  (result_df["Sentiment"] == "Neutral").sum())
            
        except Exception as e:
            st.error(f" Failed to save analysis to database: {e}")