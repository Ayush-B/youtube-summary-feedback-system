from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Dict, List


class YouTubeAPICon:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def fetch_metadata(self, video_id: str) -> Dict[str, str]:
        try:
            response = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            ).execute()
            items = response.get('items', [])
            if not items:
                raise ValueError("Video not found")

            metadata = items[0]
            return {
                "title": metadata['snippet']['title'],
                "duration": metadata['contentDetails']['duration'],
                "views": metadata['statistics']['viewCount'],
                "likes": metadata['statistics'].get('likeCount', '0'),
                "dislikes": metadata['statistics'].get('dislikeCount', '0')
            }
        except HttpError as e:
            raise ConnectionError(f"Metadata API error: {e.resp.status}") from e

    def fetch_comments(self, video_id: str, max_comments: int = 3000) -> List[str]:
        """Fetch up to max_comments (default 3000) top-level comments from YouTube API"""
        comments = []
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100  # Fetch 100 comments per page (max allowed by YouTube API)
            )
            while request and len(comments) < max_comments:
                response = request.execute()
                for item in response['items']:
                    comments.append(
                        item['snippet']['topLevelComment']['snippet']['textDisplay']
                    )
                    if len(comments) >= max_comments:
                        break  # Stop fetching more comments once limit is reached

                # Check if there are more pages of comments
                if 'nextPageToken' in response and len(comments) < max_comments:
                    request = self.youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        textFormat="plainText",
                        maxResults=100,
                        pageToken=response['nextPageToken']
                    )
                else:
                    break  # No more pages, exit loop

            return comments
        except HttpError as e:
            raise ConnectionError(f"Comments API error: {e.resp.status}") from e

    def fetch_transcript(self, video_id: str) -> str:
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = ' '.join([entry['text'] for entry in transcript_list])
            return transcript
        except Exception as e:
            return f"Transcript unavailable: {str(e)}"