from urllib.request import Request, urlopen
from urllib import request
import urllib
import re
import time
import pandas as pd
import random


class NewsCrawler:
    coin=""
    endDate=""
    startDate=""

    regexString = b"<a href=\"([^\n\r\"]*)\">([^\n\r\"]*)<\/a><\/h2>\\n<div class=\"entry-meta\">\\n<span class=\"featured-category\"><a href=\"([^\n\r\"]*)\" title=\"([^\n\r\"]*)\">([^\n\r\"]*)<\/a><\/span>\\n<time class=\"updated\" datetime=\"(\d\d\d\d-\d\d-\d\d)T\d\d:\d\d:\d\d\+\d\d:\d\d\">"
    regex = re.compile(regexString)

    newsDictionary = {"date": [], "title": []}

    def NewsCrawler(self):
        return 1

    def setCoin(self,coin):
        self.coin=coin

    def setEndDate(self,endDate):
        self.endDate=endDate

    def setStartDate(self,startDate):
        self.startDate=startDate

    def getDataPandas(self):
        ok = 1
        page = 1
        while (ok):
            link = 'https://www.ccn.com/page/' + str(page) + '?s=' + self.coin
            page += 1
            req = Request(
                link,
                headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            results = self.regex.findall(webpage)
            for row in results:
                if time.strptime(str(row[5])[2:-1], "%Y-%m-%d") < time.strptime(self.endDate, "%Y-%m-%d"):
                    if time.strptime(str(row[5])[2:-1], "%Y-%m-%d") > time.strptime(self.startDate, "%Y-%m-%d"):
                        self.newsDictionary["title"].append(
                            str(row[1])[2:-1].replace("\\xe2\\x80\\x98", "\'").replace("\\xe2\\x80\\x99", "\'").replace(
                                "&#8220;", "\"").replace("&#8221;", "\"").replace("&#8217;","\'").replace("&#038;","&"))
                        self.newsDictionary["date"].append(str(row[5])[2:-1])
                    else:
                        ok = 0
                        break
            # folosim o euristica pentru a nu fi pusi pe lista neagra a site-urilor
            time.sleep(random.uniform(0.5,1.0))
        self.newsDictionary["date"].reverse()
        self.newsDictionary["title"].reverse()

        return pd.DataFrame(self.newsDictionary)
