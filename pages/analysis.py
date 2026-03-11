import streamlit as st
import pandas as pd
import os
from utils.sentiment_engine import analyze_dataframe


def show():
    st.markdown("""
    <div class="page-header">
        <h2> Run Review Analysis</h2>
    </div>
    """, unsafe_allow_html=True)

    if not os.path.exists("data/reviews.csv"):
        st.warning(" No data found. Please upload review files first.")
        return

    df = pd.read_csv("data/reviews.csv")
    st.info(f" **{len(df)} reviews** loaded and ready to analyze.")

    if st.button("▶  Start Analysis"):
        # Ensure the Review column exists (file_loader now standardizes to 'Review')
        if "Review" not in df.columns:
            possible = ["review", "reviews", "text", "comment", "feedback"]
            matched = next((c for c in df.columns if c.lower() in possible), None)
            if matched is None:
                st.error(" No review column found. Columns available: " + str(df.columns.tolist()))
                return
            df.rename(columns={matched: "Review"}, inplace=True)

        with st.spinner("Analyzing reviews — please wait..."):
            result_df = analyze_dataframe(df)

        os.makedirs("data", exist_ok=True)
        result_df.to_csv("data/analyzed_reviews.csv", index=False)

        st.success(" Analysis complete!")
        

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total",    len(result_df))
        col2.metric("Positive", (result_df["Sentiment"] == "Positive").sum())
        col3.metric("Negative", (result_df["Sentiment"] == "Negative").sum())
        col4.metric("Neutral",  (result_df["Sentiment"] == "Neutral").sum())
