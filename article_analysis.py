from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import cleantext

response = requests.get(
    "https://www.aljazeera.com/news/2022/11/8/nicole-strengthens-into-tropical-storm-en-route-to-bahamas"
)
article_page = response.text

article_soup = BeautifulSoup(article_page, "html.parser")
headlines_dict = {
    "aj": {
        "tags": [{"class": "tr-story-p1"}, {"class": None}],
    },
    "ib": {
        "tags": [{"class": "paragraph"}, {"class": None}],
    },
    "tg": {
        "tags": [{"class": "dcr-2v2zi4"}, {"class": "dcr-hw2voq"}],
    },
}


title = article_soup.find("title").text.split((" |"))[0].split((" - Info"))[0]


paragraphs = []

for tag in headlines_dict["aj"]["tags"]:
    paragraphs += article_soup.find_all("p", tag)

article_text = title

for paragraph in paragraphs:
    article_text += "\n" + paragraph.text

blob = TextBlob(article_text)
polarity = round(blob.sentiment.polarity, 2)
subjectivity = round(blob.sentiment.subjectivity, 2)

print(article_text)
print(f"Polarity: {polarity}")
print(f"Subjectivity: {subjectivity}")

# clean_article = cleantext.clean(article_text, clean_all=True)
new_stop = STOPWORDS
new_stop.add("s")
# print(clean_article)


mask = np.array(Image.open("cloud.png"))
wc = WordCloud(
    background_color="blue",
    mask=mask,
    height=400,
    stopwords=new_stop,
    width=600,
    max_words=100,
)

wc.generate(article_text)

wc.to_file("article_wordcloud.png")
