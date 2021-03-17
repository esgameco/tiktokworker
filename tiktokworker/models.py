from pathlib import Path
from mongoengine import Document, EmbeddedDocument, StringField, URLField, BooleanField, ListField, ReferenceField, DictField

from typing import List

class Video(Document):
    title = StringField(default='')
    video_id = StringField(required=True, unique=True)
    video_info = DictField()
    found_hashtag = StringField(default='')

    used = BooleanField(default=False)

    def download(self, path: Path, downloader) -> None:
        downloader.download_video(f'{path}.mp4', self.video_info)


class Compilation(Document):
    title = StringField(default='')
    hashtag = StringField(default='')

    videos = ListField(ReferenceField(Video), required=True)

    completed = BooleanField(default=False)
    working = BooleanField(default=False)

    def download_videos(self, dir_path: Path, downloader) -> None:
        for video in self.videos:
            video.download(dir_path / video.video_id, downloader)