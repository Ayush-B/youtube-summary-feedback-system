import google.generativeai as genai
from typing import List, Dict, Optional
from base_analyzer import BaseAnalyzer


class FeedbackExtractor(BaseAnalyzer):
    """Processes comments using Gemini AI to extract 'What’s Working' and 'Needs Improvement' feedback."""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        genai.configure(api_key=self.api_key)

    WORKS_PROMPT = (
        "You are a professional video content analyst. Given the following YouTube comments about a video, "
        "analyze and summarize"
        "the most praised elements with insight. Your task is to extract deeper feedback trends that reflect what the "
        "audience appreciated."
        "List these as bullet points. Each bullet point must start with a bolded subtopic (e.g., **Clarity**) "
        "followed by a concise 1–2 sentence"
        "explanation of why this was positively received. Do not quote comments directly. Do not provide introductory "
        "or concluding sentences."
        "Do not group points or use themes. Be objective and informative. Note only use insights from comments, "
        "not your simulation.\n\nComments:\n{comments}"
    )

    IMPROVEMENT_PROMPT = (
        "You are a professional video content analyst. Given the following YouTube comments about a video, "
        "analyze and summarize"
        "the most commonly mentioned criticisms or suggestions for improvement. Your task is to extract deeper "
        "insight into what viewers found lacking."
        "List these as bullet points. Each bullet point must start with a bolded subtopic (e.g., **Pacing**) followed "
        "by a concise 1–2 sentence"
        "explanation of the issue. Do not quote comments directly. Do not provide introductory or concluding sentences."
        "Do not group points or use themes. Be direct, clear, and objective.Note only use insights from comments, "
        "not your simulation.\n\nComments:\n{comments}"
    )

    def analyze(self, comments: List[str]) -> Optional[Dict[str, str]]:
        try:
            model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
            comments_text = "\n".join(comments)
            # Generate positive feedback
            prompt_working = FeedbackExtractor.WORKS_PROMPT.format(comments=comments_text)
            res_working = model.generate_content(prompt_working)
            what_works = res_working.text.strip()
            # Generate improvement feedback
            prompt_needs = FeedbackExtractor.IMPROVEMENT_PROMPT.format(comments=comments_text)
            res_needs = model.generate_content(prompt_needs)
            needs_improvement = res_needs.text.strip()
            print(what_works,needs_improvement)
            return {"what_works": what_works, "needs_improvement": needs_improvement}
        except Exception as e:
            print(f"[ERROR] Feedback extraction failed: {e}")
            return None
