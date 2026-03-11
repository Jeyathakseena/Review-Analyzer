import streamlit as st
import pandas as pd
import os


def show():
    st.markdown("""
    <div class="page-header">
        <h2> System Overview</h2>
    </div>
    """, unsafe_allow_html=True)

    raw_exists      = os.path.exists("data/reviews.csv")
    analyzed_exists = os.path.exists("data/analyzed_reviews.csv")

    # Status badges
    st.markdown(f"""
    <div style="display:flex;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;">
        <div style="background:{'#f0fdf4' if raw_exists else '#fef2f2'};
                    border:1.5px solid {'#22c55e' if raw_exists else '#fca5a5'};
                    border-radius:10px;padding:0.6rem 1.2rem;font-size:0.85rem;font-weight:500;">
            {'✅' if raw_exists else '❌'} Raw data {'present' if raw_exists else 'missing'}
        </div>
        <div style="background:{'#f0fdf4' if analyzed_exists else '#fef2f2'};
                    border:1.5px solid {'#22c55e' if analyzed_exists else '#fca5a5'};
                    border-radius:10px;padding:0.6rem 1.2rem;font-size:0.85rem;font-weight:500;">
            {'✅' if analyzed_exists else '❌'} Analysis {'ready' if analyzed_exists else 'not run yet'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if analyzed_exists:
        df = pd.read_csv("data/analyzed_reviews.csv")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Reviews", len(df))
        col2.metric("Positive", (df["Sentiment"] == "Positive").sum())
        col3.metric("Negative", (df["Sentiment"] == "Negative").sum())
        col4.metric("Neutral",  (df["Sentiment"] == "Neutral").sum())
    else:
        st.info("ℹ️ No analysis data available yet. Upload reviews and run analysis to see metrics here.")
