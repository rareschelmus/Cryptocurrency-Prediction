from crawler_news import NewsCrawler
from crawler_price import PriceCrawler
from sentiment_analysis_module import SentimentAnalyzer_module
from linear_regression_method import LinearRegressionMethod
from random_forest_module import RandomForestModule
from appJar import gui
from datetime import datetime,timedelta

coin=""
startDate=""
endDate=""
testOn=False
random_forest_mod = RandomForestModule()
sentiment_module = SentimentAnalyzer_module()
data_price=None
data_news=None
status=0

def getNews():
    c_news = NewsCrawler()
    c_news.setCoin(coin)
    c_news.setStartDate(startDate)
    c_news.setEndDate(endDate)
    return c_news.getDataPandas()

def getPrices():
    c_price = PriceCrawler()
    c_price.setCoin(coin)
    c_price.setStartDate(startDate)
    c_price.setEndDate(endDate)
    return c_price.getDataPandas()

def runPredictions(btn):
    global coin,startDate,endDate,testOn,random_forest_mod,status,sentiment_module,data_price,data_news
    testOn=False
    coin=app.getEntry("Coin: ")
    startDate=str(app.getDatePicker("start_date_dp"))
    endDate=str((datetime.now()-timedelta(days=2)).date())
    resetMeter()

    sentiment_module.setDate(startDate, endDate)
    data_price= getPrices()
    status=1
    updateMeter()
    data_news = getNews()

    sentiment_module.scoreSentimentAnalysis(data_news)
    status = 2
    updateMeter()
    random_forest_mod.setCoin(coin)
    random_forest_mod.setDataForPrediction(data_price, sentiment_module.scoreFilter_BlankPadding("rares"))
    random_forest_mod.predictSentiment("rares")

    random_forest_mod.setDataForPrediction(data_price, sentiment_module.scoreFilter_BlankPadding("goel"))
    random_forest_mod.predictSentiment("goel")
    status = 3
    updateMeter()
    random_forest_mod.setDataForPrediction(data_price, sentiment_module.scoreFilter_BlankPadding("0"))
    random_forest_mod.predictSentiment("0")

    random_forest_mod.predictNormal()
    status = 4
    updateMeter()
    linear_mod=LinearRegressionMethod()
    linear_mod.setCoin(coin)
    linear_mod.setData(data_price)
    linear_mod.train()
    linear_mod.newPrediction()
    status = 5
    updateMeter()

def runTests(btn):
    global status, coin, startDate, endDate,testOn, random_forest_mod, sentiment_module,data_price,data_news
    testOn=True
    resetMeter()
    coin = app.getEntry("Coin: ")
    startDate = str(app.getDatePicker("start_date_dp"))
    endDate = str(app.getDatePicker("end_date_dp"))

    sentiment_module.setDate(startDate, endDate)
    data_price = getPrices()
    status = 1
    updateMeter()

    data_news = getNews()

    status = 2
    updateMeter()

    sentiment_module.scoreSentimentAnalysis(data_news)
    random_forest_mod.setCoin(coin)
    random_forest_mod.setData(data_price, sentiment_module.scoreFilter_BlankPadding("rares"))
    random_forest_mod.testSentiment("rares")

    random_forest_mod.setData(data_price, sentiment_module.scoreFilter_BlankPadding("goel"))
    random_forest_mod.testSentiment("goel")

    status = 3
    updateMeter()

    random_forest_mod.setData(data_price, sentiment_module.scoreFilter_BlankPadding("0"))
    random_forest_mod.testSentiment("0")

    random_forest_mod.testNormal()

    status = 4
    updateMeter()

    linear_mod = LinearRegressionMethod()
    linear_mod.setCoin(coin)
    linear_mod.setData(data_price)
    linear_mod.train()
    linear_mod.testPrediction()
    status = 5
    updateMeter()


