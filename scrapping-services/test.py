import requests
from bs4 import BeautifulSoup

URL = "https://news.sky.com/"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')  # Using html5lib parser

# Find all <h1> elements
h1_tags = soup.find_all('section')

# Print each <h1> element
for h1 in h1_tags:
    print(h1.prettify())

# If you want to see the full content of the first <h1> element, you can print it like this:
if h1_tags:
    print("First <h1> tag:")
    print(h1_tags[0].prettify())
else:
    print("No <h1> elements found.")