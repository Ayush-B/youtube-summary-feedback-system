from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List, Dict
from base_analyzer import BaseAnalyzer


class SentimentAnalyzer(BaseAnalyzer):
    """Classifies comments as positive, negative, or neutral using VADER."""

    def __init__(self):
        super().__init__()
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, comments: List[str]) -> Dict[str, List[str]]:
        """Classifies comments into sentiment categories using VADER."""
        sentiment_results = {"positive": [], "negative": [], "neutral": []}

        for comment in comments:
            score = self.analyzer.polarity_scores(comment)['compound']
            if score >= 0.05:
                sentiment_results["positive"].append(comment)
            elif score <= -0.05:
                sentiment_results["negative"].append(comment)
            else:
                sentiment_results["neutral"].append(comment)

        return sentiment_results
