import smtplib
import os
import re
import io
import pandas as pd
from email.message import EmailMessage
from database.db_manager import load_top_reviews

def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def send_email(
    receiver: str,
    filepath: str = None,
    pdf_path: str = None,
    report_path: str = None,
    summary: str = None,       
    **kwargs,                  
) -> tuple[bool, str]:
    """
    Send the PDF report + top 20,000 rows CSV to `receiver`.
    Returns (success: bool, message: str).
    """
    resolved_path = filepath or pdf_path or report_path

    if not resolved_path:
        return False, "No PDF path provided."

    if not is_valid_email(receiver):
        return False, "Invalid email address."

    sender   = os.environ.get("EMAIL_SENDER", "").strip()
    password = os.environ.get("EMAIL_PASSWORD", "").strip()

    if not sender or not password:
        return False, (
            "Email credentials not configured. "
            "Set the EMAIL_SENDER and EMAIL_PASSWORD environment variables."
        )

    try:
        msg = EmailMessage()
        msg["Subject"] = "Review Analysis Report"
        msg["From"]    = sender
        msg["To"]      = receiver
        msg.set_content(
            "Please find attached your automated review analysis report.\n\n"
            "Attachments:\n"
            "  1. review_report.pdf  – Visual analytics report\n"
            "  2. top_reviews.csv    – Top 20,000 reviews (by score, descending)\n"
        )

        # ── Attach PDF ────────────────────────────────────────
        with open(resolved_path, "rb") as f:
            pdf_data = f.read()

        msg.add_attachment(
            pdf_data,
            maintype="application",
            subtype="pdf",
            filename="review_report.pdf",
        )

       # ── Attach CSV (top 20,000 reviews by score) ──────────
        # Pulling the pre-sorted top 20k directly from the database
        top_df = load_top_reviews(20000)
        
        if not top_df.empty:
            csv_buffer = io.StringIO()
            top_df.to_csv(csv_buffer, index=False)
            csv_bytes = csv_buffer.getvalue().encode("utf-8")

            msg.add_attachment(
                csv_bytes,
                maintype="text",
                subtype="csv",
                filename="top_reviews.csv",
            )

        # ── Send ──────────────────────────────────────────────
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)

        return True, "Report and CSV sent successfully!"

    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Check your EMAIL_SENDER and EMAIL_PASSWORD."
    except FileNotFoundError:
        return False, f"Report file not found: {resolved_path}"
    except Exception as e:
        return False, f"Failed to send email: {e}"