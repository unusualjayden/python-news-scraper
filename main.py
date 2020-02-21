import requests
from bs4 import BeautifulSoup as bs
import re


class Scraper:
    def __init__(self, baseurl, filename, rubric=None, date=None):
        self.baseurl   = baseurl
        self.filename  = filename
        self.rubric    = rubric
        self.date      = date
        self._session   = requests.Session()
        self._rq        = requests.get(self.baseurl)
        self._soup      = bs(self._rq.content, "lxml")

    def getNewsList(self):
        newsSpans = self._soup.findAll("div", attrs={"class": "news"})
        newsList = []
        for span in newsSpans:
            href = span.find("a")["href"]
            if self.date is None:
                if re.match("/news/\d{4}/\d{2}/\d{2}/.+/", href):
                    newsList.append(self.baseurl + href)
            else:
                if re.match("/news/" + self.date.replace(".", "/") + "/.+/", href):
                    newsList.append(self.baseurl + href)
        return newsList

    def getArticlesList(self):
        articlesSpans = self._soup.findAll("div", attrs={"class": "article"})
        articlesList = []
        for span in articlesSpans:
            href = span.find("a")["href"]
            if self.date is None:
                if re.match("/articles/\d{4}/\d{2}/\d{2}", href):
                    articlesList.append(self.baseurl + href)
            else:
                if re.match("/articles/" + self.date.replace(".", "/") + "/.+/", href):
                    articlesList.append(self.baseurl + href)
        return articlesList

    def getBriefList(self):
        briefSpans = self._soup.findAll("div", attrs={"class": "article"})
        briefList = []
        for span in briefSpans:
            href = span.find("a")["href"]
            if self.date is None:
                if re.match("/brief/\d{4}/\d{2}/\d{2}", href):
                    briefList.append(self.baseurl + href)
            else:
                if re.match("/brief/" + self.date.replace(".", "/") + "/.+/", href):
                    briefList.append(self.baseurl + href)
        return briefList

    def getUrlList(self):
        if self.rubric is None:
            return self.getNewsList() + self.getArticlesList() + self.getBriefList()
        elif self.rubric == "news":
            return self.getNewsList()
        elif self.rubric == "articles":
            return self.getArticlesList()

# class Post:
# class News(Post):
# class Brief(Post):
# class Article(Post):

# LINK TITLE CONTENT

def main():
    scraper = Scraper("https://lenta.ru/", filename="example.txt")
    print(scraper.getBriefList())
if  __name__ == "__main__":
    main()