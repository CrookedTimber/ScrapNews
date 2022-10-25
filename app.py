from flask import Flask, render_template
from datetime import date
from section_scrapper import Section
from section_dictionaries import (
    culture_dict,
    headlines_dict,
    mx_la_dict,
    photos_dict,
    sci_dict,
    sports_dict,
    tech_dict,
    uk_dict,
    world_dict,
)

app = Flask(__name__, template_folder='templates')


headlines = Section(headlines_dict)
uk = Section(uk_dict)
mx_la = Section(mx_la_dict)
culture = Section(culture_dict)
science = Section(sci_dict)
sports = Section(sports_dict)
tech = Section(tech_dict)
world = Section(world_dict)
photos = Section(photos_dict)


@app.route("/")
def home():
    return render_template("index.html", title=" HEADLINES", year=date.today().year, content=headlines.contents)

@app.route("/uk")
def uk_news():
    return render_template("index.html", title=" UNITED KINGDOM", year=date.today().year, content=uk.contents)

@app.route("/latin-america")
def lat_am():
    return render_template("index.html", title="LATIN AMERICA", year=date.today().year, content=mx_la.contents)

@app.route("/world")
def world_news():
    return render_template("index.html", title=" WORLD", year=date.today().year, content=world.contents)

@app.route("/science")
def science_news():
    return render_template("index.html", title=" SCIENCE", year=date.today().year, content=science.contents)

@app.route("/tech")
def tech_news():
    return render_template("index.html", title=" TECHNOLOGY", year=date.today().year, content=tech.contents)

@app.route("/sports")
def sports_news():
    return render_template("index.html", title=" SPORTS", year=date.today().year, content=sports.contents)

@app.route("/culture")
def culture_news():
    return render_template("index.html", title=" CULTURE", year=date.today().year, content=culture.contents)

@app.route("/photos")
def photo_galleries():
    return render_template("index.html", title=" PHOTOS", year=date.today().year, content=photos.contents)

if __name__ == "__main__":
    app.run()