def reload(btn):
    global status, coin, startDate, endDate, testOn, random_forest_mod, sentiment_module, data_price, data_news
    resetMeter()
    if testOn==False:
        status = 1
        updateMeter()

        random_forest_mod.setDataForPrediction(data_price, sentiment_module.scoreFilter_BlankPadding("rares"))
        random_forest_mod.predictSentiment("rares")

        status = 2
        updateMeter()

        random_forest_mod.setDataForPrediction(data_price, sentiment_module.scoreFilter_BlankPadding("goel"))
        random_forest_mod.predictSentiment("goel")

        status = 3
        updateMeter()

        random_forest_mod.setDataForPrediction(data_price, sentiment_module.scoreFilter_BlankPadding("0"))
        random_forest_mod.predictSentiment("0")

        status = 4
        updateMeter()

        random_forest_mod.predictNormal()
        status = 5
        updateMeter()

    else:
        status = 1
        updateMeter()

        random_forest_mod.setData(data_price, sentiment_module.scoreFilter_BlankPadding("rares"))
        random_forest_mod.testSentiment("rares")

        status = 2
        updateMeter()

        random_forest_mod.setData(data_price, sentiment_module.scoreFilter_BlankPadding("goel"))
        random_forest_mod.testSentiment("goel")

        status = 3
        updateMeter()

        random_forest_mod.setData(data_price, sentiment_module.scoreFilter_BlankPadding("0"))
        random_forest_mod.testSentiment("0")

        status = 4
        updateMeter()

        random_forest_mod.testNormal()

        status = 5
        updateMeter()


def changePrediction(btn):
    if testOn==False:
        if btn=="RF+SA(R)":
            app.setImage("plot","predicted_sent_rares.png")
        elif btn=="RF+SA(G)":
            app.setImage("plot", "predicted_sent_goel.png")
        elif btn=="RF+SA(0)":
            app.setImage("plot", "predicted_sent_0.png")
        elif btn=="LR":
            app.setImage("plot", "predicted_linear_regression.png")
        elif btn=="RF":
            app.setImage("plot", "predicted_rf.png")
    else:
        if btn=="RF+SA(R)":
            app.setImage("plot","test_sent_rares.png")
        elif btn=="RF+SA(G)":
            app.setImage("plot", "test_sent_goel.png")
        elif btn=="RF+SA(0)":
            app.setImage("plot", "test_sent_0.png")
        elif btn=="LR":
            app.setImage("plot", "test_linear_regression.png")
        elif btn=="RF":
            app.setImage("plot", "test_rf.png")

def resetMeter():
    app.setMeter("progress",0)

def updateMeter():
    app.setMeter("progress",20*status)

app = gui("Oraklion", useTtk=True)

app.setTtkTheme("vista")

app.startLabelFrame("Settings")
app.setSticky("n")
app.setStretch("column")
app.setPadding([5, 5])
app.addLabel(title="")

app.setPadding([5, 12])
app.addLabelEntry("Coin: ")
app.addLabel("l12", "Choose the starting date:")
app.addDatePicker("start_date_dp")
app.setDatePickerRange("start_date_dp", 2016, 2018)
app.addButton("Run prediction", runPredictions)

app.setPadding([5, 5])
app.addLabel(title=" ")
app.setPadding([5, 12])
app.addLabel("l13", "Choose the ending date:")
app.addDatePicker("end_date_dp")
app.setDatePickerRange("end_date_dp", 2016, 2018)
app.addButton("Run Tests", runTests)
app.addButton("Reload RF",reload)
app.addMeter("progress")
app.setMeterFill("progress", "blue")
app.registerEvent(updateMeter)
app.stopLabelFrame()

app.startLabelFrame("Results", column=1, colspan=2, row=0, rowspan=8)
app.setPadding([5, 5])
app.addImage("plot", "Oraklion.png")
app.setSticky("n")
app.addButtons(["LR", "RF", "RF+SA(0)", "RF+SA(G)", "RF+SA(R)"], changePrediction)
app.stopLabelFrame()

app.go()

