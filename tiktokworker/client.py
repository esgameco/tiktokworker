import random
import string
from youtube_uploader_selenium import YouTubeUploader
from pathlib import Path

import tiktokworker.models as md
import tiktokworker.download as dl

class Client():
    def __init__(self):
        self.downloader = dl.Downloader()
    
    def test_download(self, path: Path) -> None:
        # hashtag = self.downloader.tiktok_api.search_for_hashtags(''.join(random.choice(string.ascii_letters) for num in range(10)))[0]['challenge']['title']
        hashtag = 'roblox'
        compilation = self.create_hashtag_compilation(hashtag)
        compilation.download_videos(path, self.downloader)

    # def test_upload(self, path: Path) -> None:
    #     uploader = YouTubeUploader()
    
    def create_hashtag_compilation(self, hashtag_str: str) -> md.Compilation:
        hashtag = md.Hashtag.get_hashtag(hashtag_str)
        videos = self.downloader.get_by_hashtag(hashtag)
        compilation = md.Compilation(title=f'Roblox TikTok Compilation #{hashtag.times_uploaded+1}',
                                     hashtag=hashtag,
                                     videos=videos)
        for video in videos:
            print(video.title)
        compilation.save()
        return compilation