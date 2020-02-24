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

    def writeFile(self):
        i = 0
        with open(self.filename, "w") as outfile:
            for n in self.getUrlList():
                print(f"{i} -- {n}")
                i += 1
                outfile.write(f"{n}\n")
                outfile.write((Post(n).headline()))
                outfile.write((Post(n).content()))

class Post():
    def __init__(self, url):
        self.url      = url
        self._rq      = requests.get(self.url)
        self._soup    = bs(self._rq.content, "lxml")

    def headline(self):
        return self._soup.find(class_=re.compile(r"__title")).text +"\n"

    def content(self):
        c = ""
        body = self._soup.find(class_=re.compile(r"(?:js-topic__text|b-numeric-card-box)"))
        p = body("p")
        if p is not None:
            for el in p:
                c += el.text + "\n"
        return c
