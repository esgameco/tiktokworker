import os

import tiktokworker as ttw

print(ttw)
client = ttw.client.Client()
client.test_download(os.getenv('TEST_PATH'))