""" Test scraping """

from bs4 import BeautifulSoup

with open("pages/carrot.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Adjust selector as needed
for title in soup.select("h3.card__title"):
    print(title.text.strip())
