import os
from pathlib import Path

import tiktokworker as ttw

client = ttw.client.Client()
client.test_download(Path(os.getenv('TEST_PATH')))