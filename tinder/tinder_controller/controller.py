import os
import urllib.request
from time import sleep
from selenium import webdriver

from tinder.decision_making import Decision, make_decision


class OutOfSwipes(Exception):
    """Exception for situation when daily limit of swipes is exceeded"""


class TinderController:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://tinder.com')
        self.image_counter = 0
        print('Please login into your account')

    def like(self):
        """
        Finds like button on the page and click on it
        """
        like_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like_btn.click()

    def dislike(self):
        """
        Finds dislike button on the page and click on it
        """
        dislike_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')
        dislike_btn.click()

    def close_popup(self):
        """
        Sometimes after swipe there can be the suggestion on upgrading

        Finds 'NO THANKS' button and clicks on it to return to photos swiping
        """
        no_thanks_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/button[2]')
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
        except Exception:
            try:
                self.close_popup()
            except Exception:
                self.close_match()

    def extract_picture(self, mode='swipe'):
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
            self.image_counter += 1

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

    def start_dataset_collecting(self):
        """
        Entry point for a controller to start data collection process
        """
        pass