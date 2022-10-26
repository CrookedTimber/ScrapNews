# ScrapNews
 

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Development Notes](#development-notes)
- [Contact](#contact)

![Alt text](/screenshots/screenshot_1.png?raw=true "Optional Title")

## Description

ScrapNews is a news aggregator that collects the most recent article titles, images, and links from three different sources at once: The Guardian, infobae, and Al-Jazeera. The navigation bar allows users to choose among different news categories. The content is updated at the beginning of every hour of the day.

ScrapNews was born from a desire to automate daily tasks. Reading the news can take a lot of my time as I often find myself navigating through different sources. I do this to find out if there is more information on a topic I'm interested but also because of the differing regional focus of each of the sources gathered by the web app.

### Features:
    1. Responsive design for HD screens, tablets, and smartphones.
    2. Automatic updates on the news every hour of the day.
    3. Three news sources: The Guardian, infobae, and Al-Jazeera
    4. 9 different sections: Headlines, UK, Latin America, World, Culture, Science, Technology, Sports, and Photos.

## Live Demo:

[*ScrapNews*](https://scrapnews.herokuapp.com/)

## Development Notes

### Built with:
    - Flask
    - BeautifulSoup
    - APScheduler
    - Jinja
    - jQuery
    - Bootstrap

What helped the most with the data scraping of BeautifulSoup was identifying the commonalities in the layout of the different news sources. After parsing the html of a section of these sources, the next step consist in selecting the section containing the relevant articles. Finally, the scraper iterates over each of these articles and gathers the desired data. 

Understanding the above pattern allowed me to create a "Section" class that takes care of the job for the three different sources on a given section. For each of the sources, all that is needed by this class is a dictionary containing the url of the desired section and a pair of identifiers to select the html element containing the articles. Considering the variability of the layouts, some degree of customisation was inevitable when reaching the last step of the data gathering process. In some cases, the step of collecting the titles, image urls, and article links was different within the same source when moving from one section to the other. These discrepancies are handled by the Section class itself.

As for the automatic updates, while the newest information could be easily gathered by creating an instance of the section class every time the user access any of the routes of ScrapNews, this would be too slow for an optimal user experience. To improve the loading times of the web app, it was best to have the server gather the data every hour of the day using APScheduler.


## Contact

 Name: Edgar René Ruiz López

 Email: [edgarrruizl@gmail.com](edgarrruizl@gmail.com)

