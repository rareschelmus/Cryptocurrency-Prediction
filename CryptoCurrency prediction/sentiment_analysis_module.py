from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy
import pandas
import math
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *


class SentimentAnalyzer_module:

    startDate=""
    endDate=""
    data_set=pandas.DataFrame()
    score_data=pandas.DataFrame()

    def SentymentAnalyzer(self):
        return 1

    def setData(self,data_set):
        self.data_set=data_set

    def setDate(self,startDate,endDate):
        self.startDate=startDate
        self.endDate=endDate

    def scoreSentimentAnalysis(self, data_news):
        data_set=pandas.DataFrame(data_news)
        scores=pandas.DataFrame(data_set[["date"]])
        scores["score"]=""
        sentiment_module=SentimentIntensityAnalyzer()
        pos = 0
        for i, item in data_set.iterrows():
            try:
                sentiment_scores = sentiment_module.polarity_scores(item["title"])
                score = sentiment_scores["pos"] - sentiment_scores["neg"]
                scores.set_value(pos, 'score', score)
            except TypeError:
                pass
            pos += 1

        #salvam sub forma de data frame rezultatul obtinut anterior
        scores_data_frame = pandas.DataFrame(scores)

        #genereaza date calendaristice continue
        continuous_dates = pandas.date_range(self.startDate, self.endDate)
        continuous_data = pandas.DataFrame(data=continuous_dates.get_values(), columns=['date'])
        continuous_data["score"] = ''

        continuous_data=self.scoreFilter_MultipleArticles(continuous_data,scores_data_frame)

        self.data_set=continuous_data

    def scoreFilter_MultipleArticles(self,continuous_data, scores_data_frame):
        pos = 0
        for i, items in continuous_data.iterrows():
            # gaseste toate cu data X
            date_df = scores_data_frame.loc[scores_data_frame["date"] == str(items["date"])[:10]]

            if len(date_df) is 1:
                for j, row in date_df.iterrows():
                    continuous_data.set_value(pos, 'score', row['score'])
            elif len(date_df) > 1:
                number_of_elements = 0
                sum = 0
                for j, row in date_df.iterrows():
                    if row['score'] != 0.0:
                        sum += row['score']
                        number_of_elements += 1
                if number_of_elements == 0:
                    number_of_elements = 1
                continuous_data.set_value(pos, 'score', sum / number_of_elements)
            else:
                continuous_data.set_value(pos, 'score', 9)
            pos += 1

        if continuous_data.get_value(0, 'score') is 9:
            continuous_data.set_value(0, 'score', 0)
        if continuous_data.get_value(len(continuous_data) - 1, 'score') is 9:
            continuous_data.set_value(len(continuous_data) - 1, 'score', 0)

        return continuous_data

    def scoreFilter_BlankPadding(self,method):
        if method=="rares":
            pos = 0
            x = self.data_set.get_value(0, 'score')
            for i, items in self.data_set.iterrows():
                if items['score'] == 9:
                    pos_y = pos + 1
                    ok = 0
                    y = 0
                    while ok is 0:
                        if self.data_set.get_value(pos_y, 'score') != 9:
                            ok = 1
                            y = self.data_set.get_value(pos_y, 'score')
                        else:
                            pos_y += 1
                    for j in range(pos, pos_y):
                        new_score = (self.data_set.get_value(j - 1, 'score') + y) / (math.floor(math.sqrt(pos + pos_y + 1)) + 1)
                        self.data_set.set_value(j, 'score', new_score)
                pos += 1
            return self.data_set
        elif method=="goel":
            pos = 0
            x = self.data_set.get_value(0, 'score')
            for i, items in self.data_set.iterrows():
                if items['score'] == 9:
                    pos_y = pos + 1
                    ok = 0
                    y = 0
                    while ok is 0:
                        if self.data_set.get_value(pos_y, 'score') != 9:
                            ok = 1
                            y = self.data_set.get_value(pos_y, 'score')
                        else:
                            pos_y += 1
                    for j in range(pos, pos_y):
                        new_score = (self.data_set.get_value(j - 1, 'score') + y) / 2
                        self.data_set.set_value(j, 'score', new_score)
                pos += 1
        elif method == "0":
            pos = 0
            for i, items in self.data_set.iterrows():
                if items["score"]==9:
                    self.data_set.set_value(pos,'score',0)
                pos+=1
        else:
            pass
        return self.data_set