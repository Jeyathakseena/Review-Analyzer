import pandas as pd
from docx import Document


def is_text_column(series):
    """Return True if at least 50% of sampled values contain alphabetic characters."""
    sample = series.dropna().astype(str).head(20)
    text_count = sum(1 for val in sample if any(c.isalpha() for c in val))
    return text_count >= len(sample) * 0.5


def find_review_column(df):
    keywords = ["review", "comment", "feedback", "text", "message"]

    # Prefer keyword-named columns first
    for col in df.columns:
        if any(k in col.lower() for k in keywords):
            if is_text_column(df[col]):
                return col

    # Fall back to first valid text column
    for col in df.select_dtypes(include="object").columns:
        if is_text_column(df[col]):
            return col

    return None


def load_file(uploaded_file):
    """
    Load an uploaded file and return a DataFrame with a single 'Review' column.
    Returns (DataFrame, None) on success, (None, error_message) on failure.
    """
    filename = uploaded_file.name

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            col = find_review_column(df)
            if col is None:
                return None, f"No text column found in '{filename}'"
            return pd.DataFrame({"Review": df[col].dropna().astype(str)}), None

        elif filename.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
            col = find_review_column(df)
            if col is None:
                return None, f"No text column found in '{filename}'"
            return pd.DataFrame({"Review": df[col].dropna().astype(str)}), None

        elif filename.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")
            reviews = [r.strip() for r in text.split("\n") if r.strip()]
            return pd.DataFrame({"Review": reviews}), None

        elif filename.endswith(".docx"):
            doc = Document(uploaded_file)
            reviews = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            return pd.DataFrame({"Review": reviews}), None

        else:
            return None, f"Unsupported file type: '{filename}'"

    except Exception as e:
        return None, f"Error reading '{filename}': {e}"
