#  Review Analysis System

A Streamlit-based web app that processes bulk customer reviews, runs sentiment analysis, and delivers visual reports via email.

## Features

- 📤 Upload reviews via CSV, TXT, XLSX, or DOCX
- ⚙️ Rule-based sentiment scoring engine (Positive / Negative / Neutral)
- 📊 Interactive charts — pie, bar, and score histogram
- 📋 Browse, filter, and download analyzed records
- 📄 Auto-generate a branded PDF analytics report
- 📧 Email the PDF + top 20,000 reviews CSV to any recipient
- 🗑️ Clear all data and start fresh

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [pandas](https://pandas.pydata.org/) — data processing
- [fpdf](https://pyfpdf.readthedocs.io/) — PDF generation
- [plotly](https://plotly.com/python/) — charts
- Python `smtplib` — email delivery


📦 project_root
 ┣ 📂 database
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 db_manager.py
 ┃ ┗ 📜 system_data.db
 ┣ 📂 pages
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 analysis.py
 ┃ ┣ 📜 clear_data.py
 ┃ ┣ 📜 dashboard.py
 ┃ ┣ 📜 email_report.py
 ┃ ┣ 📜 overview.py
 ┃ ┣ 📜 records.py
 ┃ ┗ 📜 upload.py
 ┣ 📂 reports
 ┃ ┣ 📜 bar_chart.png
 ┃ ┣ 📜 histogram.png
 ┃ ┣ 📜 pie_chart.png
 ┃ ┗ 📜 review_report.pdf
 ┣ 📂 utils
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 email_sender.py
 ┃ ┣ 📜 file_loader.py
 ┃ ┣ 📜 keyword_lists.py
 ┃ ┣ 📜 report_generator.py
 ┃ ┗ 📜 sentiment_engine.py
 ┣ 📜 .env
 ┣ 📜 .gitignore
 ┣ 📜 app.py
 ┗ 📜 license.txt