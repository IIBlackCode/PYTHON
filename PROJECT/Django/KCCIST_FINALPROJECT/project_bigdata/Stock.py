import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
import os
import datetime

from eunjeon import Mecab
import requests
from bs4 import BeautifulSoup
import FinanceDataReader as fdr
from datetime import datetime, timedelta
import csv

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# 정규화 함수
def MinMaxScaler(data):
    denom = np.max(data,0)-np.min(data,0)
    nume = data-np.min(data,0)
    return nume/denom

# 정규화 되돌리기 함수
def back_MinMax(data,value):
    diff = np.max(data,0)-np.min(data,0)
    back = value * diff + np.min(data,0)
    return back

# seqLength일간의 데이터(X)와 predictDate(Y)일 후 데이터를 매핑
def getXY(timeSeries, seqLength, predictDate):
    xdata = []
    ydata = []
    print('len(timeSeries)-seqLength-predictDate): ', len(timeSeries)-seqLength-predictDate)
    for i in range(0, len(timeSeries)-seqLength-predictDate):
        tx = timeSeries[i:i+seqLength,:-1]
        ty = timeSeries[i+seqLength:i+seqLength+predictDate,[-1]]
        xdata.append(tx)
        ydata.append(ty)
    return np.array(xdata), np.array(ydata)

def getX(timeSeries, seqLength):
    xdata = []
    tx = timeSeries[:seqLength]
    xdata.append(tx)
    return np.array(xdata)


def getModel(xy, predictDate, seqLength, name, hidden, unit, epoch, batch):
    # trainSize = len(xy) - predictDate*2
    trainSize = int(len(xy) * 0.7)
    trainSet = MinMaxScaler(xy[0:trainSize])
    testSet = MinMaxScaler(xy[trainSize - seqLength:])

    trainX, trainY = getXY(trainSet, seqLength, predictDate)
    testX, testY = getXY(testSet, seqLength, predictDate)
    print('trainX.shape[1], trainX.shape[2]: ', trainX.shape[1], trainX.shape[2])

    ## 모델 구성
    model = keras.Sequential()

    if 'RNN' in name:
        model.add(layers.SimpleRNN(units=unit, activation='tanh', return_sequences=True,
                                   input_shape=[trainX.shape[1], trainX.shape[2]]))
        for _ in range(hidden):
            model.add(layers.SimpleRNN(units=unit, activation='tanh', return_sequences=True))
        model.add(layers.SimpleRNN(units=20, activation='tanh'))

    elif 'LSTM' in name:
        model.add(layers.LSTM(units=unit, activation='relu', return_sequences=True,
                              input_shape=[trainX.shape[1], trainX.shape[2]]))
        for _ in range(hidden):
            model.add(layers.LSTM(units=unit, activation='relu', return_sequences=True))
        model.add(layers.LSTM(units=20, activation='relu'))

    elif 'BidLSTM' in name:
        model.add(layers.Bidirectional(layers.LSTM(units=unit, activation='relu', return_sequences=True),
                                       input_shape=[trainX.shape[1], trainX.shape[2]]))
        for _ in range(hidden):
            model.add(layers.Bidirectional(layers.LSTM(units=unit, activation='relu', return_sequences=True)))
        model.add(layers.Bidirectional(layers.LSTM(units=20, activation='relu')))

    elif 'GRU' in name:
        model.add(layers.GRU(units=unit, activation='tanh', return_sequences=True,
                             input_shape=[trainX.shape[1], trainX.shape[2]]))
        for _ in range(hidden):
            model.add(layers.GRU(units=unit, activation='tanh', return_sequences=True))
        model.add(layers.GRU(units=20, activation='tanh'))

    model.add(layers.Dense(predictDate))
    model.summary()

    # 모델 학습과정 설정
    model.compile(loss='mse', optimizer='adam', metrics=['mae', ])

    # 얼리스탑 & 모델 저장
    early_stop = EarlyStopping(monitor='loss', patience=5)
    filename = os.path.join('./models', name + '.h5')
    checkpoint = ModelCheckpoint(filename, monitor='loss', verbose=1, save_best_only=True, mode='auto')

    # 모델 트레이닝
    hist = model.fit(trainX, trainY, epochs=epoch, batch_size=batch, callbacks=[early_stop, checkpoint])
    # 모델 테스트
    res = model.evaluate(testX, testY, batch_size=batch)
    print("loss: ", res[0])
    print("mae: ", res[1])

    return model, res

