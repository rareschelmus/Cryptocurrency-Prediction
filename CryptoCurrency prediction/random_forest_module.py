import numpy
import pandas
from treeinterpreter import treeinterpreter
from sklearn.ensemble import RandomForestRegressor
import datetime

import matplotlib.pyplot as plt

class RandomForestModule:

    startDate = ""
    endDate=""

    data_test_price = pandas.DataFrame()
    data_training_price = pandas.DataFrame()

    data_test_sentiment=pandas.DataFrame()
    data_training_sentiment=pandas.DataFrame()

    random_forest_mod = RandomForestRegressor()
    coin = ""

    def RandomForestModule(self):
        return 1

    def setData(self,price_data_set,sentiment_score):
        self.data_training_price=price_data_set[:-10]
        self.data_test_price=price_data_set[-10:]

        self.data_training_sentiment=sentiment_score[:-10]
        self.data_test_sentiment=sentiment_score[-10:]

    def setDataPrice(self,price_data_set):
        self.data_training_price=price_data_set[:-10]
        self.data_test_price=price_data_set[-10:]

    def setDataForPrediction(self,price_data_set,sentiment_score):
        self.data_training_price=price_data_set
        self.data_test_price=price_data_set

        self.data_training_sentiment=sentiment_score
        self.data_test_sentiment=sentiment_score

    def setCoin(self,coin):
        self.coin=coin

    def setStartDate(self, date):
        self.startDate=date

    def setEndDate(self,date):
        self.endDate=date

    def testSentiment(self,mode):
        train_data_x = numpy.asarray([[x] for x in self.data_training_sentiment["score"]])
        train_data_y = numpy.asarray(self.data_training_price["close"])
        test_data_x = numpy.asarray([[x] for x in self.data_test_sentiment["score"]])
        test_data_y = numpy.asarray(self.data_test_price["close"])

        random_forest = RandomForestRegressor()
        random_forest.fit(train_data_x, train_data_y)

        prediction, bias, contributions = treeinterpreter.predict(random_forest, test_data_x)

        date_prediction = pandas.date_range(self.data_test_price["date"][self.data_test_price.index[-10]], self.data_test_price["date"][self.data_test_price.index[-1]])
        prediction_data = pandas.DataFrame(data=prediction[0:], index=date_prediction, columns=["predicted_prices"])

        fix_constant = self.data_training_price["close"][self.data_training_price.index[-1]] - prediction[0]
        for i, item in prediction_data.iterrows():
            item["predicted_prices"] = item['predicted_prices'] + fix_constant

        predictions_plot = prediction_data.plot()
        y_test = pandas.DataFrame(data=test_data_y[0:], index=date_prediction, columns=["prices"])
        fig = y_test.plot(ax=predictions_plot).get_figure()
        fig.savefig("test_sent_"+mode+".png")


    def testNormal(self):
        x_train = numpy.asarray([[int(x[-2:])] for x in self.data_training_price['date']])
        y_train = numpy.asarray(self.data_training_price['close'])

        random_forest = RandomForestRegressor()
        random_forest.fit(x_train, y_train)

        prediction = []
        new_dates= self.generateDates(self.data_training_price["date"][self.data_training_price.index[-1]],10)
        date_prediction = [int(x[-2:]) for x in new_dates]

        for i in date_prediction:
            prediction.append(random_forest.predict(i))

        prediction_data = pandas.DataFrame(data=prediction[0:], index=date_prediction, columns=["predicted_price"])
        actual_price = pandas.DataFrame(data= [x for x in self.data_test_price['close']], index=date_prediction, columns=["actual_price"])

        prediction_plot = prediction_data.plot()

        fig = actual_price.plot(ax=prediction_plot).get_figure()
        fig.savefig("test_rf.png")

    def predictSentiment(self,mode):
        # antrenam arborii pentru a obtine scorurile noi
        train_data_x = numpy.asarray([[int(x[-2:])] for x in self.data_training_price["date"]])
        train_data_y = numpy.asarray([x for x in self.data_training_sentiment["score"]])
        random_forest = RandomForestRegressor()
        random_forest.fit(train_data_x, train_data_y)

        predicted_sentiment_score=[]
        date_prediction =[int(str(x)[-11:-9]) for x in pandas.date_range(self.generateDates(self.data_training_price["date"][self.data_training_price.index[-1]],1)[0],
                                            periods=10)]
        for i in date_prediction:
            predicted_sentiment_score.append(random_forest.predict(i)[0])

        train_data_x = numpy.asarray([[x] for x in self.data_training_sentiment["score"]])
        train_data_y = numpy.asarray([x for x in self.data_training_price["close"]])

        random_forest_2=RandomForestRegressor()
        random_forest_2.fit(train_data_x,train_data_y)

        predicted_price=[]
        for i in predicted_sentiment_score:
            predicted_price.append(random_forest_2.predict(i)[0])

        predicted_price_frame=pandas.DataFrame(data=predicted_price,index=date_prediction,columns=["predicted price"])
        predicted_price_frame.plot().get_figure().savefig("predicted_sent_"+mode+".png")


    def predictNormal(self):
        x_train = numpy.asarray([[int(x[-2:])] for x in self.data_training_price['date']])
        y_train = numpy.asarray(self.data_training_price['close'])

        random_forest = RandomForestRegressor()
        random_forest.fit(x_train, y_train)

        prediction = []
        new_dates = self.generateDates(self.data_training_price["date"][self.data_training_price.index[-1]], 10)
        date_prediction = [int(x[-2:]) for x in new_dates]

        for i in date_prediction:
            prediction.append(random_forest.predict(i))

        prediction_data = pandas.DataFrame(data=prediction[0:], index=date_prediction, columns=["predicted_price"])

        fig = prediction_data.plot().get_figure()

        fig.savefig("predicted_rf.png")
        return 1

    def generateDates(self, startDate,period):
        start = datetime.datetime.strptime(startDate, "%Y-%m-%d")
        step = datetime.timedelta(days=1)
        dates = []

        for i in range(0,period):
            start += step
            dates.append(str(start.date()))
        return dates



