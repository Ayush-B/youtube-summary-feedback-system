import google.generativeai as genai
from typing import Optional
from base_analyzer import BaseAnalyzer

class Summarizer(BaseAnalyzer):
    """Handles summarization of a video transcript using Google Gemini AI."""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        genai.configure(api_key=self.api_key)

    SUMMARY_PROMPT = (
        "You are an expert content summarizer. Your task is to read the following YouTube video transcript "
        "and produce a concise, insightful summary. Focus on key points, main topics, and any important details or "
        "takeaways."
        "The summary should be clear, well-structured, and engaging. Provide plain text only.\n\n"
        "Transcript:\n{transcript}"
    )
    def analyze(self, cleaned_transcript: str) -> Optional[str]:
        try:
            model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
            prompt = Summarizer.SUMMARY_PROMPT.format(transcript=cleaned_transcript)
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[ERROR] Summary generation failed: {e}")
            return None
