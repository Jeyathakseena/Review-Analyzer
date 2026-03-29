import streamlit as st
from database.db_manager import load_raw_reviews, load_analyzed_reviews

def show():
    st.markdown("""
    <div class="page-header">
        <h2> System Overview</h2>
    </div>
    """, unsafe_allow_html=True)

    # --- NEW DATABASE LOGIC ---
    raw_df = load_raw_reviews()
    analyzed_df = load_analyzed_reviews()
    
    raw_exists = not raw_df.empty
    analyzed_exists = not analyzed_df.empty

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
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Reviews", len(analyzed_df))
        col2.metric("Positive", (analyzed_df["Sentiment"] == "Positive").sum())
        col3.metric("Negative", (analyzed_df["Sentiment"] == "Negative").sum())
        col4.metric("Neutral",  (analyzed_df["Sentiment"] == "Neutral").sum())
    else:
        st.info("ℹ️ No analysis data available yet. Upload reviews and run analysis to see metrics here.")