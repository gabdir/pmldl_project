import os
import hashlib
import random
import threading
import requests
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from pathlib import Path

from tinder.decision_making import Decision, make_decision


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
        span_like = self.driver.find_element_by_xpath("//span[text()='Like'][@class='Hidden']")
        like_btn = span_like.find_element_by_xpath('../..')
        like_btn.click()

    def dislike(self):
        """
        Finds dislike button on the page and click on it
        """
        span_dislike = self.driver.find_element_by_xpath("//span[text()='Nope'][@class='Hidden']")
        dislike_btn = span_dislike.find_element_by_xpath('../..')
        dislike_btn.click()

    def close_popup(self):
        """
        Sometimes after swipe there can be the suggestion on upgrading

        Finds 'NO THANKS' button and clicks on it to return to photos swiping
        """
        try:
            span_no_thanks = self.driver.find_element_by_xpath("//span[text()='No Thanks']")
        except NoSuchElementException:
            try:
                span_not_interested = self.driver.find_element_by_xpath("//span[text()='Not interested']")
            except NoSuchElementException:
                raise NoSuchElementException
            else:
                not_interested_btn = span_not_interested.find_element_by_xpath('..')
                not_interested_btn.click()
        else:
            no_thanks_btn = span_no_thanks.find_element_by_xpath('..')
            no_thanks_btn.click()

    def close_match(self):
        """
        Sometimes after swipe there can happen a match

        Finds button 'CLOSE' and clicks on it to return to photos swiping
        """
        match_btn = self.driver.find_element_by_css_selector("button[title='Back to Tinder']")
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
        except ElementClickInterceptedException:
            raise OutOfSwipes from None

    def extract_picture_link(self, folder: Path):
        """
        Return url of the image and path to save
        """
        PIC_SELECTOR = "div[class$='StretchedBox'][style^='background-image']"
        pic_element = self.driver.find_elements_by_css_selector(PIC_SELECTOR)[1]
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

        return url, path_to_save

    def save_picture(self, url: str, path_to_save: Path, timeout: int=60):
        """
        Downloads picture from given url and saves it according to given path
        """
        try:
            response = requests.get(url, timeout=timeout)
        except ConnectionError:
            print('Problems with connection')
            return

        if response.status_code == 200:
            with open(path_to_save, 'wb') as f:
                for chunk in response:
                    f.write(chunk)

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

        def collect(folder, action):
            try:
                url, path_to_save = self.extract_picture_link(folder)
            except NoSuchElementException:
                print('WTF are you swiping, I cannot even see a picture')
                return

            try:
                action()
            except (NoSuchElementException, ElementClickInterceptedException):
                print('WTF are you doing, I cannot see buttons')
                return

            threading.Thread(target=self.save_picture, args=(url, path_to_save)).start()

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
                print('Liked!!!')
            elif input_ == Decision.DISLIKE:
                print('Disliked :(')

            return input_

        print('You are in dataset collection mode! Go to the page where you are swiping girls')

        liked_folder = Path(dataset_folder) / 'liked'
        disliked_folder = Path(dataset_folder) / 'disliked'
        liked_folder.mkdir(parents=True, exist_ok=True)
        disliked_folder.mkdir(parents=True, exist_ok=True)

        print('Waiting...')

        is_like_available = False
        while not is_like_available:
            try:
                span_like = self.driver.find_element_by_xpath("//span[text()='Like'][@class='Hidden']")
            except NoSuchElementException:
                pass
            else:
                is_like_available = True

        while True:
            input_ = prompt()
            if input_ == Decision.LIKE:
                args = (liked_folder, self.like)
            else:
                args = (disliked_folder, self.dislike)
            collect(*args)
