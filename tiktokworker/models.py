from pathlib import Path
from mongoengine import Document, EmbeddedDocument, StringField, URLField, BooleanField, ListField, ReferenceField, DictField, IntField

from typing import List


class Hashtag(Document):
    name = StringField(required=True)
    times_uploaded = IntField(default=0)
    videos_used = IntField(default=0)

    @staticmethod
    def get_hashtag(hashtag: str) -> Hashtag:
        try:
            return Hashtag.objects(name=hashtag)[0]
        except:
            hashtag_object = Hashtag(name=hashtag)
            hashtag_object.save()
            return hashtag_object


class Video(Document):
    title = StringField(default='')
    video_id = StringField(required=True, unique=True)
    video_info = DictField()
    found_hashtag = StringField(default='')

    used = BooleanField(default=False)

    @staticmethod
    def get_video(hashtag: Hashtag, video_info: dict) -> Video:
        try:
            return md.Video.objects(video_id=video_info['id'])[0]
        except:
            video = md.Video(
                title=video_info['desc'],
                video_id=video_info['id'],
                found_hashtag=hashtag,
                video_info=video_info
            )
            video.save()
            return video

    def download(self, path: Path, downloader) -> None:
        downloader.download_video(f'{path}.mp4', self.video_info)


class Compilation(Document):
    title = StringField(default='')
    hashtag = ReferenceField(Hashtag, required=True)

    videos = ListField(ReferenceField(Video), required=True)

    completed = BooleanField(default=False)
    working = BooleanField(default=False)

    def download_videos(self, dir_path: Path, downloader) -> None:
        for video in self.videos:
            video.download(dir_path / video.video_id, downloader)