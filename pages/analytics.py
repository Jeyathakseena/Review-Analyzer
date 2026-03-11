import streamlit as st
import pandas as pd
import os
import plotly.express as px

COLORS = {"Positive": "#7c3aed", "Negative": "#ef4444", "Neutral": "#9ca3af"}

def show():
    st.markdown("""
    <div class="page-header">
        <h2> Analytics Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)

    if not os.path.exists("data/analyzed_reviews.csv"):
        st.warning(" No analyzed data found. Please run analysis first.")
        return

    df = pd.read_csv("data/analyzed_reviews.csv")

    total    = len(df)
    positive = (df["Sentiment"] == "Positive").sum()
    negative = (df["Sentiment"] == "Negative").sum()
    neutral  = (df["Sentiment"] == "Neutral").sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reviews", total)
    col2.metric("Positive", positive)
    col3.metric("Negative", negative)
    col4.metric("Neutral",  neutral)

    st.divider()

    sentiment_counts = df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    c1, c2 = st.columns(2)

    with c1:
        pie = px.pie(
            sentiment_counts, values="Count", names="Sentiment",
            title="Sentiment Distribution",
            color="Sentiment", color_discrete_map=COLORS,
        )
        pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(pie, use_container_width=True)

    with c2:
        bar = px.bar(
            sentiment_counts, x="Sentiment", y="Count",
            color="Sentiment", color_discrete_map=COLORS,
            title="Sentiment Comparison",
        )
        bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          showlegend=False)
        st.plotly_chart(bar, use_container_width=True)

    hist = px.histogram(
        df, x="Score", nbins=20,
        title="Sentiment Score Distribution",
        color_discrete_sequence=["#a855f7"],
    )
    hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(hist, use_container_width=True)

    st.divider()
    st.subheader("Review Length Analysis")

    df["Length"] = df["Review"].astype(str).apply(len)
    length_chart = px.histogram(
        df, x="Length", nbins=30,
        title="Review Length Distribution",
        color_discrete_sequence=["#c084fc"],
    )
    length_chart.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(length_chart, use_container_width=True)
