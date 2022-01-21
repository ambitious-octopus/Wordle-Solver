import sys
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


with open("words.txt", "r") as file:
    words = file.readlines()[0].split(" ")


class Website:
    def __init__(self):
        self.browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.browser.get('https://www.powerlanguage.co.uk/wordle/')
        time.sleep(1)
        self.background = self.browser.find_element(By.TAG_NAME, 'html')
        self.background.click()
        time.sleep(1)
        self.counter = 0

    def send_word_get_answer(self, word):
        self.background.send_keys(word)
        self.background.send_keys(Keys.ENTER)
        time.sleep(1)
        host = self.browser.find_element(By.TAG_NAME, "game-app")
        game = self.browser.execute_script("return arguments[0].shadowRoot.getElementById('game')",
                                       host)
        board = game.find_element(By.ID, "board")
        rows = self.browser.execute_script("return arguments[0].getElementsByTagName('game-row')",
                                       board)
        row = self.browser.execute_script("return arguments[0].shadowRoot.querySelector("
                                      "'.row').innerHTML",
                                     rows[self.counter])
        self.counter += 1

        bs_text = BeautifulSoup(row, 'html.parser')
        results = {}
        for word in bs_text.findAll('game-tile'):
            letter = word.get('letter')
            eval = word.get('evaluation')
            results[letter] = eval

        return (self.counter -1 , results)



def filter_by_presence(present_list, absent_list, words):
    candidates = list()
    for w in words:
        if all(letter in w for letter in present_list):
            candidates.append(w)
        else:
            pass

    for w in candidates:
        if any(letter in w for letter in absent_list):
            candidates.remove(w)
        else:
            pass

    return candidates



def simple_strategy():
    web = Website()

    # This is a strong combination found somewhere!
    guess = ['quick', 'brown', 'shady', 'cleft', 'gimps']

    vocab = words
    present_list = list()
    absence_list = list()
    for i in range(6):
        if i == 5:
            print(vocab[0])
            web.send_word_get_answer(vocab[0])
            sys.exit()
        elif len(vocab) == 1:
            web.send_word_get_answer(vocab[0])
            sys.exit()
        else:
            round_ = web.send_word_get_answer(guess[i])
            for key, value in round_[1].items():
                if value == "correct" or value == "present":
                    present_list.append(key)
                else:
                    absence_list.append(key)

            vocab = filter_by_presence(present_list, absence_list, vocab)

            print("Current vocabulary: ")
            print(vocab)

        time.sleep(2)
    time.sleep(1000)


simple_strategy()



