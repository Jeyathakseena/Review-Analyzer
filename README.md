# 🔮 Review Analysis System

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



## Project Structure
```
review_analyzer/
├── app.py                  # Main entry point & navigation
├── pages/
│   ├── overview.py         # Dashboard summary
│   ├── upload.py           # File upload
│   ├── analysis.py         # Run sentiment analysis
│   ├── records.py          # Browse records
│   ├── analytics.py        # Charts & visualizations
│   ├── email_report.py     # Email report page
│   └── clear_data.py       # Clear all data
├── utils/
│   ├── sentiment_engine.py # Scoring logic
│   ├── report_generator.py # PDF builder
│   ├── email_sender.py     # Email delivery
│   ├── file_loader.py      # File parsing
│   └── keyword_lists.py    # Sentiment keywords
├── data/                   # Generated at runtime (gitignored)
├── reports/                # Generated at runtime (gitignored)
└── requirements.txt
```

