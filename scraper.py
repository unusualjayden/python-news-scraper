import re
import requests
from bs4 import BeautifulSoup as bs


class Scraper:
    def __init__(self, baseurl, filename, rubric=None, date=None):
        self.baseurl  = baseurl
        self.filename = filename
        self.rubric   = rubric
        self.date     = date
        self._session = requests.Session()
        self._rq      = requests.get(self.baseurl)
        self._soup    = bs(self._rq.content, "lxml")

    # TODO posttype = all

    def getPostTypeUrlList(self, pt):
        c = "news" if pt == "news" else "article"
        spans = self._soup.findAll("div", attrs={"class": c})
        url_list = []
        for span in spans:
            href = span.find("a")["href"]
            if self.date is None:
                if re.match("/" + pt + "/\d{4}/\d{2}/\d{2}/.+/", href):
                    url_list.append(self.baseurl + href)
            else:
                if re.match("/" + pt + "/" + self.date.replace(".", "/") + "/.+/", href):
                    url_list.append(self.baseurl + href)
        return url_list

    def getUrlList(self):
        if self.rubric is None:
            return self.getPostTypeUrlList("news") + \
                   self.getPostTypeUrlList("articles") + \
                   self.getPostTypeUrlList("brief")
        else:
            return self.getPostTypeUrlList(self.rubric)


class Post():
    def __init__(self, url):
        self.url      = url
        self._rq      = requests.get(self.url)
        self._soup    = bs(self._rq.content, "lxml")

    def headline(self):
        return self._soup.find("h1", attrs={"itemprop": "headline"}).text

    def content(self):
        return self._soup.find("div", attrs={"itemprop": "articleBody"}).text
