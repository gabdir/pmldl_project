import os
import urllib.request
import hashlib
import random
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from pathlib import Path

from tinder.decision_making import Decision, make_decision
from ._xpathes import LIKE_BTN_XPATH, DISLIKE_BTN_XPATH


class OutOfSwipes(Exception):
    """Exception for situation when daily limit of swipes is exceeded"""


class TinderController:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://tinder.com')
        print('Please login into your account')

    def like(self):
        """
        Finds like button on the page and click on it
        """
        like_btn = self.driver.find_element_by_xpath(LIKE_BTN_XPATH)
        like_btn.click()

    def dislike(self):
        """
        Finds dislike button on the page and click on it
        """
        dislike_btn = self.driver.find_element_by_xpath(DISLIKE_BTN_XPATH)
        dislike_btn.click()

    def close_popup(self):
        """
        Sometimes after swipe there can be the suggestion on upgrading

        Finds 'NO THANKS' button and clicks on it to return to photos swiping
        """
        try:
            no_thanks_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/button[2]')
        except NoSuchElementException:
            try:
                not_interested_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
            except NoSuchElementException:
                raise NoSuchElementException
            else:
                not_interested_btn.click()
        else:
            no_thanks_btn.click()

    def close_match(self):
        """
        Sometimes after swipe there can happen a match

        Finds button 'CLOSE' and clicks on it to return to photos swiping
        """
        match_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[4]/button')
        match_btn.click()

    def action(self, act):
        """
        Makes action based on given decision
        """
        try:
            if act == Decision.LIKE:
                self.like()
            elif act == Decision.DISLIKE:
                self.dislike()
            else:
                print('Unknown action')
        except NoSuchElementException:
            try:
                self.close_popup()
            except NoSuchElementException:
                self.close_match()

    def save_picture(self, folder: Path):
        """
        Exctracting a picture from current page and saving it to a given folder
        """
        pic_element = self.driver.find_element_by_xpath('//*[@id="t-339552546"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/span[1]/div')
        background_image = pic_element.get_attribute('style').split('; ')[0]
        start = background_image.find('"') + 1
        end = background_image.rfind('"')
        url = background_image[start:end]
        _, img_extension = os.path.splitext(url)
        url_hash = hashlib.md5(url.encode()).hexdigest()[-5:]
        path_to_save = folder / (url_hash + img_extension)
        while os.path.isfile(path_to_save):
            url_hash += random.randint(0, 9)
            path_to_save = folder / (url_hash + img_extension)
        urllib.request.urlretrieve(url, path_to_save)

    def extract_picture(self):
        """
        Exctracts current picture on the page
        """
        try:
            pic_element = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/span[1]/div')
        except Exception:
            raise OutOfSwipes from None
        else:
            background_image = pic_element.get_attribute('style').split('; ')[0]
            start = background_image.find('"') + 1
            end = background_image.rfind('"')
            url = background_image[start:end]
            _, img_extension = os.path.splitext(url)
            urllib.request.urlretrieve(url, str(self.image_counter) + img_extension)

    def swipe(self):
        """
        Encapsulates logic for one swipe
        """
        picture = self.extract_picture()
        self.action(make_decision(picture))


    def start_swiping(self):
        """
        Entry point for a controller to start swiping
        """
        while True:
            sleep(0.5)
            try:
                self.swipe()
            except OutOfSwipes:
                print('Seems we have reached a daily limit of swipes :(')
                break

    def start_dataset_collecting(self, dataset_folder):
        """
        Entry point for a controller to start data collection process
        """

        def prompt():
            """
            Helper function to process input from the user
            """
            prompt_string = f'Like({int(Decision.LIKE)}) or Dislike({int(Decision.DISLIKE)}): '

            try:
                input_ = int(input(prompt_string))
            except ValueError:
                input_ = None
            
            while not (input_ == Decision.LIKE or input_ == Decision.DISLIKE):
                try:
                    input_ = int(input(prompt_string))
                except ValueError:
                    input_ = None

            if input_ == Decision.LIKE:
                print('You liked the girl !!!')
            elif input_ == Decision.DISLIKE:
                print('You disliked the girl :(')

            return input_

        print('You are in dataset collection mode')

        liked_folder = Path(dataset_folder) / 'liked'
        disliked_folder = Path(dataset_folder) / 'disliked'
        liked_folder.mkdir(parents=True, exist_ok=True)
        disliked_folder.mkdir(parents=True, exist_ok=True)

        while True:
            input_ = prompt()

            if input_ == Decision.LIKE:
                self.save_picture(liked_folder)
                self.like()
            elif input_ == Decision.DISLIKE:
                self.save_picture(disliked_folder)
                self.dislike()