def getPredict(model, testX, xy):
    # 7 모델 사용
    xhat = testX
    yhat = model.predict(xhat)
    # 원래 값으로 되돌리기
    predict = back_MinMax(xy[:, [-1]], yhat)
    predict = predict.reshape(-1)
    # print("예측값",predict)

    return predict







def updateStockCSV():
    TODAY = datetime.today().strftime("%Y-%m-%d")
    YESTERDAY = (datetime.strptime(TODAY, '%Y-%m-%d') + timedelta(days=-1)).strftime("%Y-%m-%d")
    LAST_TIME = (datetime.today() - timedelta(180)).strftime("%Y-%m-%d")

    dicList = pd.read_csv("./project_bigdata/csv/dictionary.csv", usecols=[1, 2], encoding="CP949")
    dic = {}
    for d in dicList.values:
        dic[d[0]] = d[1]

    sample = pd.read_csv("./project_bigdata/csv/Total.csv", usecols=[0,1], encoding='cp949')
    for i in sample.values:
        name = i[0]
        code = str(i[1])
        code = "0" * (6 - len(code)) + code
        if name != '게임테마' and name != '겨울테마' and name != '자율주행차테마' and name != '항공여행테마' and name != '인공지능테마':
            df = fdr.DataReader(code, LAST_TIME, TODAY)
            df['5Days'] = df['Close'].rolling(5).mean()
            df['10Days'] = df['Close'].rolling(10).mean()
            df['20Days'] = df['Close'].rolling(20).mean()
            df['60Days'] = df['Close'].rolling(60).mean()
            df['120Days'] = df['Close'].rolling(120).mean()
            df['emotion'] = 0
            df['count'] = 0
            df = df.reset_index()

            # 크롤링
            flag = False
            page = 1
            find_emo = {}

            while True:
                request = requests.get(f"http://www.paxnet.co.kr/news/{code}/stock?currentPageNo={page}")
                soup = BeautifulSoup(request.text, "lxml")
                ul = soup.find("div", {"id": "contents"})
                div1 = ul.find("div", {"class": "board-thumbnail"})
                if div1 != None:
                    div2 = div1.find("ul", {"class": "thumb-list"})
                    li = div2.find_all("li")
                    for i in li:
                        date = i.find("dl").find("dd", {"class": "date"}).find_all("span")[1].text.split(" ")
                        if date[0] >= YESTERDAY:
                            news = i.find("dl").find("dd", {"class": "date"}).find_all("span")[0].text
                            if news != "인포스탁" and (date[1] < "09:00" or date[1] > "15:30"):
                                link = "http://www.paxnet.co.kr" + i.find("dl").find("dt").find("a")["href"]
                                subRequest = requests.get(link)
                                subSoup = BeautifulSoup(subRequest.text, "lxml")
                                div = subSoup.find("div", {"id": "contents"}).find("div", {"class": "cont-area"}).find(
                                    "div", {
                                        "class": "report-view"}).find("div", {"class": "report-view-cont"})
                                p = div.find_all("p")
                                content = div.find("div", {"id": "span_article_content"})
                                textSum = []
                                for cont in p:
                                    textSum.append(cont.text)
                                textTemp = "".join(textSum).join(content.text)
                                dateT = datetime.strptime(date[0], "%Y.%m.%d")

                                if date[1] > "15:30":
                                    dateT += timedelta(days=1)
                                    tempDateT = str(dateT).split(" ")
                                    emoDate = tempDateT[0].replace(".", "-")
                                    if emoDate == YESTERDAY:
                                        find_emo[emoDate] = find_emo.get(emoDate, "") + textTemp
                                        df.loc[df["Date"] == emoDate, "count"] += 1
                                elif date[1] < "09:00":
                                    emoDate = date[0].replace(".", "-")
                                    if emoDate == TODAY:
                                        find_emo[emoDate] = find_emo.get(emoDate, "") + textTemp
                                        df.loc[df["Date"] == emoDate, "count"] += 1

                        else:
                            flag = True
                            break

                    page += 1

                    if flag:
                        break

                else:
                    break

            for k, v in find_emo.items():
                count, score = 0, 0
                m = Mecab()
                list = m.morphs(v)

                for word in list:
                    if word in dic.keys():
                        if dic[word] == 1:
                            score += 1
                        count += 1

                if count != 0:
                    for sc in df.values:
                        if str(sc[0]) == k:
                            temp = int((score / count) * 100)
                            emotion = 0

                            if temp > 58:
                                emotion = 1
                            elif temp <= 46:
                                emotion = -1

                            df.loc[df["Date"] == k, "emotion"] = emotion

            df['Escore'] = (df['Close'] + (df['Close'] * 0.01 * df['emotion'] * (df['count']))).astype(np.int64)
            df = df.dropna()
            df.reset_index(drop=False, inplace=True)
            df = df.iloc[-1]
            df1 = [str(df[1])[:10]]
            for j in range(2,len(df)) :
                df1.append(df[j])
            fs = open(f'./project_bigdata/csv/{name}.csv', 'a', newline='', encoding='UTF-8-sig')
            ##
            dfTmp = pd.read_csv(f'./project_bigdata/csv/{name}.csv', encoding='utf-8')
            if dfTmp['Date'][-1:].values != [TODAY]:
                wr = csv.writer(fs)
                wr.writerow(df1)
            fs.close()

