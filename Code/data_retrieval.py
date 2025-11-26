from youtubeAPICon import YouTubeAPICon
from data_preprocessor import DataPreprocessor
import re


class DataRetrieval:
    def __init__(self, api_key: str, video_url: str):
        self.api = YouTubeAPICon(api_key)
        self.video_url = video_url
        self.video_id = None

    def validate_url(self):
        """Validate YouTube URL and extract video ID"""
        pattern = r"^https?://(www\.)?(youtube\.com|youtu\.be)/(watch\?v=)?([a-zA-Z0-9_-]{11})"
        match = re.match(pattern, self.video_url)
        if not match:
            raise ValueError("Invalid YouTube URL")
        self.video_id = match.group(4)

    def get_metadata(self) -> dict:
        """Fetch and return video metadata"""
        if not self.video_id:
            raise RuntimeError("URL validation required before data retrieval")
        metadata = self.api.fetch_metadata(self.video_id)
        # Enforce operational constraints
        if metadata["duration"].startswith("PT") and "H" in metadata["duration"]:  # Checks for 1+ hour videos
            raise ValueError("Video exceeds the allowed duration of 1 hour")

        return metadata

    def get_transcript(self) -> str:
        """Fetch and return cleaned transcript"""
        if not self.video_id:
            raise RuntimeError("URL validation required before data retrieval")
        raw_transcript = self.api.fetch_transcript(self.video_id)
        return DataPreprocessor.clean_transcript(raw_transcript)

    def get_comments(self) -> list[str]:
        """Fetch and return filtered comments"""
        if not self.video_id:
            raise RuntimeError("URL validation required before data retrieval")
        raw_comments = self.api.fetch_comments(self.video_id, max_comments=500)

        if len(raw_comments) < 100:
            raise ValueError("Video does not have the required minimum of 100 comments")

        return DataPreprocessor.filter_comments(raw_comments)
