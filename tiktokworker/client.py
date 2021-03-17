import random
import string
from pathlib import Path

import tiktokworker.models as md
import tiktokworker.download as dl

class Client():
    def __init__(self):
        self.downloader = dl.Downloader()
    
    def test_download(self, path: Path) -> None:
        hashtag = self.downloader.tiktok_api.search_for_hashtags(''.join(random.choice(string.ascii_letters) for num in range(10)))[0]['challenge']['title']
        compilation = self.create_hashtag_compilation(hashtag)
        compilation.download_videos(path, self.downloader)
    
    def create_hashtag_compilation(self, hashtag: str) -> md.Compilation:
        videos = self.downloader.get_by_hashtag(hashtag)
        compilation = md.Compilation(title='test',
                                     hashtag=hashtag,
                                     videos=videos)
        for video in videos:
            print(video.title)
        compilation.save()
        return compilation