def updateThemeCSV() :
    TODAY = datetime.today().strftime("%Y-%m-%d")
    themelist = ['게임','겨울', '인공지능', '자율주행차', '항공여행']
    for k in themelist:
        sample = pd.read_csv(f'./project_bigdata/csv/{k}.csv', usecols=[0, 1], encoding='cp949')
        namelist = []
        for m in sample.values[:-1]:
            name = m[0]
            temp = pd.read_csv(f'./project_bigdata/csv/{name}.csv', encoding="utf-8")
            namelist.append(temp)
        df_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Change', '5Days', '10Days',
                      '20Days', '60Days', '120Days', 'emotion', 'count', 'Escore']
        df = pd.DataFrame(columns=df_columns)
        df = namelist[0]
        for i in range(0, len(namelist)):
            df['Date'] = namelist[i]['Date']
            df['Open'] += namelist[i]['Open']
            df['High'] += namelist[i]['High']
            df['Low'] += namelist[i]['Low']
            df['Close'] += namelist[i]['Close']
            df['Volume'] += namelist[i]['Volume']
            df['Change'] += namelist[i]['Change']
            df['5Days'] += namelist[i]['5Days']
            df['10Days'] += namelist[i]['10Days']
            df['20Days'] += namelist[i]['20Days']
            df['60Days'] += namelist[i]['60Days']
            df['120Days'] += namelist[i]['120Days']
            df['emotion'] += namelist[i]['emotion']
            df['count'] += namelist[i]['count']
        df['Open'] //= len(namelist)
        df['High'] //= len(namelist)
        df['Low'] //= len(namelist)
        df['Close'] //= len(namelist)
        df['Volume'] //= len(namelist)
        df['Change'] /= len(namelist)
        df['5Days'] /= len(namelist)
        df['10Days'] /= len(namelist)
        df['20Days'] /= len(namelist)
        df['60Days'] /= len(namelist)
        df['120Days'] /= len(namelist)
        df['emotion'] = np.ceil(df['emotion'] / len(namelist))
        df['count'] = np.round(np.sqrt(df['count']), 1)
        df['Escore'] = (df['Close'] + (df['Close'] * 0.01 * df['emotion'] * (df['count']))).astype(np.int64)
        cnt = 0
        for i in df['emotion'].values:
            if i > 0:
                df.loc[cnt, 'emotion'] = 1
            elif i < 0:
                df.loc[cnt, 'emotion'] = -1
            else:
                df.loc[cnt, 'emotion'] = 0
            cnt += 1
        df = df.iloc[-1]
        df1 = []
        for j in df_columns:
            df1.append(df[j])
        fs = open(f'./project_bigdata/csv/{k}테마.csv', 'a', newline='', encoding='utf-8-sig')
        dfTmp = pd.read_csv(f'./project_bigdata/csv/{k}테마.csv', encoding='utf-8')
        if dfTmp['Date'][-1:].values != [TODAY]:
            wr = csv.writer(fs)
            wr.writerow(df1)
        fs.close()