import os
from mongoengine import connect

import tiktokworker.client
import tiktokworker.download
import tiktokworker.models

connect(host=os.getenv('MONGO_URI'))