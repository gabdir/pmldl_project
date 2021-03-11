import os
import hashlib
import random
import threading
import requests
from time import sleep
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException

from tinder.decision_making import Decision, make_decision, Model
from tinder.conversations import get_first_message, get_answer


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

    def go_to_matches(self):
        """
        Change left side of the page on current matches
        """
        btn = self.driver.find_element_by_xpath("//button[text()='Matches']")
        btn.click()

    def go_to_messages(self):
        """
        Change left side of the page on messages
        """
        btn = self.driver.find_element_by_xpath("//button[text()='Messages']")
        btn.click()

    def go_to_swipes(self):
        """
        From messages go back to swipes
        """
        try:
            btn = self.driver.find_element_by_xpath("//button[@aria-label='Close']")
        except NoSuchElementException:
            pass
        else:
            btn.click()

    def close_popup(self):
        """
        Sometimes after swipe there can be the suggestion on upgrading, matches and other popups
        """
        try:
            span_no_thanks = self.driver.find_element_by_xpath("//span[text()='No Thanks']")
            no_thanks_btn = span_no_thanks.find_element_by_xpath('..')
            no_thanks_btn.click()
        except (NoSuchElementException, StaleElementReferenceException):
            try:
                span_not_interested = self.driver.find_element_by_xpath("//span[text()='Not interested']")
                not_interested_btn = span_not_interested.find_element_by_xpath('..')
                not_interested_btn.click()
            except (NoSuchElementException, StaleElementReferenceException):
                try:
                    span_remind_later = self.driver.find_element_by_xpath("//span[text()='Remind me again later']")
                    remind_later_btn = span_remind_later.find_element_by_xpath('..')
                    remind_later_btn.click()
                except (NoSuchElementException, StaleElementReferenceException):
                    try:
                        match_btn = self.driver.find_element_by_css_selector("button[title='Back to Tinder']")
                        match_btn.click()
                    except (NoSuchElementException, StaleElementReferenceException):
                        pass

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
            self.close_popup()
        except ElementClickInterceptedException:
            raise OutOfSwipes from None

    def extract_picture(self):
        """
        Get url of the picture on the page
        """
        PIC_SELECTOR = "div[class$='StretchedBox'][style^='background-image']"
        pic_element = self.driver.find_elements_by_css_selector(PIC_SELECTOR)[1]
        background_image = pic_element.get_attribute('style').split('; ')[0]
        start = background_image.find('"') + 1
        end = background_image.rfind('"')
        url = background_image[start:end]

        return url

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
            url_hash += str(random.randint(0, 9))
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

    def send_message(self, msg=None):
        """
        When on page with textarea send message
        """
        if msg is None:
            msg = get_first_message()
        textarea = self.driver.find_element_by_xpath("//textarea[@placeholder='Type a message']")
        textarea.send_keys(msg)
        sleep(1) # to make sure message is ready
        span_send = self.driver.find_element_by_xpath("//span[text()='Send']")
        send_btn = span_send.find_element_by_xpath('..')
        send_btn.click()
        sleep(1)

    def go_through_matches_and_message(self):
        """
        Go through all matches and text them first message
        """
        print('Checking matches ...')
        while True:
            try:
                self.go_to_matches()
            except NoSuchElementException:
                return
            else:
                sleep(3)
                matches = self.driver.find_elements_by_xpath("//a[starts-with(@class, 'matchListItem')]")
                matches = list(filter(lambda m: m.get_attribute('href') != 'https://tinder.com/app/likes-you', matches))
                try:
                    match = matches.pop(0)
                except IndexError:
                    break
                else:
                    match.click()
                    sleep(2) # to make sure place with messages loaded
                    self.send_message()

    def process_conversation(self):
        """
        Process a dialog with one person

        Collects chain of messages and answer if needed
        """

        ME = 'fff'

        dialog = []
        owner = []

        messages = self.driver.find_elements_by_xpath("//span[starts-with(@class, 'text')]")

        for msg in messages:
            text = msg.text

            container = msg.find_element_by_xpath('..')
            attr = container.get_attribute('class')
            pos = attr.find('C(#')
            color = attr[pos + 3:pos + 6]

            dialog.append(text)
            owner.append(color)

        # merge sequence of messages from one sender
        dialog_chain = [dialog[0]]
        owner_chain = [owner[0]]

        for msg, who in zip(dialog[1:], owner[1:]):
            if who == owner_chain[-1]:
                dialog_chain[-1] = 'f{dialog_chain[-1]} {msg}'
            else:
                dialog_chain.append(msg)
                owner_chain.append(who)

        print(dialog_chain)
        print(owner_chain)

        if owner_chain[-1] != ME:
            answer = get_answer(dialog_chain[-1])
            self.send_message(answer)

    def go_through_conversations(self):
        """
        Go through all dialogs and process each of them
        """
        print('Checking conversations ...')
        try:
            self.go_to_messages()
        except NoSuchElementException:
            return
        else:
            conversations = self.driver.find_elements_by_xpath("//a[starts-with(@class, 'messageListItem')]")
            for conversation in conversations:
                conversation.click()
                sleep(5)
                self.process_conversation()

    def swipe(self):
        """
        Encapsulates logic for one swipe
        """

        self.close_popup()
        picture_url = self.extract_picture()

        self.close_popup()
        self.action(make_decision(picture_url, self.model))

    def start_swiping(self, model_path):
        """
        Entry point for a controller to start swiping
        """

        self.model = Model(model_path)

        print('Waiting...')

        is_pic_available = False
        PIC_SELECTOR = "div[class$='StretchedBox'][style^='background-image']"
        while not is_pic_available:
            try:
                pics = self.driver.find_elements_by_css_selector(PIC_SELECTOR)
            except NoSuchElementException:
                pass
            else:
                if len(pics) > 1:
                    is_pic_available = True

        i = 1
        while True:
            sleep(0.5)

            if i % 10 == 0:
                self.go_through_matches_and_message()
                sleep(1)
                self.go_through_conversations()

            print('Making swipes ...')
            self.go_to_swipes()

            try:
                self.swipe()
            except OutOfSwipes:
                print('Seems we have reached a daily limit of swipes :(')
                break

            i += 1

    def start_dataset_collecting(self, dataset_folder):
        """
        Entry point for a controller to start data collection process
        """

        def collect(action, folder):
            if folder is not None:
                try:
                    url, path_to_save = self.extract_picture_link(folder)
                except NoSuchElementException:
                    print('WTF are you swiping, I cannot even see a picture')
                    return
                threading.Thread(target=self.save_picture, args=(url, path_to_save)).start()

            try:
                action()
            except (NoSuchElementException, ElementClickInterceptedException):
                print('WTF are you doing, I cannot see buttons')
                return

        def prompt():
            """
            Helper function to process input from the user
            """
            prompt_string = f'Like({int(Decision.LIKE)}), Dislike({int(Decision.DISLIKE)}) or ' \
                            f'Close popup({int(Decision.CLOSE_POPUP)}): '

            try:
                input_ = int(input(prompt_string))
            except ValueError:
                input_ = None
            
            while not (input_ == Decision.LIKE or input_ == Decision.DISLIKE or input_ == Decision.CLOSE_POPUP):
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
                args = (self.like, liked_folder)
            elif input_ == Decision.DISLIKE:
                args = (self.dislike, disliked_folder)
            elif input_ == Decision.CLOSE_POPUP:
                args = (self.close_popup, None)

            collect(*args)
