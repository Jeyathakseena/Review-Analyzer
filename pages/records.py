import streamlit as st
from database.db_manager import load_analyzed_reviews

def show():
    st.markdown("""
    <div class="page-header">
        <h2> Review Records</h2>
    </div>
    """, unsafe_allow_html=True)

    # --- NEW DATABASE LOGIC ---
    df = load_analyzed_reviews()

    if df.empty:
        st.warning(" No analyzed data found. Please run analysis first.")
        return

    col1, col2 = st.columns([3, 1])

    with col1:
        search = st.text_input(" Search reviews", placeholder="Type a keyword...")

    with col2:
        sentiment = st.selectbox("Filter Sentiment", ["All", "Positive", "Negative", "Neutral"])

    if search:
        df = df[df["Review"].str.contains(search, case=False, na=False)]

    if sentiment != "All":
        df = df[df["Sentiment"] == sentiment]

    st.markdown(f"**{len(df)} record(s) found**")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False),
        "filtered_reviews.csv",
        mime="text/csv",
    )