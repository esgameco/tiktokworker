"""This module implements uploading videos on YouTube via Selenium using metadata JSON file
    to extract its title, description etc."""

from typing import DefaultDict, Optional
from selenium_firefox.firefox import Firefox, By, Keys
from collections import defaultdict
import json
import time
from youtube_uploader_selenium import const
from pathlib import Path
import logging
import random

logging.basicConfig()


def load_metadata(metadata_json_path: Optional[str] = None) -> DefaultDict[str, str]:
    if metadata_json_path is None:
        return defaultdict(str)
    with open(metadata_json_path) as metadata_json_file:
        return defaultdict(str, json.load(metadata_json_file))


class YouTubeUploader:
    """A class for uploading videos on YouTube via Selenium using metadata JSON file
    to extract its title, description etc"""

    def __init__(self, video_path: str, metadata: dict, browser: Firefox) -> None:
        self.video_path = video_path
        self.metadata_dict = metadata
        self.browser = browser
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self._validate_inputs()

    def _validate_inputs(self):
        if not self.metadata_dict[const.VIDEO_TITLE]:
            self.logger.warning("The video title was not found in a metadata file")
            self.metadata_dict[const.VIDEO_TITLE] = Path(self.video_path).stem
            self.logger.warning("The video title was set to {}".format(Path(self.video_path).stem))
        if not self.metadata_dict[const.VIDEO_DESCRIPTION]:
            self.logger.warning("The video description was not found in a metadata file")

    def upload(self, use_monetization=True):
        try:
            self._login()
            return self._upload(use_monetization)
        except Exception as e:
            print(e)
            self._quit()
            raise

    def _wait(self):
        time.sleep(const.USER_WAITING_TIME + random.uniform(0, 2))
    
    def _short_wait(self):
        time.sleep(random.uniform(0, 1))

    def _login(self):
        self.browser.get(const.YOUTUBE_URL)
        self._wait()

        if self.browser.has_cookies_for_current_website():
            self.browser.load_cookies()
            self._wait()
            self.browser.refresh()
        else:
            self.logger.info('Please sign in and then press enter')
            input()
            self.browser.get(const.YOUTUBE_URL)
            self._wait()
            self.browser.save_cookies()

    def _upload(self, use_monetization: bool) -> (bool, Optional[str]):
        self._go_to_upload()
        self._send_video()
        self._wait()

        self._set_title()
        self._set_description()
        self._set_kids_section()

        # self._set_tags()

        self._click_next()

        # Monetization
        if use_monetization:
            self._set_monetization_on()
            self._click_next()

            self._set_monetization_suitability()
            self._click_next()
            self._click_next()
        else:
            self._click_next()

        try:
            self._set_video_public()
        except Exception:
            # Deals with copyright 'checks'
            self._click_next()
            self._set_video_public()

        video_id = self._get_video_id()

        self._wait_while_upload()

        done_button = self.browser.find(By.ID, const.DONE_BUTTON)

        # Catch such error as
        # "File is a duplicate of a video you have already uploaded"
        if done_button.get_attribute('aria-disabled') == 'true':
            error_message = self.browser.find(By.XPATH,
                                              const.ERROR_CONTAINER).text
            self.logger.error(error_message)
            return False, None

        done_button.click()
        self._wait()

        # Monetization
        if use_monetization:
            self._publish_anyway()

        self.logger.debug("Published the video with video_id = {}".format(video_id))
        self._wait()
        self.browser.get(const.YOUTUBE_URL)
        self._quit()
        return True, video_id

    def _go_to_upload(self):
        self.browser.get(const.YOUTUBE_URL)
        self._wait()
        self.browser.get(const.YOUTUBE_UPLOAD_URL)
        self._wait()

    def _send_video(self):
        absolute_video_path = str(Path.cwd() / self.video_path)
        self.browser.find(By.XPATH, const.INPUT_FILE_VIDEO).send_keys(absolute_video_path)
        self.logger.debug('Attached video {}'.format(self.video_path))

    def _set_title(self):
        title_field = self.browser.find(By.ID, const.TEXTBOX, timeout=10)
        title_field.click()
        self._short_wait()
        title_field.clear()
        self._short_wait()
        title_field.send_keys(Keys.COMMAND + 'a')
        self._short_wait()
        title_field.send_keys(self.metadata_dict[const.VIDEO_TITLE])
        self.logger.debug('The video title was set to \"{}\"'.format(self.metadata_dict[const.VIDEO_TITLE]))
        self._wait()

    def _set_description(self):
        video_description = self.metadata_dict[const.VIDEO_DESCRIPTION]
        if video_description:
            description_container = self.browser.find(By.CSS_SELECTOR,
                                                      const.DESCRIPTION_SELECTOR)
            description_field = self.browser.find(By.ID, const.TEXTBOX, element=description_container)
            description_field.click()
            self._wait()
            description_field.clear()
            self._wait()
            description_field.send_keys(self.metadata_dict[const.VIDEO_DESCRIPTION].replace('\\n', u'\ue007'))
            self.logger.debug(
                'The video description was set to \"{}\"'.format(self.metadata_dict[const.VIDEO_DESCRIPTION]))

    def _set_kids_section(self):
        kids_section = self.browser.find(By.NAME, const.NOT_MADE_FOR_KIDS_LABEL)
        self.browser.find(By.ID, const.RADIO_LABEL, kids_section).click()
        self.logger.debug('Selected \"{}\"'.format(const.NOT_MADE_FOR_KIDS_LABEL))

    def _set_tags(self):
        more_options = self.browser.find(By.CLASS_NAME, const.ADVANCED_BUTTON)
        # more_options = self.browser.find(By.CLASS_NAME, const.TOGGLE_BUTTON)
        more_options.click()
        self._wait()
        self._wait()

        tags_container = self.browser.find(By.ID, const.TAGS_CONTAINER)
        tags_container.click()
        tags_input = tags_container.find_element(By.ID, const.TEXT_INPUT)
        tags_input.click()
        self._wait()
        tags_input.send_keys(self.metadata_dict[const.VIDEO_TAGS])
        self._wait()
    
    def _set_monetization_on(self):
        monetization_bar = self.browser.find(By.ID, const.MONETIZATION_LABEL)
        monetization_bar.click()
        self._wait()

        on_label = self.browser.find(By.ID, const.MONETIZATION_ON_LABEL)
        on_label.click()
        self._wait()

        done_button = self.browser.find(By.ID, const.MONETIZATION_DONE)
        done_button.click()
        self._wait()
        self.logger.debug(
                'The video monetization was set to on')

    def _set_monetization_suitability(self):
        button = self.browser.find(By.CLASS_NAME, const.MONETIZATION_SUITABILITY_LABEL)
        button.click()
        self._wait()
        self.logger.debug(
                'The video monetization was set to none of the above')
    
    def _publish_anyway(self):
        button = self.browser.find(By.ID, const.PUBLISH_ANYWAY_LABEL)
        button.click()
        self._wait()
        self.logger.debug(
                'The video published publicly')

    def _click_next(self):
        self.browser.find(By.ID, const.NEXT_BUTTON).click()
        self.logger.debug('Clicked {}'.format(const.NEXT_BUTTON))
        self._wait()

    def _set_video_public(self):
        public_main_button = self.browser.find(By.NAME, const.PUBLIC_BUTTON)
        self.browser.find(By.ID, const.RADIO_LABEL, public_main_button).click()
        self._wait()
        self.logger.debug('Made the video {}'.format(const.PUBLIC_BUTTON))

    def _wait_while_upload(self):
        status_container = self.browser.find(By.XPATH,
                                             const.STATUS_CONTAINER)
        while True:
            in_process = status_container.text.find(const.UPLOADED) != -1
            if in_process:
                self._wait()
            else:
                break

    def _get_video_id(self) -> Optional[str]:
        video_id = None
        try:
            video_url_container = self.browser.find(By.XPATH, const.VIDEO_URL_CONTAINER)
            video_url_element = self.browser.find(By.XPATH, const.VIDEO_URL_ELEMENT,
                                                  element=video_url_container)
            video_id = video_url_element.get_attribute(const.HREF).split('/')[-1]
        except:
            self.logger.warning(const.VIDEO_NOT_FOUND_ERROR)
            pass
        return video_id

    def _quit(self):
        self.browser.driver.quit()
    
    @staticmethod
    def _try(func):
        def newfunc():
            try:
                func()
            except Exception:
                pass
        return newfunc
