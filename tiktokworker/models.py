from pathlib import Path
from mongoengine import Document, StringField, URLField, BooleanField, ListField

class Video(Document):
    title = StringField(default='')
    video_id = StringField(required=True, unique=True)
    url = URLField(required=True, unique=True)
    found_hashtag = StringField(default='')

    used = BooleanField(default=False)

    def download(self, path: Path, downloader) -> None:
        downloader.download_video(path, self.url)


class Compilation(Document):
    title = StringField(default='')
    hashtag = StringField(default='')

    videos = ListField(Video(), required=True)

    completed = BooleanField(default=False)
    working = BooleanField(default=False)

    def download_videos(self, dir_path: Path, downloader) -> None:
        for video in self.videos:
            video.download(dir_path / video.video_id, downloader)