# pmldl_project

### Team
 - Danis Begishev (BS17-DS02)
 - Aydar Gabdrahmanov (BS17-DS02)
 - Maxim Popov (BS17-DS01)
 
### Project
 - Tinder Bot
 
### Objective
To create the bot which will automate the actions of users on the dating platform called Tinder. Gender to simulate the behaviour of is male.
What to automate:
  - [ ] Decisions on whether the girl is good looking or not
    - [ ] Collect the dataset of girls' pictures and label data on 'like-dislike' targets (Started)
    - [ ] Train CNN to classify photos
  - [x] Left-right swipe based on the previous decision
  - [ ] Handling of the matches: in case of match bot needs to start a conversation with a high probability of answer from the girl and try to support the dialogue for a long time
  - [ ] [BONUS] make notifications on matches and dialogues to the user in Telegram
  
### Usage of the bot
The main audience of the bot are males who use Tinder and don’t want to spend time on swiping and starting the conversation. The slogan of the bot is
“It's good when the soil has already been tested”.

### Current solutions
On the Internet, there can be found some personal solutions on the problem which can automate swipes or dialogues, we want to fully automate the logic of acquaintance with girls and make it personalized for us.

### Main components
As it was mentioned above, our bot’s ‘brain’ is going to consist of two parts: one is responsible for visual perception of girls’ looking and another one is responsible for conversations. Both these parts are going to be trained in a supervised manner and most probably are not going to be updated during usage in case we will not have enough time to build a system for learning based on feedback, so basically we are going to have an offline framed learning system.

### Performance measurement
As a metric of quality of bot’s actions we can look at the mean length of dialogues.

### Human expertise
In the context of dialogues human expertise is always applicable, so we can always estimate the quality of conversations just by simply looking at it.

### How to run
1. Create virtualenv, activate it and install given requirements

- python3 -m venv venv
- . venv/bin/activate
- pip install -r requirements.txt

2. Download [ChromeWebDriver](https://chromedriver.chromium.org/downloads) and locate **chromedriver** in /usr/local/bin

