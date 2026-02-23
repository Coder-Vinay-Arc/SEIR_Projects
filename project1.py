import sys
import requests
from bs4 import BeautifulSoup

# take url from command line
url = sys.argv[1]

# get page data
response = requests.get(url)

html = response.text
soup = BeautifulSoup(html, "html.parser")

print("TITLE:")
print(soup.title.text)

print("BODY:")
print(soup.get_text())

print("LINKS:")
links = soup.find_all("a")

for link in links:
    print(link.get("href"))