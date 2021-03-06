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

    def download_video(self, path: Path, video_info: dict) -> None:
        video_bytes = self.tiktok_api.get_Video_By_TikTok(video_info, custom_did=self.did)
        open(path, "wb").write(video_bytes)
    
    def get_by_hashtag(self, hashtag: md.Hashtag, number: int = 20) -> List[md.Video]:
        videos = list()
        for video_info in self.tiktok_api.byHashtag(hashtag, 
                                                    count=number, 
                                                    offset=int((hashtag.videos_used-1)%number)+1
                                                    custom_did=self.did):
            video = md.Video.get_video(hashtag, video_info)
            videos.append(video)
        return videos