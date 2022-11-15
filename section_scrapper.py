from bs4 import BeautifulSoup
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from article_analysis import (
    get_article_text,
    get_sentiment_analysis,
)
from googletrans import Translator
import json

translator = Translator()


def get_articles_section(site_dict):
    response = requests.get(site_dict["url"])
    mainpage = response.text

    soup = BeautifulSoup(mainpage, "html.parser")

    is_url_tg_headlines = site_dict["url"] == "https://www.theguardian.com/uk/"

    articles = (
        soup.find("section", {"id": "headlines"}).find_all(
            site_dict["tags"][0], class_=site_dict["tags"][1]
        )
        if is_url_tg_headlines
        else soup.find_all(site_dict["tags"][0], class_=site_dict["tags"][1])
    )

    return articles


def get_aj_data(site_dict, max_articles):

    articles = get_articles_section(site_dict)

    aj_articles_array = []

    for idx, article in enumerate(articles):
        if idx == max_articles:
            break

        article_url = "https://www.aljazeera.com" + article.find(
            "a", class_="u-clickable-card__link"
        ).get("href")

        article_dict = {
            "title": article.find("a", class_="u-clickable-card__link").text.replace(
                "\xad", ""
            ),
            "url": article_url,
            "img": "https://www.aljazeera.com"
            + article.find("img", class_="gc__image").get("src"),
            "img_alt": article.find("img", class_="gc__image").get("alt"),
            "sentiment": "",
            "word_cloud": "",
        }

        aj_articles_array.append(article_dict)

    aj_section = {
        "source": "Al Jazeera",
        "section_url": site_dict["url"],
        "logo": "https://upload.wikimedia.org/wikipedia/en/f/f2/Aljazeera_eng.svg",
        "logo_alt": "Al Jazeera logo",
        "articles": aj_articles_array,
        "card_class": "aj-card",
    }

    return aj_section


def get_tg_articles_info(site_dict, max_articles):

    articles = get_articles_section(site_dict)

    tg_articles_array = []

    for idx, article in enumerate(articles):
        if idx == max_articles:
            break

        article_url = article.find(
            "a", class_="u-faux-block-link__overlay js-headline-text"
        ).get("href")

        article_dict = {
            "title": article.find(
                "a", class_="u-faux-block-link__overlay js-headline-text"
            )
            .getText()
            .strip(),
            "url": article_url,
            "img": article.find("img", class_="responsive-img").get("src")
            if article.find("img", class_="responsive-img") is not None
            else "https://upload.wikimedia.org/wikipedia/commons/6/6a/The_Guardian_2.svg",
            "img_alt": article.find("img", class_="responsive-img").get("alt")
            if article.find("img", class_="responsive-img") is not None
            else "The Guardian Logo",
            "sentiment": "",
            "word_cloud": "",
        }

        tg_articles_array.append(article_dict)

    tg_section = {
        "source": "The Guardian",
        "section_url": site_dict["url"],
        "logo": "https://upload.wikimedia.org/wikipedia/commons/archive/7/75/20180115060915%21The_Guardian_2018.svg",
        "logo_alt": "The Guardian logo",
        "articles": tg_articles_array,
        "card_class": "tg-card",
    }

    return tg_section


def get_ib_articles_info(site_dict, max_articles):

    articles = get_articles_section(site_dict)

    ib_articles_array = []

    for idx, article in enumerate(articles):
        if idx == max_articles:
            break

        article_url = "https://www.infobae.com/" + article.get("href")

        article_dict = {
            "title": article.find("span").getText().strip()
            if article.find("span") is not None
            else article.find("h2").getText().strip(),
            "url": article_url,
            "img": article.find("img").get("src")
            if article.find("img") is not None
            else "https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1432665899/fmumod2xiulnacz6ecmr.jpg",
            "img_alt": article.find("img", class_="cst_img").get("alt")
            if article.find("img", class_="cst_img") is not None
            else "infobae logo",
            "sentiment": "",
            "word_cloud": "",
        }

        ib_articles_array.append(article_dict)

    ib_section = {
        "source": "infobae",
        "section_url": site_dict["url"],
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Infobae.com_logo.png/1024px-Infobae.com_logo.png",
        "logo_alt": "infobae logo",
        "articles": ib_articles_array,
        "card_class": "ib-card",
    }

    return ib_section


class Section:
    def __init__(self, dict, section_name):
        self.section_name = section_name
        self.dict = dict
        self.max_articles = 8
        self.contents = []
        self.refresh_content()
        self.refresher = BackgroundScheduler(daemon=True)
        self.refresher.add_job(self.refresh_content, trigger="cron", hour="*")
        self.refresher.start()

    def refresh_content(self):
        self.contents = []
        self.contents.append(get_tg_articles_info(self.dict["tg"], self.max_articles))
        self.contents.append(get_ib_articles_info(self.dict["ib"], self.max_articles))
        self.contents.append(get_aj_data(self.dict["aj"], self.max_articles))
        self.analyze_articles()

    def analyze_articles(self):
        for article in self.contents[0]["articles"]:
            article_text = get_article_text(article["url"], "tg")
            article["sentiment"] = get_sentiment_analysis(article_text)
            # article["word_cloud"] = generate_word_cloud(article_text, "tg", self.section_name, idx)

        for article in self.contents[1]["articles"]:
            article_text = get_article_text(article["url"], "ib")

            article["sentiment"] = get_sentiment_analysis(article_text)
            # article["word_cloud"] = generate_word_cloud(article_text, "ib", self.section_name, idx)

        for article in self.contents[2]["articles"]:
            article_text = get_article_text(article["url"], "aj")
            article["sentiment"] = get_sentiment_analysis(article_text)
            # article["word_cloud"] = generate_word_cloud(article_text, "aj", self.section_name, idx)
