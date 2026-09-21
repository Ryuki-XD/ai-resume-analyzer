# AI Resume Analyzer 📄🤖

A production-quality AI-powered resume analysis tool built with Python, Streamlit, and scikit-learn. Upload your resume, paste a job description, and get instant ATS compatibility scoring, keyword analysis, skill gap identification, and actionable improvement suggestions.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **📤 Resume Upload** — Support for PDF and DOCX formats
- **🔍 Text Extraction** — Intelligent text parsing from uploaded documents
- **📊 ATS Compatibility Score** — TF-IDF + cosine similarity scoring against job descriptions
- **🏷️ Keyword Analysis** — Identify matched and missing keywords
- **🎯 Skill Gap Analysis** — Categorized skill matching across Technical, Tools, Soft Skills, and more
- **💡 Improvement Suggestions** — Prioritized, actionable recommendations
- **📈 Interactive Charts** — Plotly-powered gauge, bar, and radar visualizations
- **📥 PDF Export** — Download a professional analysis report

---

## 🏗️ Project Structure

```
AI RESUME ANALYZER/
├── app/                        # Streamlit UI layer
│   ├── __init__.py
│   ├── main.py                 # App entry point & navigation
│   ├── components/             # Reusable UI components
│   │   ├── __init__.py
│   │   ├── cards.py            # Metric & suggestion cards
│   │   ├── charts.py           # Plotly chart renderers
│   │   └── styles.py           # CSS theming & injection
│   └── pages/                  # Page modules
│       ├── __init__.py
│       ├── analyzer.py         # Resume analysis page
│       └── dashboard.py        # Landing dashboard
├── data/                       # Data assets
│   └── skills.json             # Skill database by category
├── models/                     # Data models
│   ├── __init__.py
│   └── schemas.py              # Dataclasses for results
├── services/                   # Business logic
│   ├── __init__.py
│   ├── analyzer.py             # Core analysis engine
│   ├── report_generator.py     # PDF report builder
│   └── resume_parser.py        # PDF/DOCX text extraction
├── utils/                      # Shared utilities
│   ├── __init__.py
│   ├── constants.py            # Config & skill dictionaries
│   ├── logger.py               # Logging configuration
│   └── text_processing.py      # NLP text utilities
├── logs/                       # Log files (auto-created)
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run.py                      # Launch script
```

---

## Matching and regression checks

Skill and keyword matching uses whole terms, so JavaScript does not count as
Java and unrelated words do not count as R or C. Names such as C++ and C# are
matched literally. This is text matching, not a guarantee of an employer's ATS result.

Run `python -m unittest discover -s tests -v` from the repository root to check
term matching; these checks need only Python's standard library.

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ryuki-XD/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data** (auto-downloads on first run, or manually)
   ```bash
   python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords')"
   ```

5. **Run the application**
   ```bash
   streamlit run app/main.py
   ```
   Or use the launch script:
   ```bash
   python run.py
   ```

6. Open your browser to `http://localhost:8501`

---

## 🎯 Usage

1. Navigate to **Analyze Resume** from the sidebar
2. Upload a PDF or DOCX resume file
3. Paste the target job description
4. Click **🚀 Analyze Resume**
5. Review the ATS score, keyword analysis, skill gaps, and suggestions
6. Click **📥 Download PDF Report** to export results

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| NLP/ML | scikit-learn (TF-IDF), NLTK |
| Charts | Plotly |
| PDF Parsing | PyPDF2 |
| DOCX Parsing | python-docx |
| PDF Export | fpdf2 |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [scikit-learn](https://scikit-learn.org/) for ML/NLP capabilities
- [Plotly](https://plotly.com/) for interactive visualizations
