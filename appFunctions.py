# go to a random Wikipedia page and output the longest word and most typed word
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from textblob import TextBlob
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty

Builder.load_file('mainPage.kv')


class MainPage(Widget):
    @staticmethod
    def random_article():
        url = 'https://en.wikipedia.org/wiki/Special:Random'
        html = urllib.request.urlopen(url).read()
        # to fix any HTML errors, use beautiful soup
        soup = BeautifulSoup(html, 'html.parser')
        title_soup = soup('title')  # find the article title
        title = title_soup[0].text
        paragraph_tags = soup('p')  # find the words in the HTML paragraph tags
        words = dict()  # keeps track of all the words found and the counts associated with each word
        for tag in paragraph_tags:
            working_line = tag.text
            blob = TextBlob(working_line)
            nouns = blob.noun_phrases
            for noun in nouns:
                words[noun] = words.get(noun, 0) + 1
        biggest_word = None
        big_count = 0
        # find the biggest word
        for k, v in words.items():
            if k is None or v > big_count:
                biggest_word = k
                big_count = v
        attributes = Data(title, biggest_word, big_count)
        return attributes

    def display_info(self):
        new_article = self.random_article()
        self.ids.app_attributes.text = repr(new_article) # display text to the app
        print('Display Info Text #############################')
        print(repr(new_article))
        self.store_history(new_article)  # store the article into history
        self.update_history()

    @staticmethod
    def store_history(attribute_obj):
        global working_history
        working_history.set_history(attribute_obj)

    def update_history(self):
        print('Update history text ##########################')
        formatted_data = ''
        for obj in working_history.history:
            formatted_data += repr(obj)+'\n'
        print(formatted_data)  # for debugging purposes
        self.ids.history_label.text = formatted_data

    def turn_on(self):
        self.display_info()

    @staticmethod
    def turn_off():
        quit()


class ArticleContent(Widget):
    pass


class WikiHopper(App):
    def build(self):
        return MainPage()


class History:
    # history will be a list of data objects
    def __init__(self):
        self.history = list()

    def set_history(self, data):
        if len(self.history) < 10:
            self.history.insert(0, data)
        elif len(self.history) == 10:
            # ensures that only 10 items are kept on the list at a time
            self.history.pop()
            self.history.insert(0, data)
        else:
            print('Error')

    def get_history(self):
        return self.history


working_history = History()  # list of the attributes of previous articles. initialized every time program starts


class Data:
    def __init__(self, an_article, a_word, a_count):
        fixed_name = an_article.replace('- Wikipedia', '')
        self.article_name = fixed_name
        self.largest_word = a_word
        self.word_count = a_count

    def get_article_name(self):
        return self.article_name

    def get_largest_word(self):
        return self.largest_word

    def get_word_count(self):
        return self.word_count

    def __repr__(self):
        return 'Article Name: '+str(self.article_name)+' Largest Word: '+str(self.get_largest_word()) + ' Count: '\
               + str(self.word_count)
