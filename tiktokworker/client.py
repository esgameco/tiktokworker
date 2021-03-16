from pathlib import Path

import tiktokworker.models as md
import tiktokworker.download as dl

class Client():
    def __init__(self):
        self.downloader = dl.Downloader()
    
    def test_download(self, path: Path) -> None:
        compilation = self.create_hashtag_compilation('19 dollar fornite card')
        compilation.download_videos(path, self.downloader)
    
    def create_hashtag_compilation(self, hashtag: str) -> md.Compilation:
        videos = self.downloader.get_by_hashtag(hashtag)
        compilation = md.Compilation(title='test',
                                    hashtag=hashtag,
                                    videos=videos)
        compilation.save()
        return compilation