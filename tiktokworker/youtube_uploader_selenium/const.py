"""A class for storing constants for YoutubeUploader class"""
YOUTUBE_URL = 'https://www.youtube.com'
YOUTUBE_STUDIO_URL = 'https://studio.youtube.com'
YOUTUBE_UPLOAD_URL = 'https://www.youtube.com/upload'
USER_WAITING_TIME = 10
VIDEO_TITLE = 'title'
VIDEO_DESCRIPTION = 'description'
VIDEO_TAGS = 'tags'
DESCRIPTION_CONTAINER = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/' \
                        'ytcp-uploads-details/div/ytcp-uploads-basics/ytcp-mention-textbox[2]'
MORE_OPTIONS_CONTAINER = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/' \
                         'ytcp-uploads-details/div/div/ytcp-button/div'
TEXTBOX = 'textbox'
TEXT_INPUT = 'text-input'
RADIO_LABEL = 'radioLabel'
STATUS_CONTAINER = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/' \
                   'div/div[1]/ytcp-video-upload-progress/span'
NOT_MADE_FOR_KIDS_LABEL = 'NOT_MADE_FOR_KIDS'

# NEW
DESCRIPTION_SELECTOR = 'ytcp-mention-textbox.style-scope:nth-child(2) > ytcp-form-input-container:nth-child(1) > div:nth-child(1) > div:nth-child(3) > ytcp-mention-input:nth-child(1)'

# Monetization
MONETIZATION_LABEL = 'm10n-container'
MONETIZATION_ON_LABEL = 'radio-on'
MONETIZATION_DONE = 'save-button'
MONETIZATION_SUITABILITY_LABEL = 'all-none-checkbox'
PUBLISH_ANYWAY_LABEL = 'publish-button'

NEXT_BUTTON = 'next-button'
PUBLIC_BUTTON = 'PUBLIC'
VIDEO_URL_CONTAINER = "//span[@class='video-url-fadeable style-scope ytcp-video-info']"
VIDEO_URL_ELEMENT = "//a[@class='style-scope ytcp-video-info']"
HREF = 'href'
UPLOADED = 'Uploading'
ERROR_CONTAINER = '//*[@id="error-message"]'
VIDEO_NOT_FOUND_ERROR = 'Could not find video_id'
DONE_BUTTON = 'done-button'
INPUT_FILE_VIDEO = "//input[@type='file']"

ADVANCED_BUTTON = 'advanced-button'
TOGGLE_BUTTON = 'toggle-button'
TAGS_CONTAINER = 'tags-container'
