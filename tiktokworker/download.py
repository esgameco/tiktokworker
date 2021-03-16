import random
import string
from pathlib import Path
from TikTokApi import TikTokApi
from mongoengine import NotUniqueError

from typing import List

import tiktokworker.models as md

class Downloader():
    def __init__(self):
        self.verifyFp = "verify_" + ''.join(random.choice(string.ascii_letters) for num in range(40))
        self.did = ''.join(random.choice(string.digits) for num in range(19))
        self.tiktok_api = TikTokApi.get_instance(custom_verifyFp=self.verifyFp)

    def download_video(self, path: Path, url: str) -> None:
        # b = api.get_Video_By_TikTok(, custom_did=did) # Uses whole dictionary instead of just url
        video_bytes = api.get_Video_By_DownloadURL(url, custom_did=self.did)
        open(path, "wb").write(video_bytes)
    
    def get_by_hashtag(self, hashtag: str, number: int = 20) -> List[md.Video]:
        videos = list()
        for video_info in self.tiktok_api.byHashtag(hashtag, count=number, custom_did=self.did):
            video = md.Video(
                title=video_info['desc'],
                video_id=video_info['id'],
                url=video_info['video']['downloadAddr'],
                found_hashtag=hashtag
            )
            try:
                video.save() # TODO: Is this necessary?
            except NotUniqueError:
                pass
            videos.append(video)
        return videos