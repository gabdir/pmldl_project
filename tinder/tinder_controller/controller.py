from time import sleep
from selenium import webdriver

from tinder.decision_making import Decision, make_decision


class TinderController:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://tinder.com')
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

    def extract_picture(self):
        """
        Exctracts current picture on the page
        """
        pic_element = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/span[1]/div/@style')
        # pic_element.

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
            self.swipe()

    def start_dataset_collecting(self):
        """
        Entry point for a controller to start data collection process
        """
        pass