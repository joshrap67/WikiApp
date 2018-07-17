# WikiHopper Kivy Application

Kivy application which displays the most common noun of a random Wikipedia article.
## Getting Started

Not much is needed for this application to run. Below are notes on how to deploy this application.
### Prerequisites

Python is required for this application to run (version 3.70 or greater).

Pip, a package management system, is recommended to be installed as it allows for packages to be installed easily. Version 10.0.1 was used for the creation of this project.

Included in the repository is a filename 'requirements.txt'. Using pip one can easily install the required python packages by simply running the following command in the directory of the project:
`pip install -r requirements.txt`

If pip is not used, the required packages to install are:
- kivy (version 1.10.0)
- textblob (version 0.15.1)
- bs4 (version 4.6.0)

A connection to the internet is also required for this project to function as requests need to be sent online to retrieve data from Wikipedia articles.
## Deployment

To run this application, execute the following command in the directory with the files in this repository:
`python main.py`

This application is very simple with only two actions required by the user.
- To fetch a new random article, press the top button labeled 'Fetch Random Article'
- To launch a specific Wikipedia article in a browser, click the text of the article to be visited
## Built With

- [Python](https://www.python.org/) - Used for the backend of the application
- [Kivy](https://kivy.org/#home) - Framework used for the frontend of the application
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - Python library that aides in parsing of websites and helps cleans up HTML format from websites that might not be formatted correctly.
- [TextBlob](https://textblob.readthedocs.io/en/dev/) - Text processing library that allows for nouns in a string to be identified.
## Authors

- Joshua Rapoport - *Creator and Main Software Developer*
