import re
from typing import List


class DataPreprocessor:
    @staticmethod
    def remove_filler_words(transcript: str) -> str:
        """Removes common filler words from the transcript"""
        fillers = ["um", "uh", "like", "you know", "so", "actually", "basically", "literally", "right"]
        pattern = r'\b(' + '|'.join(fillers) + r')\b'
        cleaned_transcript = re.sub(pattern, '', transcript, flags=re.IGNORECASE)
        return cleaned_transcript

    @staticmethod
    def clean_transcript(raw_transcript: str) -> str:
        """Cleans transcript by removing timestamps, filler words, and spam content"""
        cleaned = re.sub(r'\[\d+:\d+(?::\d+)?]', '', raw_transcript)  # Remove timestamps
        cleaned = DataPreprocessor.remove_filler_words(cleaned)  # Remove filler words
        return cleaned.lower()

    @staticmethod
    def filter_comments(raw_comments: List[str]) -> List[str]:
        # Remove duplicate comments
        seen = set()
        filtered = []
        # Remove spam content using regex patterns
        spam_patterns = [
            r'\b(free|subscribe|click here|visit our website|spam)\b',
            r'(http|https)://\S+',  # URLs
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',  # Emails
            r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'  # IP addresses
        ]

        for comment in raw_comments:
            if comment and comment not in seen:
                for pattern in spam_patterns:
                    comment = re.sub(pattern, '', comment, flags=re.IGNORECASE)
                seen.add(comment)
                filtered.append(comment)
        return filtered
