'''
Written by Joshua Rapoport
'''
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from textblob import TextBlob
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
import webbrowser

'''
Classes
'''


class History:
    # history will be a list of data objects. Holds the 10 most current articles
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


class Data:
    # holds specific attributes of a single article
    def __init__(self, an_article, a_word, a_count, a_url):
        fixed_name = an_article.replace('- Wikipedia', '')
        self.article_name = fixed_name
        self.largest_word = a_word
        self.word_count = a_count
        self.url = a_url

    def get_article_name(self):
        return self.article_name

    def get_largest_word(self):
        return self.largest_word

    def get_word_count(self):
        return self.word_count

    def get_url(self):
        return self.url

    def __repr__(self):
        return 'ARTICLE NAME: '+str(self.article_name)+' LARGEST WORD: '+str(self.get_largest_word()) + ' COUNT: '\
               + str(self.word_count)


'''
Global Variables
'''
actual_url = None  # url of a random wiki article
working_history = History()  # list of the attributes of previous articles. initialized every time program starts

'''
Widgets and Kivy Layouts
'''


class HistoryLabel(ButtonBehavior, Label):
    # label of specific previous articles. Dynamically added to HistoryLayout
    pass


class HistoryLayout(BoxLayout):
    # contains the last 10 articles which were accessed
    def update_history(self):
        # remove old labels
        for child in [c for c in self.children if isinstance(c, HistoryLabel)]:
            self.remove_widget(child)
        # add labels corresponding to previous articles in the current history
        index = 0
        for obj in working_history.history:
            new_label = HistoryLabel(text=repr(obj), size_hint_y=None, id=str(index))
            self.add_widget(new_label)
            index += 1

    def launch_url(self, unique_id):
        # called when label is clicked, launches specific article in a browser
        url = working_history.history[int(unique_id)].get_url()
        webbrowser.open(url, new=0, autoraise=True)


class MainPage(GridLayout):

    @staticmethod
    def random_article():
        url = 'https://en.wikipedia.org/wiki/Special:Random'
        html = urllib.request.urlopen(url).read()
        # to fix any HTML errors, use beautiful soup
        soup = BeautifulSoup(html, 'html.parser')
        title_soup = soup('title')  # find the article title
        title = title_soup[0].text
        # find the url of the random article
        url_soup = soup.find_all('link', rel='canonical')
        global actual_url
        for link in url_soup:
            actual_url = link['href']
        # find the words in the HTML paragraph tags
        paragraph_tags = soup('p')
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
        attributes = Data(title, biggest_word, big_count, actual_url)
        return attributes

    def display_info(self):
        # called when user presses button
        new_article = self.random_article()
        # update text in current article layout
        self.ids['current_article_container'].ids['current_article_label'].text = repr(new_article)
        self.store_history(new_article)  # store the article into history
        self.ids['history_contianer'].update_history()

    def launch_url(self):
        url = working_history.history[0].get_url()
        webbrowser.open(url, new=0, autoraise=True)

    @staticmethod
    def store_history(attribute_obj):
        global working_history
        working_history.set_history(attribute_obj)


'''
Building the Kivy app
'''


class WikiHopperApp(App):
    def build(self):
        return MainPage()


if __name__ == '__main__':
    WikiHopperApp().run()
