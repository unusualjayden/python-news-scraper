import requests
from bs4 import BeautifulSoup as bs
import re


# TODO singleton
class Scraper:
    def __init__(self, baseurl, filename, rubric=None, date=None):
        self.baseurl = baseurl
        self.filename = filename
        self.rubric = rubric
        self.date = date
        self._session = requests.Session()
        self._rq = requests.get(self.baseurl)
        self._soup = bs(self._rq.content, "lxml")

    def getPostList(self, posttype):
        c = "news" if posttype == "news" else "article"
        newsSpans = self._soup.findAll("div", attrs={"class": c})
        newsList = []
        for span in newsSpans:
            href = span.find("a")["href"]
            if self.date is None:
                if re.match("/" + posttype + "/\d{4}/\d{2}/\d{2}/.+/", href):
                    newsList.append(self.baseurl + href)
            else:
                if re.match("/" + posttype + "/" + self.date.replace(".", "/") + "/.+/", href):
                    newsList.append(self.baseurl + href)
        return newsList

    def getUrlList(self):
        if self.rubric is None:
            return self.getPostList("news") + self.getPostList("articles") + self.getPostList("brief")
        else:
            return self.getPostList(self.rubric)


class Post:
    def __init__(self, url):
        self.url = url
        self._rq = requests.get(self.url)
        self._soup = bs(self._rq.content, "lxml")
        self.headline = None
        self.subheads = None
        self.cont = None

    @property
    def getHeadline(self):
        return self._soup.find("h1", attrs={"itemprop": "headline"}).text

    @property
    def content(self):
        return self._soup.find("div", attrs={"itemprop": "articleBody"}).text


def main():
    scraper = Scraper("https://lenta.ru/", filename="example.txt", rubric="articles")
    print(Post(scraper.getUrlList()[0]).content)
    # with open("./example.txt", "w") as outfile:
    #     for n in scraper.getUrlList():
    #         outfile.write(Post(n).content.text)


if __name__ == "__main__":
    main()
