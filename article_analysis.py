from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

# from wordcloud import WordCloud, STOPWORDS
# from PIL import Image
# import numpy as np


def get_article_text(article_link, site_id):

    response = requests.get(article_link)
    article_page = response.text

    article_soup = BeautifulSoup(article_page, "html.parser")
    article_tags = {
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

    for tag in article_tags[site_id]["tags"]:
        paragraphs += article_soup.find_all("p", tag)

    article_text = title

    for paragraph in paragraphs:
        article_text += "\n" + paragraph.text

    return article_text


def get_sentiment_analysis(article_text):

    blob = TextBlob(article_text)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)
    return [polarity, subjectivity]

    # def generate_word_cloud(article_text, site_id, section_name, article_idx):

    print("Generating")
    new_stop = STOPWORDS
    new_stop.add("s")

    mask = np.array(Image.open("cloud.png"))
    wc = WordCloud(
        background_color="white",
        mask=mask,
        height=400,
        stopwords=new_stop,
        width=600,
        max_words=100,
    )

    filename = f"images/{site_id}_{section_name}_word_cloud_{article_idx}.png"

    wc.generate(article_text)

    wc.to_file(filename)

    return "/" + filename
