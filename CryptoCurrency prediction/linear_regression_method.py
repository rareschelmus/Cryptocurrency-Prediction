import pandas
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import datetime


class LinearRegressionMethod:
    startDate=""
    data_test=pandas.DataFrame()
    data_training=pandas.DataFrame()
    linear_mod = linear_model.LinearRegression()
    coin =""

    def LinearRegressionMethod(self):
        return 1

    def setData(self,price_data_set):
        self.data_training=price_data_set[:-10]
        self.data_test=price_data_set[-10:]
        return 1

    def setCoin(self,coin):
        self.coin=coin

    def setDate(self, date):
        self.startDate=date

    def train(self):
        dates = np.reshape(range(1,len(self.data_training["date"])+1), (len(self.data_training["date"]), 1))
        prices = np.reshape(self.data_training["close"], (len(self.data_training["close"]), 1))
        self.linear_mod.fit(dates, prices)

    def testPrediction(self):
        prediction = []
        days=range(len(self.data_training["date"]),len(self.data_training["date"])+len(self.data_test["date"]))

        for day in days:
            predicted_price = self.linear_mod.predict(day)
            prediction.append(predicted_price[0][0])

        delta=prediction[0]-self.data_training["close"][self.data_training.index[-1]]
        prediction=[x-delta for x in prediction]

        prediction_frame=pandas.DataFrame(data=prediction,index=[int(str(x)[-2:]) for x in self.data_test["date"]],columns=["predicted price"])
        actual_price=pandas.DataFrame(data=[y for y in self.data_test["close"]],index=[int(str(x)[-2:]) for x in self.data_test["date"]],columns=["actual price"])

        prediction_plot=prediction_frame.plot()
        fig=actual_price.plot(ax=prediction_plot).get_figure()
        fig.savefig("test_linear_regression.png")

    def newPrediction(self):
        prediction = []
        days = range(len(self.data_training["date"]), len(self.data_training["date"]) + len(self.data_test["date"]))
        for day in days:
            predicted_price = self.linear_mod.predict(day)
            prediction.append(predicted_price[0][0])

        dates=self.generateDates(self.data_training["date"][self.data_training.index[-1]],10)

        prediction_frame = pandas.DataFrame(data=prediction[0:], index=[int(str(x)[-2:]) for x in dates],
                                             columns=["predicted_prices"])

        prediction_plot = prediction_frame.plot()
        plt.gcf().subplots_adjust(bottom=0.15)

        prediction_figure=prediction_plot.get_figure()
        prediction_figure.savefig("predicted_linear_regression.png")

    def generateDates(self, startDate,period):
        start = datetime.datetime.strptime(startDate, "%Y-%m-%d")
        step = datetime.timedelta(days=1)
        dates = []
        for i in range(0,period):
            start += step
            dates.append(str(start.date()))
        return dates
