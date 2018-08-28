from urllib import request
import urllib
import re
import pandas as pd
import datetime

class PriceCrawler:
    startDate=""
    endDate=""
    coin=""
    regexString = b"<tr class=\"text-right\">\\n ?<td class=\"text-left\">([a-zA-Z]{3} \d\d, \d\d\d\d)<\/td>\\n ?<td data-format-fiat data-format-value=\"([\d]*\.[\d]*)\">([\d]*\.[\d]*)<\/td>\\n ?<td data-format-fiat data-format-value=\"([\d]*\.[\d]*)\">([\d]*\.[\d]*)<\/td>\\n ?<td data-format-fiat data-format-value=\"([\d]*\.[\d]*)\">([\d]*\.[\d]*)<\/td>\\n ?<td data-format-fiat data-format-value=\"([\d]*\.[\d]*)\">([\d]*\.[\d]*)<\/td>\\n ?<td data-format-market-cap data-format-value=\"([\d]*\.[\d]*)\">([\d,]*)<\/td>\\n ?<td data-format-market-cap data-format-value=\"([\d\.\+e]*)\">([\d,]*)<\/td>\\n ?<\/tr>"
    regex = re.compile(regexString)
    pricesDictionary = {"date": [], "close": []}

    def NewsCrawler(self):
        return 1

    def setCoin(self,coin):
        self.coin = coin

    def setEndDate(self,endDate):
        self.endDate = endDate

    def setStartDate(self,startDate):
        self.startDate=startDate

    def getDataPandas(self):
        self.pricesDictionary = {"date": [], "close": []}
        response = urllib.request.urlopen(
            "https://coinmarketcap.com/currencies/"+
            self.coin+
            "/historical-data/?start="+
            self.startDate.replace("-","")+
            "&end="+
            self.endDate.replace("-","")).read()

        results = self.regex.findall(response)
        results = reversed(results)
        for row in results:
            self.pricesDictionary["date"].append(str(row[0])[2:-1])
            self.pricesDictionary["close"].append(float(row[8]))


        self.pricesDictionary["date"]=self.generateDates(self.startDate,self.endDate)
        return pd.DataFrame(self.pricesDictionary)

    def generateDates(self,startDate,endDate):
        start=datetime.datetime.strptime(startDate,"%Y-%m-%d")
        end=datetime.datetime.strptime(endDate,"%Y-%m-%d")
        step=datetime.timedelta(days=1)
        dates=[]
        while start<=end:
            dates.append(str(start.date()))
            start+=step
        return dates