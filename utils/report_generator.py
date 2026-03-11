import pandas as pd
import os
from fpdf import FPDF
import plotly.express as px


def sanitize(text: str) -> str:
    """Replace common Unicode characters that latin-1 can't encode."""
    replacements = {
        "\u2018": "'", "\u2019": "'",   # left/right single quotes
        "\u201c": '"', "\u201d": '"',   # left/right double quotes
        "\u2013": "-", "\u2014": "--",  # en-dash, em-dash
        "\u2026": "...",                # ellipsis
        "\u00e9": "e", "\u00e8": "e",  # accented e
        "\u00e0": "a", "\u00e2": "a",  # accented a
        "\u00f4": "o", "\u00fb": "u",  # accented o, u
    }
    for orig, replacement in replacements.items():
        text = text.replace(orig, replacement)
    # Fallback: drop any remaining non-latin-1 characters
    return text.encode("latin-1", errors="ignore").decode("latin-1")


def generate_report():
    if not os.path.exists("data/analyzed_reviews.csv"):
        return None

    df = pd.read_csv("data/analyzed_reviews.csv")
    os.makedirs("reports", exist_ok=True)

    total     = len(df)
    positive  = len(df[df["Sentiment"] == "Positive"])
    negative  = len(df[df["Sentiment"] == "Negative"])
    neutral   = len(df[df["Sentiment"] == "Neutral"])
    avg_score = round(df["Score"].mean(), 2)

    sentiment_counts = df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    # Pie chart
    pie = px.pie(
        sentiment_counts, values="Count", names="Sentiment",
        color="Sentiment",
        color_discrete_map={"Positive": "#7c3aed", "Negative": "#ef4444", "Neutral": "#9ca3af"},
        title="Sentiment Distribution",
    )
    pie_path = "reports/pie_chart.png"
    pie.write_image(pie_path)

    # Bar chart
    bar = px.bar(
        sentiment_counts, x="Sentiment", y="Count", color="Sentiment",
        color_discrete_map={"Positive": "#7c3aed", "Negative": "#ef4444", "Neutral": "#9ca3af"},
        title="Sentiment Comparison",
    )
    bar_path = "reports/bar_chart.png"
    bar.write_image(bar_path)

    # Score histogram
    hist = px.histogram(df, x="Score", nbins=20, title="Score Distribution",
                        color_discrete_sequence=["#a855f7"])
    hist_path = "reports/histogram.png"
    hist.write_image(hist_path)

    # ── Build PDF ─────────────────────────────────────────────
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(61, 18, 112)
    pdf.cell(0, 12, "Review Analytics Report", ln=True)
    pdf.ln(2)

    # Metrics table
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 8, "Summary Metrics", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(60, 60, 60)

    for label, value in [
        ("Total Reviews",   total),
        ("Positive Reviews", positive),
        ("Negative Reviews", negative),
        ("Neutral Reviews",  neutral),
        ("Average Score",    avg_score),
    ]:
        pdf.cell(80, 8, label, border=1)
        pdf.cell(40, 8, str(value), border=1, ln=True)

    pdf.ln(8)

    # Charts
    for img_path, title in [
        (pie_path,  "Sentiment Distribution"),
        (bar_path,  "Sentiment Comparison"),
        (hist_path, "Score Distribution"),
    ]:
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(61, 18, 112)
        pdf.cell(0, 10, title, ln=True)
        pdf.image(img_path, w=170)
        pdf.ln(6)
        if pdf.get_y() > 220:
            pdf.add_page()

    # Sample reviews
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(61, 18, 112)
    pdf.cell(0, 10, "Sample Reviews (Top 10)", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(40, 40, 40)

    for _, row in df.head(10).iterrows():
        review = sanitize(str(row["Review"])[:200])
        sentiment = sanitize(str(row["Sentiment"]))
        line = f"[{sentiment} | Score: {row['Score']}]  {review}"
        pdf.multi_cell(0, 7, line)
        pdf.ln(2)

    report_path = "reports/review_report.pdf"
    pdf.output(report_path)
    return report_path