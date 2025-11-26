# YouTube Summary Feedback System
Tkinter desktop app that analyzes YouTube videos for summary, sentiment, and feedback using Gemini and comment processing.

## Description
- Python desktop application
- Analyzes YouTube videos and viewer comments
- Generates:
  - Video summary
  - Comment sentiment analysis
  - Thematic feedback
- Uses:
  - Tkinter (UI)
  - YouTube Data API (retrieval)
  - Gemini (text generation)

---

## Features
- Input: YouTube URL
- Output:
  - Transcript summary
  - Sentiment score
  - Feedback bullets
  - Exported `.txt` reports
- Background threading to keep UI responsive

---

## Repository Structure
```text
youtube-summary-feedback-system/
├─ Code/
│  ├─ base_analyzer.py
│  ├─ data_preprocessor.py
│  ├─ data_retrieval.py
│  ├─ feedback_extractor.py
│  ├─ main.py
│  ├─ sentiment_analyzer.py
│  ├─ summarizer.py
│  ├─ user_interface.py
│  ├─ youtubeAPICon.py
│  ├─ assets/
│  └─ reports/
├─ Sprint3 final documentationv1.pdf
├─ sprint3 Final ppt.pptx
├─ YouTubeFeedbackvideo.mp4
└─ README.md
```

## Installation
```text
git clone https://github.com/Ayush-B/youtube-summary-feedback-system.git
cd youtube-summary-feedback-system/Code
python -m venv .venv
```

## Activate Environment
```text
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

## Install Dependencies
```text
pip install -r requirements.txt
```

## Environment Variables
```text
YOUTUBE_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```
Place inside .env
.env must be in .gitignore


## Running the Application
```text
python main.py
```
